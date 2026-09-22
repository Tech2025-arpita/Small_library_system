from django.db import models

class Student(models.Model):
    stdt_id=models.BigAutoField(primary_key=True)
    stdt_name=models.CharField(max_length=255)
    crt_at=models.DateTimeField(auto_now_add=True)
    upt_at=models.DateTimeField(auto_now=True)

    class Meta:
        ''' Student table'''
        db_table = 'Stdt'
        
    def __str__(self):
        return self.stdt_name