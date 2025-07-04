#!/usr/bin/env python3
"""
Simple PDF RAG Chat System Test Script

This script tests the basic functionality without requiring external PDF generation libraries.
It uses the existing test_document.txt file and tests the core API endpoints.

Usage:
    python simple_test.py [--api-key YOUR_API_KEY] [--base-url BASE_URL]
"""

import requests
import json
import time
import os
import sys
import argparse
import tempfile
import subprocess
from typing import Optional, Dict, Any

class SimplePDFRAGTester:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str = "", details: Dict[str, Any] = None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details or {}
        }
        self.test_results.append(result)
        
    def create_test_pdf(self) -> str:
        """Create a test PDF from the text document"""
        try:
            # Check if test_document.txt exists
            if not os.path.exists('test_document.txt'):
                self.log_test("Test PDF Creation", False, "test_document.txt not found")
                return None
            
            # Try to convert to PDF using pandoc
            pdf_path = 'test_document.pdf'
            try:
                subprocess.run(['pandoc', 'test_document.txt', '-o', pdf_path], check=True)
                self.log_test("Test PDF Creation", True, f"Created {pdf_path}")
                return pdf_path
            except (subprocess.CalledProcessError, FileNotFoundError):
                # If pandoc fails, try using text file directly
                self.log_test("Test PDF Creation", False, "Pandoc not available, using text file")
                return 'test_document.txt'
                
        except Exception as e:
            self.log_test("Test PDF Creation", False, f"Error: {str(e)}")
            return None
    
    def test_health_check(self) -> bool:
        """Test API health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                success = data.get('status') == 'ok'
                self.log_test("Health Check", success, f"API Status: {data.get('status', 'unknown')}")
                return success
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_pdf_list_empty(self) -> bool:
        """Test getting empty PDF list"""
        try:
            response = self.session.get(f"{self.base_url}/api/pdfs")
            if response.status_code == 200:
                data = response.json()
                success = isinstance(data.get('pdfs', []), list)
                self.log_test("PDF List (Empty)", success, f"Found {len(data.get('pdfs', []))} PDFs")
                return success
            else:
                self.log_test("PDF List (Empty)", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("PDF List (Empty)", False, f"Error: {str(e)}")
            return False
    
    def test_pdf_upload(self) -> Optional[str]:
        """Test PDF upload and indexing"""
        if not self.api_key:
            self.log_test("PDF Upload", False, "No API key provided")
            return None
            
        try:
            # Create test PDF
            pdf_path = self.create_test_pdf()
            if not pdf_path:
                return None
            
            # Upload PDF
            with open(pdf_path, 'rb') as f:
                files = {'file': (os.path.basename(pdf_path), f, 'application/pdf' if pdf_path.endswith('.pdf') else 'text/plain')}
                data = {'api_key': self.api_key}
                
                response = self.session.post(
                    f"{self.base_url}/api/upload-pdf",
                    files=files,
                    data=data
                )
            
            if response.status_code == 200:
                data = response.json()
                pdf_id = data.get('pdf_id')
                chunks_count = data.get('chunks_count', 0)
                
                success = pdf_id is not None and chunks_count > 0
                self.log_test("PDF Upload", success, 
                             f"Uploaded PDF with {chunks_count} chunks", 
                             {"pdf_id": pdf_id, "chunks_count": chunks_count})
                return pdf_id if success else None
            else:
                error_detail = response.json().get('detail', 'Unknown error') if response.content else 'No response body'
                self.log_test("PDF Upload", False, f"HTTP {response.status_code}: {error_detail}")
                return None
                
        except Exception as e:
            self.log_test("PDF Upload", False, f"Error: {str(e)}")
            return None
    
    def test_pdf_list_with_pdf(self) -> bool:
        """Test getting PDF list after upload"""
        try:
            response = self.session.get(f"{self.base_url}/api/pdfs")
            if response.status_code == 200:
                data = response.json()
                pdfs = data.get('pdfs', [])
                success = len(pdfs) > 0
                self.log_test("PDF List (With PDFs)", success, f"Found {len(pdfs)} PDFs")
                return success
            else:
                self.log_test("PDF List (With PDFs)", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("PDF List (With PDFs)", False, f"Error: {str(e)}")
            return False
    
    def test_chat_functionality(self, pdf_id: str) -> bool:
        """Test chat functionality with uploaded PDF"""
        if not self.api_key:
            self.log_test("Chat Functionality", False, "No API key provided")
            return False
            
        try:
            # Test basic question
            chat_data = {
                "user_message": "What is artificial intelligence?",
                "pdf_id": pdf_id,
                "api_key": self.api_key,
                "model": "gpt-4o-mini"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=chat_data,
                stream=True
            )
            
            if response.status_code == 200:
                # Read streaming response
                content = ""
                for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                    if chunk:
                        content += chunk
                
                success = len(content) > 0
                self.log_test("Chat Functionality", success, 
                             f"Received {len(content)} characters response",
                             {"response_length": len(content)})
                return success
            else:
                error_detail = response.json().get('detail', 'Unknown error') if response.content else 'No response body'
                self.log_test("Chat Functionality", False, f"HTTP {response.status_code}: {error_detail}")
                return False
                
        except Exception as e:
            self.log_test("Chat Functionality", False, f"Error: {str(e)}")
            return False
    
    def test_chat_without_pdf(self) -> bool:
        """Test chat functionality without selecting a PDF"""
        if not self.api_key:
            self.log_test("Chat Without PDF", False, "No API key provided")
            return False
            
        try:
            chat_data = {
                "user_message": "What is artificial intelligence?",
                "pdf_id": "nonexistent-pdf-id",
                "api_key": self.api_key
            }
            
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=chat_data
            )
            
            # Should return an error
            success = response.status_code != 200
            self.log_test("Chat Without PDF", success, 
                         f"Expected error, got HTTP {response.status_code}")
            return success
                
        except Exception as e:
            self.log_test("Chat Without PDF", False, f"Error: {str(e)}")
            return False
    
    def test_invalid_file_upload(self) -> bool:
        """Test uploading invalid file type"""
        if not self.api_key:
            self.log_test("Invalid File Upload", False, "No API key provided")
            return False
            
        try:
            # Create a text file instead of PDF
            fd, temp_path = tempfile.mkstemp(suffix='.txt')
            with os.fdopen(fd, 'w') as f:
                f.write("This is not a PDF file")
            
            with open(temp_path, 'rb') as f:
                files = {'file': ('test.txt', f, 'text/plain')}
                data = {'api_key': self.api_key}
                
                response = self.session.post(
                    f"{self.base_url}/api/upload-pdf",
                    files=files,
                    data=data
                )
            
            # Clean up
            os.unlink(temp_path)
            
            # Should return an error
            success = response.status_code == 400
            self.log_test("Invalid File Upload", success, 
                         f"Expected 400 error, got HTTP {response.status_code}")
            return success
                
        except Exception as e:
            self.log_test("Invalid File Upload", False, f"Error: {str(e)}")
            return False
    
    def test_pdf_deletion(self, pdf_id: str) -> bool:
        """Test PDF deletion"""
        try:
            response = self.session.delete(f"{self.base_url}/api/pdfs/{pdf_id}")
            
            if response.status_code == 200:
                self.log_test("PDF Deletion", True, f"Successfully deleted PDF {pdf_id}")
                return True
            else:
                self.log_test("PDF Deletion", False, f"HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("PDF Deletion", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return results"""
        print("🚀 Starting Simple PDF RAG Chat System Tests")
        print("=" * 50)
        
        # Test 1: Health check
        if not self.test_health_check():
            print("\n❌ API is not available. Please start the server first.")
            print("   Run: uvicorn api.app:app --host 0.0.0.0 --port 8000")
            return {"success": False, "message": "API not available"}
        
        # Test 2: Empty PDF list
        self.test_pdf_list_empty()
        
        # Test 3: Invalid file upload
        self.test_invalid_file_upload()
        
        # Test 4: PDF upload (if API key provided)
        pdf_id = None
        if self.api_key:
            pdf_id = self.test_pdf_upload()
            
            if pdf_id:
                # Test 5: PDF list with PDFs
                self.test_pdf_list_with_pdf()
                
                # Test 6: Chat functionality
                self.test_chat_functionality(pdf_id)
                
                # Test 7: PDF deletion
                self.test_pdf_deletion(pdf_id)
        else:
            print("\n⚠️  No API key provided. Skipping upload and chat tests.")
            print("   Use --api-key YOUR_API_KEY to test full functionality.")
            print("   Or set OPENAI_API_KEY environment variable.")
        
        # Test 8: Chat without PDF
        self.test_chat_without_pdf()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Results Summary")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! The PDF RAG chat system is working correctly.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Please check the details above.")
        
        return {
            "success": passed == total,
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": total - passed,
            "success_rate": (passed/total)*100,
            "results": self.test_results
        }

def main():
    parser = argparse.ArgumentParser(description="Simple Test PDF RAG Chat System")
    parser.add_argument("--api-key", help="OpenAI API key for testing")
    parser.add_argument("--base-url", default="http://localhost:8000", 
                       help="Base URL of the API server")
    parser.add_argument("--start-server", action="store_true",
                       help="Start the FastAPI server before testing")
    
    args = parser.parse_args()
    
    # Check if API key is provided via environment variable
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    
    # Start server if requested
    if args.start_server:
        print("🚀 Starting FastAPI server...")
        try:
            # Start server in background
            server_process = subprocess.Popen(
                ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"],
                cwd=os.getcwd()
            )
            
            # Wait for server to start
            time.sleep(3)
            
            print("✅ Server started successfully")
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return 1
    
    # Run tests
    tester = SimplePDFRAGTester(base_url=args.base_url, api_key=api_key)
    results = tester.run_all_tests()
    
    # Clean up server if we started it
    if args.start_server and 'server_process' in locals():
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()
    
    return 0 if results['success'] else 1

if __name__ == "__main__":
    sys.exit(main()) 