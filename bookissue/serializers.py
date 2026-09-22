from rest_framework import serializers
from bookissue.models import BookIssue

class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookIssue
        fields=['issue_id', 'student', 'book', 'issue_date', 'upt_at']
        read_only_fields=['issue_id', 'issue_date', 'upt_at']

    # def get_student_count(self, obj): #NOSONAR
    #     return obj.issues.values("student").distinct().count() #NOSONAR

