from django.db import models
from base.models import Account


class ProductName(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    added_on = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.product_name


class ProductTestData(models.Model):
    product_name = models.ForeignKey(ProductName, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=200)
    method = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    mins = models.CharField(max_length=200)
    maxs = models.CharField(max_length=200)
    typical = models.CharField(max_length=2)
    added_on = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.product_name)  # type casting for foreign key


class TestName(models.Model):
    test_name = models.CharField(max_length=200, unique=True)
    user_id = models.ForeignKey(Account)
    added_on = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.test_name


class ProductTestList(models.Model):
    product_name = models.ForeignKey(ProductName, on_delete=models.CASCADE)
    test_name = models.ForeignKey(TestName, on_delete=models.CASCADE)
    method = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)
    mins = models.CharField(max_length=200)
    maxs = models.CharField(max_length=200)
    typical = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.test_name)  # type casting for foreign key


class CustomerContact(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_address = models.CharField(max_length=400)
    customer_contacts_name = models.CharField(max_length=200)
    customer_contact = models.CharField(max_length=100)
    reference_contact_name = models.CharField(max_length=200)
    reference_contact = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name


class EquipmentDetails(models.Model):
    equipment_number = models.CharField(max_length=200)
    equipment_make = models.CharField(max_length=200 ,null=True, blank=True)
    equipment_model = models.CharField(max_length=200)
    component = models.CharField(max_length=400)
    component_make = models.CharField(max_length=400)
    component_model = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100)
    lube_oil = models.ForeignKey(ProductName, on_delete=models.CASCADE)
    capacity = models.CharField(max_length=100)


class OilAnalysisTests(models.Model):
    test_name = models.CharField(max_length=200, unique=True)
    user_id = models.ForeignKey(Account)
    added_on = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.test_name


class ElementalAnalysisTests(models.Model):
    test_name = models.CharField(max_length=200, unique=True)
    user_id = models.ForeignKey(Account)
    added_on = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.test_name
