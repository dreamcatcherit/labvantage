from django.db import models
from inventory.models import ProductName, TestName
from base.models import Account


class LabRequestForm(models.Model):
    # lab request form 
    product_name = models.ForeignKey(ProductName, on_delete=models.CASCADE)
    ref_no = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField()
    batch_number = models.CharField(max_length=200, unique=True)
    sampling_time = models.DateTimeField()
    lab_test_number = models.CharField(null=True, max_length=200)
    sample_receiving_time = models.DateTimeField()
    sample_source = models.CharField(max_length=200)
    tank_number = models.CharField(max_length=200)
    batch_quantity = models.CharField(max_length=200)
    formulation_number = models.CharField(max_length=200)
    sample_type = models.CharField(max_length=200)
    comments = models.TextField(null=True)
    releasing_time = models.DateTimeField()
    Permission_Choices = (
        ('Pen', 'Pending'),
        ('Apr', 'Approved'),
        ('Rej', 'Rejected'),
        ('Ver', 'Verified'),
    )
    permission_status = models.CharField(max_length=3, choices=Permission_Choices, default='Pen')


# Lab Inspection Report Generation
class ProductInfo(models.Model):
    # upper form fields
    product_name = models.ForeignKey(ProductName, on_delete=models.CASCADE, null=True)
    lab_request_form = models.ForeignKey(LabRequestForm)
    batch_number = models.CharField(max_length=400, null=True)
    sample_number = models.CharField(max_length=400, null=True)
    test_type = models.CharField(max_length=400, null=True)
    serial_number = models.CharField(max_length=400, null=True)
    tank_number = models.CharField(max_length=400, null=True)
    batch_size = models.CharField(max_length=400, null=True)
    date_tested = models.DateTimeField(null=True)
    time_in_date = models.DateTimeField(null=True)
    time_out_date = models.DateTimeField(null=True)
    blending_date = models.DateTimeField(null=True)
    initial = models.BooleanField(default=False)
    Permission_Choices = (
        ('Pen', 'Pending'),
        ('Apr', 'Approved'),
        ('Rej', 'Rejected'),
        ('Ver', 'Verified'),
    )
    permission_status = models.CharField(max_length=3, choices=Permission_Choices, default='Pen')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TestInfo(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    product_name = models.ForeignKey(ProductName, on_delete=models.CASCADE)  # inventory
    test_name = models.ForeignKey(TestName, on_delete=models.CASCADE, null=True)
    method = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    mins = models.CharField(max_length=200)
    maxs = models.CharField(max_length=200)
    typical = models.CharField(max_length=200)
    result = models.CharField(max_length=200, null=True)
    sign = models.ForeignKey(Account, null=True)
    added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.test_name)  # type casting for foreign key


class ReleaseCertificateInfo(models.Model):
    product_name = models.CharField(max_length=400, null=True)
    sample_source = models.CharField(max_length=400, null=True)
    batch_number = models.CharField(max_length=400, null=True)
    sampling_time = models.DateTimeField(null=True)
    sample_tested = models.CharField(max_length=400, null=True)
    filling_weight_calculations = models.CharField(max_length=400, null=True)
    head_of_qa = models.CharField(max_length=400, null=True)
    date_signed = models.DateTimeField(auto_now_add=True, null=True)
