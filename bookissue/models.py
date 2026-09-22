from django.db import models
from book.models import Book
from student.models import Student

class BookIssue(models.Model):
    issue_id=models.BigAutoField(primary_key=True)
    student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="book_issues")
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="issues")
    issue_date=models.DateTimeField(auto_now_add=True)
    upt_at=models.DateTimeField(auto_now=True)

    class Meta:
        ''' BookIssue table'''
        db_table = 'bkis'
        
