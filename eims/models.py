from base.models import Account
from django.db import models
import os


class InstrumentInfo(models.Model):
    instrument_name = models.CharField(max_length=100, unique=True)
    category_choices = (
        ('I', 'Instrument'),
        ('E', 'Equipment'),
        ('MD', 'Measuring Device'),
    )
    category_type = models.CharField(max_length=2, choices=category_choices, default='I')
    model_number = models.CharField(max_length=100, null=True, blank=True)
    supplier = models.CharField(max_length=100, null=True, blank=True)
    manufacturer = models.CharField(max_length=100)
    received_date = models.DateTimeField(null=True, blank=True)
    installation_date = models.DateTimeField(null=True, blank=True)
    po_date = models.DateTimeField(null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    instrument_category = models.CharField(max_length=100, null=True, blank=True)
    status_choices = (
        ('A', 'Active'),
        ('IA', 'Inactive')
    )
    status = models.CharField(max_length=2, choices=status_choices, default='IA')
    uploaded_doc = models.FileField(upload_to="documents/instruments/%Y/%m/%d", null=True, blank=True)

    def filename(self):
        return os.path.basename(self.file.name)


class CalibrationInfo(models.Model):
    instrument_info = models.ForeignKey(InstrumentInfo)
    calibration_test_name = models.CharField(max_length=100, unique=True)
    scheduled_at = models.DateField()
    interval = models.IntegerField()
    gross_day = models.IntegerField()


class CalibrationReport(models.Model):
    status_choices = (
        ('IP', 'In Progress'),
        ('C', 'Complete'),
    )
    status = models.CharField(max_length=2, choices=status_choices, default='IP')
    Permission_Choices = (
        ('Pen', 'Pending'),
        ('Apr', 'Approved'),
        ('Rej', 'Rejected'),
    )
    permission_status = models.CharField(max_length=3, choices=Permission_Choices, default='Pen')
    created_at = models.DateTimeField(auto_now_add=True)


class CalibrationTests(models.Model):
    calibration_report = models.ForeignKey(CalibrationReport)
    instrument_info = models.ForeignKey(InstrumentInfo)
    calibration_test_name = models.CharField(max_length=100)
    scheduled_at = models.DateField(null=True, blank=True)
    occurred_at = models.DateField(null=True, blank=True)
    gross_day = models.IntegerField()
    status_choices = (
        ('C', 'Complete'),
        ('IC', 'Incomplete')
    )
    status = models.CharField(max_length=2, choices=status_choices, default='IC')
    username = models.ForeignKey(Account, null=True, blank=True)


class Attachments(models.Model):
    calibration_tests = models.ForeignKey(CalibrationTests)
    uploaded_file = models.FileField(upload_to="documents/calibration/internal/%Y/%m/%d")


class NotifyCalibrationTests(models.Model):
    calibration_tests = models.ForeignKey(CalibrationTests)
