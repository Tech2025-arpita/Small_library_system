from django.db import models
from book.models import Book
from author.models import Author
from student.models import Student


class BookReview(models.Model):
    review_id=models.BigAutoField(primary_key=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="reviews")
    author=models.ForeignKey(Author,on_delete=models.CASCADE,related_name="reviews")
    stdt=models.ForeignKey(Student,on_delete=models.CASCADE,related_name="reviews")
    bk_desc=models.TextField()
    crt_at=models.DateTimeField(auto_now_add=True)
    upt_at=models.DateTimeField(auto_now=True)

    class Meta:
        ''' BookReview table'''
        db_table = 'bkrv'
        
    def __str__(self):
        return self.stdt
