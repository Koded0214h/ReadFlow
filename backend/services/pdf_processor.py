from datetime import timezone
import os
import pdfplumber
from django.core.files.base import ContentFile
from documents.models import Document, ContentChunk

class PDFProcessor:
    def __init__(self, document_id):
        self.document_id = document_id
        self.document = Document.objects.get(id=document_id)
    
        # In your PDFProcessor
    def process_document(self):
        try:
            self.document.status = Document.PROCESSING
            self.document.save()
            
            chunks = self.extract_content()
            self.create_chunks(chunks)
            
            # Refresh the document to ensure we have the latest version
            self.document.refresh_from_db()
            self.document.status = Document.COMPLETED
            self.document.processed_at = timezone.now()  # Add this import
            self.document.save()
            
            return True
        except Exception as e:
            self.document.status = Document.FAILED
            self.document.save()
            raise e
    
    def extract_content(self):
        """Extract and chunk content from PDF"""
        chunks = []
        chunk_index = 0
        
        with pdfplumber.open(self.document.file.path) as pdf:
            self.document.pages = len(pdf.pages)
            self.document.save()
            
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text
                text = page.extract_text() or ""
                
                if text.strip():
                    # Simple paragraph-based chunking
                    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                    
                    for para in paragraphs:
                        if len(para) > 50:  # Only create chunks for substantial content
                            chunks.append({
                                'chunk_index': chunk_index,
                                'content_type': ContentChunk.TEXT,
                                'content': para,
                                'reading_time': self.estimate_reading_time(para),
                                'metadata': {
                                    'page_number': page_num,
                                    'word_count': len(para.split()),
                                    'char_count': len(para)
                                }
                            })
                            chunk_index += 1
        
        return chunks
    
    def estimate_reading_time(self, text):
        """Estimate reading time in seconds (average: 200 words per minute)"""
        word_count = len(text.split())
        return max(5, int((word_count / 200) * 60))  # Minimum 5 seconds
    
    def create_chunks(self, chunks):
        """Create ContentChunk objects in database"""
        for chunk_data in chunks:
            ContentChunk.objects.create(
                document=self.document,
                **chunk_data
            )   