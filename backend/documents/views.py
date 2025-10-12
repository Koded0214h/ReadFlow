from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Document, ContentChunk
from .serializers import DocumentSerializer, ContentChunkSerializer, DocumentUploadSerializer
from services.pdf_processor import PDFProcessor

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # Use the upload serializer for validation
        upload_serializer = DocumentUploadSerializer(data=request.data)
        
        if upload_serializer.is_valid():
            file = upload_serializer.validated_data['file']
            title = upload_serializer.validated_data.get('title') or file.name
            
            # Create the document with all required fields
            document = Document.objects.create(
                user=request.user,
                title=title,
                original_filename=file.name,
                file=file,
                file_size=file.size
            )
            
            # Process the PDF
            try:
                processor = PDFProcessor(document.id)
                processor.process_document()
            except Exception as e:
                document.status = Document.FAILED
                document.save()
                return Response(
                    {'error': 'Failed to process PDF'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Return the document using the main serializer
            serializer = self.get_serializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(upload_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        # Remove this method since we're overriding create()
        pass
    
    @action(detail=True, methods=['get'])
    def chunks(self, request, pk=None):
        document = self.get_object()
        chunks = document.chunks.all()
        serializer = ContentChunkSerializer(chunks, many=True)
        return Response(serializer.data)

class ContentChunkViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContentChunkSerializer
    
    def get_queryset(self):
        return ContentChunk.objects.filter(
            document__user=self.request.user
        )
        
        
    
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Document

@login_required
def library_view(request):
    documents = Document.objects.filter(user=request.user)
    return render(request, 'library.html', {
        'documents': documents
    })

@login_required
def upload_view(request):
    return render(request, 'upload.html')

@login_required
def read_view(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)
    chunks = document.chunks.all().order_by('chunk_index')
    
    # Mock user interests (you'll implement this properly later)
    user_interests = ['Technology', 'Business']  # This will come from user profile
    
    total_reading_time = sum(chunk.reading_time for chunk in chunks)
    
    return render(request, 'reading/read_document.html', {
        'document': document,
        'chunks': chunks,
        'user_interests': user_interests,
        'total_reading_time': total_reading_time // 60
    })

# API Test Views
def test_dashboard(request):
    """Main test dashboard with links to all test pages"""
    return render(request, 'test/dashboard.html')

def test_register(request):
    """Test page for user registration API"""
    return render(request, 'test/register.html')

def test_login(request):
    """Test page for user login API"""
    return render(request, 'test/login.html')

@login_required
def test_profile(request):
    """Test page for user profile API"""
    return render(request, 'test/profile.html')

@login_required
def test_documents(request):
    """Test page for documents API (CRUD operations)"""
    return render(request, 'test/documents.html')

@login_required
def test_chunks(request):
    """Test page for chunks API"""
    return render(request, 'test/chunks.html')
