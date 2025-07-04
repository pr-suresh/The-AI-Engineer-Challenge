# PDF RAG Chat System Testing Guide

This guide explains how to test the PDF RAG chat system to ensure it's working correctly.

## Prerequisites

1. **Python Environment**: Make sure you have Python 3.8+ installed
2. **Dependencies**: Install the required packages
3. **OpenAI API Key**: You'll need an OpenAI API key for full testing
4. **Server Running**: The FastAPI server should be running

## Quick Start

### 1. Install Dependencies

```bash
# Install basic requirements
pip install requests

# Optional: Install PDF generation dependencies
pip install reportlab pandoc
```

### 2. Start the Server

```bash
# Start the FastAPI server
uvicorn api.app:app --host 0.0.0.0 --port 8000
```

### 3. Run Basic Tests

```bash
# Run simple tests (no external dependencies required)
python simple_test.py

# Run with API key for full testing
python simple_test.py --api-key YOUR_OPENAI_API_KEY

# Or set environment variable
export OPENAI_API_KEY=your_api_key_here
python simple_test.py
```

### 4. Run Comprehensive Tests

```bash
# Run full test suite with PDF generation
python test_pdf_rag.py --api-key YOUR_OPENAI_API_KEY

# Start server automatically and run tests
python test_pdf_rag.py --api-key YOUR_OPENAI_API_KEY --start-server
```

## Test Coverage

The test suite covers the following functionality:

### ✅ API Health Check
- Verifies the server is running and responding
- Tests the `/api/health` endpoint

### ✅ PDF Management
- **Empty PDF List**: Tests getting PDF list when no PDFs are uploaded
- **PDF Upload**: Tests uploading and indexing a PDF document
- **PDF List with PDFs**: Tests getting PDF list after upload
- **PDF Deletion**: Tests removing PDFs and their indexes

### ✅ Chat Functionality
- **Chat with PDF**: Tests asking questions about uploaded PDFs
- **Chat without PDF**: Tests error handling when no PDF is selected
- **Streaming Responses**: Tests real-time response streaming

### ✅ Error Handling
- **Invalid File Upload**: Tests rejection of non-PDF files
- **Missing API Key**: Tests behavior when API key is not provided
- **Invalid PDF ID**: Tests error handling for non-existent PDFs

## Test Files

- `simple_test.py`: Basic test script with minimal dependencies
- `test_pdf_rag.py`: Comprehensive test script with PDF generation
- `test_document.txt`: Sample document for testing
- `test_requirements.txt`: Additional dependencies for full testing

## Manual Testing

You can also test the system manually:

### 1. Frontend Testing

1. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

2. Open your browser to `http://localhost:5173`

3. Test the following:
   - Enter your OpenAI API key
   - Upload a PDF file
   - Ask questions about the PDF
   - Delete PDFs
   - Test error scenarios

### 2. API Testing with curl

```bash
# Health check
curl http://localhost:8000/api/health

# List PDFs
curl http://localhost:8000/api/pdfs

# Upload PDF
curl -X POST http://localhost:8000/api/upload-pdf \
  -F "file=@test_document.pdf" \
  -F "api_key=YOUR_API_KEY"

# Chat with PDF
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "What is artificial intelligence?",
    "pdf_id": "YOUR_PDF_ID",
    "api_key": "YOUR_API_KEY"
  }'

# Delete PDF
curl -X DELETE http://localhost:8000/api/pdfs/YOUR_PDF_ID
```

## Expected Test Results

### ✅ All Tests Pass
```
🚀 Starting Simple PDF RAG Chat System Tests
==================================================
✅ PASS Health Check: API Status: ok
✅ PASS PDF List (Empty): Found 0 PDFs
✅ PASS Invalid File Upload: Expected 400 error, got HTTP 400
✅ PASS Test PDF Creation: Created test_document.pdf
✅ PASS PDF Upload: Uploaded PDF with 5 chunks
✅ PASS PDF List (With PDFs): Found 1 PDFs
✅ PASS Chat Functionality: Received 245 characters response
✅ PASS PDF Deletion: Successfully deleted PDF abc123
✅ PASS Chat Without PDF: Expected error, got HTTP 404

==================================================
📊 Test Results Summary
==================================================
Total Tests: 9
Passed: 9
Failed: 0
Success Rate: 100.0%

🎉 All tests passed! The PDF RAG chat system is working correctly.
```

### ⚠️ Partial Test Results (No API Key)
```
🚀 Starting Simple PDF RAG Chat System Tests
==================================================
✅ PASS Health Check: API Status: ok
✅ PASS PDF List (Empty): Found 0 PDFs
❌ FAIL Invalid File Upload: No API key provided
❌ FAIL PDF Upload: No API key provided
❌ FAIL Chat Without PDF: No API key provided

⚠️  No API key provided. Skipping upload and chat tests.
   Use --api-key YOUR_API_KEY to test full functionality.
   Or set OPENAI_API_KEY environment variable.

==================================================
📊 Test Results Summary
==================================================
Total Tests: 5
Passed: 2
Failed: 3
Success Rate: 40.0%

⚠️  3 test(s) failed. Please check the details above.
```

## Troubleshooting

### Common Issues

1. **Server Not Running**
   ```
   ❌ FAIL Health Check: Connection error: [Errno 61] Connection refused
   ```
   **Solution**: Start the server with `uvicorn api.app:app --host 0.0.0.0 --port 8000`

2. **Missing API Key**
   ```
   ❌ FAIL PDF Upload: No API key provided
   ```
   **Solution**: Provide your OpenAI API key with `--api-key` or set `OPENAI_API_KEY` environment variable

3. **PDF Generation Failed**
   ```
   ❌ FAIL Test PDF Creation: Pandoc not available, using text file
   ```
   **Solution**: Install pandoc or reportlab for PDF generation, or use the simple test script

4. **Upload Errors**
   ```
   ❌ FAIL PDF Upload: HTTP 400: Invalid OpenAI API key format
   ```
   **Solution**: Check your API key format (should start with `sk-`)

### Debug Mode

For more detailed debugging, you can modify the test scripts to include more verbose output or check the server logs.

## Performance Testing

For performance testing, you can:

1. Upload larger PDFs
2. Test with multiple concurrent requests
3. Monitor response times
4. Test memory usage during indexing

## Security Testing

Consider testing:

1. API key validation
2. File type validation
3. Input sanitization
4. Rate limiting (if implemented)

## Continuous Integration

You can integrate these tests into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Test PDF RAG System
  run: |
    pip install requests
    python simple_test.py --api-key ${{ secrets.OPENAI_API_KEY }}
```

## Support

If you encounter issues:

1. Check the server logs for detailed error messages
2. Verify all dependencies are installed
3. Ensure your OpenAI API key is valid and has sufficient credits
4. Check that the server is running on the correct port 