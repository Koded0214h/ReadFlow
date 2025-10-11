from rest_framework import serializers
from .models import Document, ContentChunk

class ContentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentChunk
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    chunks = ContentChunkSerializer(many=True, read_only=True)
    
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('user', 'status', 'processed_at', 'metadata')

class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    title = serializers.CharField(max_length=500, required=False)
    
    def validate_file(self, value):
        if not value.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        if value.size > 50 * 1024 * 1024:  # 50MB limit
            raise serializers.ValidationError("File size must be under 50MB.")
        return value