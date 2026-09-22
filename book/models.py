from django.db import models
from author.models import Author

class Book(models.Model):
    bk_id=models.BigAutoField(primary_key=True)
    bk_name=models.CharField(max_length=255)
    bk_desc=models.CharField(max_length=255)
    crt_at=models.DateTimeField(auto_now_add=True)
    upt_at=models.DateTimeField(auto_now=True)
    crt_by=models.ForeignKey(Author,on_delete=models.CASCADE)

    class Meta:
            ''' Book table'''
            db_table = 'Book'
    
    def __str__(self):
        return self.bk_name