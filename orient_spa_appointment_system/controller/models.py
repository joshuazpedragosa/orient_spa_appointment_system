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
        
        
class services(models.Model):
    service_name = models.CharField(max_length=100, null=False, default='')
    service_price = models.IntegerField(default=0, null=False)
    service_img = models.ImageField(upload_to='image_uploads')
    service_description = models.CharField(max_length=250, null=False, default='')
    
    class Meta:
        db_table = 'tbl_services'
        
class appointments(models.Model):
    client_name = models.CharField(max_length=100, null=False, default='')
    client_email = models.CharField(max_length=100, null=False, default='')
    client_number = models.IntegerField(default=0, null=False)
    appointment_date = models.CharField(max_length=100, null=False, default='')
    appointment_time = models.CharField(max_length=100, null=False, default='')
    service_id = models.IntegerField(default=0, null=False)
    service_name = models.CharField(max_length=100, null=False, default='')
    service_price = models.IntegerField(default=0, null=False)
    appointment_status = models.CharField(max_length=20, null=False, default='Pending')
    
    class Meta: 
        db_table = 'tbl_appointment'
        
class employee_schedule(models.Model):
    employee_vid = models.CharField(max_length=200, null=False, default='')
    appointment_id = models.IntegerField(default=0, null=False)
    time = models.CharField(max_length=100, null=False, default='')
    date = models.CharField(max_length=100,  null=False, default='')
    status = models.CharField(max_length=20, null=False, default='To Pay')
    
    class Meta:
        db_table = 'tbl_employee_schedule'
        
class dtr_record(models.Model):
    employee_vid = models.CharField(max_length=200, null=False, default='')
    am_in = models.CharField(max_length=20, null=True, default='')
    am_out = models.CharField(max_length=20, null=True, default='')
    pm_in = models.CharField(max_length=20, null=True, default='')
    pm_out = models.CharField(max_length=20, null=True, default='')
    date = models.CharField(max_length=20, null=True, default='')
    
    class Meta:
        db_table = 'tbl_dtr'