import random
from django.utils.datetime_safe import datetime
from eims.models import CalibrationReport, CalibrationTests, InstrumentInfo


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


def check_internal():
    in_progress = CalibrationReport.objects.filter(status='IP')
    if in_progress.exists():
        for obj in in_progress:
            for mi_obj in CalibrationTests.objects.filter(calibration_report=obj,
                    scheduled_at__lt=datetime.today(),
                    status='IC'
            ):
                inactive_instrument = InstrumentInfo.objects.get(id=mi_obj.instrument_info.id)
                inactive_instrument.status = 'IA'
                inactive_instrument.save()

    return True
