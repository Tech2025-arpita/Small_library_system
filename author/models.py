from django.db import models

class Author(models.Model):
    auth_id=models.BigAutoField(primary_key=True)
    auth_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ''' Author table'''
        db_table = 'Author_table'

    def __str__(self):
        return self.auth_name