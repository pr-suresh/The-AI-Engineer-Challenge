#!/usr/bin/env python3
"""
Create a simple test PDF file using PyPDF2
"""

import PyPDF2
from io import BytesIO

def create_simple_pdf():
    """Create a simple PDF file for testing"""
    
    # Create a PDF writer
    pdf_writer = PyPDF2.PdfWriter()
    
    # Create a simple page (this is a basic example)
    # Note: PyPDF2 doesn't create content, it only manipulates existing PDFs
    # So we'll create a minimal PDF structure
    
    # Create a simple text-based PDF using reportlab if available
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Create PDF in memory
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Add content
        c.drawString(100, 750, "Test PDF Document")
        c.drawString(100, 720, "This is a test document for the PDF RAG chat system.")
        c.drawString(100, 690, "It contains information about artificial intelligence.")
        c.drawString(100, 660, "AI is a branch of computer science that aims to create intelligent machines.")
        c.drawString(100, 630, "Machine learning is a subset of AI that enables computers to learn.")
        c.drawString(100, 600, "Deep learning uses neural networks with multiple layers.")
        c.drawString(100, 570, "Natural language processing helps computers understand human language.")
        c.drawString(100, 540, "Computer vision enables machines to interpret visual information.")
        c.drawString(100, 510, "Robotics combines AI with mechanical engineering.")
        c.drawString(100, 480, "The future of AI holds great promise for solving complex problems.")
        
        c.save()
        
        # Get the PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        # Save to file
        with open('test_document.pdf', 'wb') as f:
            f.write(pdf_content)
        
        print("✅ Created test_document.pdf successfully")
        return True
        
    except ImportError:
        print("❌ ReportLab not available, cannot create PDF content")
        print("   Install with: pip install reportlab")
        return False

if __name__ == "__main__":
    create_simple_pdf() 