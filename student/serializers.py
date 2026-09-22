from rest_framework import serializers
from student.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['stdt_id','stdt_name','crt_at','upt_at']
        read_only_fields=['stdt_id','crt_at','upt_at']



