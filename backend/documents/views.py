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