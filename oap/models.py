from django.db import models
from base.models import Account
from inventory.models import CustomerContact, EquipmentDetails


class ProgressiveAnalysis(models.Model):
    date_sampled = models.DateTimeField(blank=True, null=True)
    date_received = models.DateTimeField(blank=True, null=True)
    lab_number = models.CharField(max_length=200, null=True, blank=True)
    date_reported = models.DateTimeField(blank=True, null=True)
    oil_life = models.CharField(max_length=200, blank=True, null=True)
    component_life = models.CharField(max_length=200, blank=True, null=True)
    filter_life = models.CharField(max_length=200, blank=True, null=True)
    daily_top_up = models.CharField(max_length=200, blank=True, null=True)
    oil_changed = models.CharField(max_length=100, blank=True, null=True)
    date_of_oil_renewed = models.DateTimeField(null=True, blank=True)
    sump_capacity = models.CharField(max_length=100, blank=True, null=True)
    reservoir_temperature = models.CharField(max_length=100, blank=True, null=True)
    oil_in = models.CharField(max_length=100, blank=True, null=True)
    oil_out = models.CharField(max_length=100, blank=True, null=True)
    coolant_in = models.CharField(max_length=100, blank=True, null=True)
    coolant_out = models.CharField(max_length=100, blank=True, null=True)


class OAPReport(models.Model):
    customer_contact = models.ForeignKey(CustomerContact)
    equipment_details = models.ForeignKey(EquipmentDetails)
    progressive_analysis = models.ForeignKey(ProgressiveAnalysis)
    Permission_Choices = (
        ('Ini', 'Initial'),
        ('Pen', 'Pending'),
        ('Apr', 'Approved'),
        ('Rej', 'Rejected'),
        ('Ver', 'Verified'),
    )
    comment = models.CharField(max_length=200, null=True, blank=True)

    permission_status = models.CharField(max_length=3, choices=Permission_Choices, default='Ini')
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)


class OilAnalysis(models.Model):
    oap_report = models.ForeignKey(OAPReport)
    user_id = models.ForeignKey(Account)
    test_name = models.CharField(max_length=200)
    result = models.CharField(max_length=200, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)


class ElementalAnalysis(models.Model):
    oap_report = models.ForeignKey(OAPReport)
    user_id = models.ForeignKey(Account)
    test_name = models.CharField(max_length=200)
    result = models.CharField(max_length=200, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

