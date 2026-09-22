from rest_framework import serializers
from book.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['bk_id','bk_name','bk_desc','crt_at','upt_at','crt_by']
        read_only_fields=['bk_id','crt_at','upt_at']



