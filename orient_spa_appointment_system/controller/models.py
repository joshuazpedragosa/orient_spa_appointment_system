from django.db import models

# Create your models here.
class authentication(models.Model):
    v_id = models.CharField(max_length=200, null=False, default='')
    priv = models.IntegerField(null=False, default=2)
    first_name = models.CharField(max_length=100, null=False, default='')
    last_name = models.CharField(max_length=100, null=False, default='')
    email = models.CharField(max_length=100,  null=False, default='')
    password = models.CharField(max_length=200, null=False, default='')
    random_code = models.IntegerField(null=False, default=0)
    v_status = models.CharField(max_length=10, null=False, default='unverified')
    
    class Meta:
        db_table = 'tbl_users'    