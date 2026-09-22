from rest_framework import serializers
from bookreview.models import BookReview

class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookReview
        fields=['review_id','book','author','stdt','bk_desc','crt_at','upt_at']
        read_only_fields=['review_id', 'crt_at', 'upt_at']

