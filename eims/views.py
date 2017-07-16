from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from eims.models import InstrumentInfo, CalibrationInfo, CalibrationReport, CalibrationTests, Attachments
import datetime
from dateutil.relativedelta import relativedelta
from eims.utils import get_random_color
from operator import itemgetter


@login_required
def add_new_instrument(request):
    if request.method == 'POST':
        if request.FILES:
            InstrumentInfo.objects.create(
                category_type=request.POST.get('category_type'),
                supplier=request.POST.get('supplier'),
                manufacturer=request.POST.get('manufacturer'),
                instrument_name=request.POST.get('instrument_name'),
                model_number=request.POST.get('model_number'),
                received_date=None if request.POST.get('received_date')=='' else request.POST.get('received_date'),
                installation_date=None if request.POST.get('installation_date') == '' else request.POST.get('installation_date'),
                po_date=None if request.POST.get('po_date') == '' else request.POST.get('po_date'),
                serial_number=request.POST.get('serial_number'),
                instrument_category= request.POST.get('instrument_category'),
                uploaded_doc=request.FILES['upload_file'],
            )
        else:
            InstrumentInfo.objects.create(
                category_type=request.POST.get('category_type'),
                supplier=request.POST.get('supplier'),
                manufacturer=request.POST.get('manufacturer'),
                instrument_name=request.POST.get('instrument_name'),
                model_number=request.POST.get('model_number'),
                received_date=None if request.POST.get('received_date') == '' else request.POST.get('received_date'),
                installation_date=None if request.POST.get('installation_date') == '' else request.POST.get(
                    'installation_date'),
                po_date=None if request.POST.get('po_date') == '' else request.POST.get('po_date'),
                serial_number=request.POST.get('serial_number'),
                instrument_category=request.POST.get('instrument_category'),
            )

        messages.info(request, 'New Instrument added')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'eims/add_new_instrument.html')


@login_required
def view_instrument(request):
    return render(request, 'eims/view_instrument.html')


@login_required
def view_instruments(request):
    instruments = InstrumentInfo.objects.all()
    return render(request, 'eims/view_instruments.html', {
        'instruments': instruments
    })


@login_required
def view_internal_reports(request):
    calibration_reports = CalibrationReport.objects.all()
    return render(request, 'eims/view_internal_reports.html', {
        'reports': calibration_reports
    })


@login_required
def view_internal_report(request, id):
    current_report = CalibrationReport.objects.get(id=id)
    calibration_tests = CalibrationTests.objects.filter(
            calibration_report=current_report
            ).prefetch_related(
                'calibration_report',
                'instrument_info'
            )
    test_colors = {}
    datasets = dict(enumerate([[], [], [], [], [], [], [], [], [], [], [], []], 1))
    for test in calibration_tests:
        if test.calibration_test_name not in test_colors:
            color = get_random_color()
            while color in test_colors:
                color = get_random_color()
            test_colors[test.calibration_test_name] = color
        datasets[test.scheduled_at.month].append([test.scheduled_at.day, test_colors[test.calibration_test_name]])
    for j in range(1, 13):
        if not datasets[j]:
            for i in range(1, 32):
                datasets[j].append([i, ''])
        else:
            numbers = []
            for x in datasets[j]:
                if x[0] not in numbers:
                    numbers.append(x[0])
            for i in range(1,32):
                if i not in numbers:
                    datasets[j].append([i,''])
            datasets[j] = sorted(datasets[j], key=itemgetter(0))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return render(request, 'eims/view_internal_report.html', {
        'id': id,
        'calibration_tests': calibration_tests,
        'datasets': zip(months, datasets.items()),
        'test_color': test_colors.items()
    })


@login_required
def view_calibration_tests(request):
    current_report = CalibrationReport.objects.filter(status='IP')
    if current_report.exists():
        if request.method == "POST":
            current_report = current_report[0]
            current_report.status = 'C'
            current_report.save()
            for obj in CalibrationInfo.objects.all():
                obj.scheduled_at = None
                obj.save()
            messages.info(request, 'Yearly Internal Calibration Completed Successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        calibration_tests = CalibrationTests.objects.filter(
            calibration_report=current_report
            ).prefetch_related(
                'calibration_report',
                'instrument_info'
            )
        test_colors = {}
        datasets = dict(enumerate([[], [], [], [], [], [], [], [], [], [], [], []], 1))
        for test in calibration_tests:
            if test.calibration_test_name not in test_colors:
                color = get_random_color()
                while color in test_colors:
                    color = get_random_color()
                test_colors[test.calibration_test_name] = color
            datasets[test.scheduled_at.month].append([test.scheduled_at.day, test_colors[test.calibration_test_name]])
        for j in range(1, 13):
            if not datasets[j]:
                for i in range(1, 32):
                    datasets[j].append([i, ''])
            else:
                numbers = []
                for x in datasets[j]:
                    if x[0] not in numbers:
                        numbers.append(x[0])
                for i in range(1,32):
                    if i not in numbers:
                        datasets[j].append([i,''])
                datasets[j] = sorted(datasets[j], key=itemgetter(0))
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return render(request, 'eims/view_calibration_tests.html', {
            'calibration_tests': calibration_tests,
            'datasets': zip(months, datasets.items()),
            'test_color': test_colors.items()
        })
    return render(request, 'eims/view_calibration_tests.html', {

    })


@login_required
def view_calibration_test(request, id):
    calibration_test = CalibrationTests.objects.get(id=id)
    if calibration_test.status == 'C':
        attachments = Attachments.objects.filter(calibration_tests=calibration_test)

        return render(request, 'eims/view_calibration_test.html', {
            'calibration_test': calibration_test,
            'attachments': attachments,

        })

    if request.method == 'POST':
        calibration_test.occurred_at = request.POST.get('occurred_at')
        calibration_test.username = request.user
        calibration_test.status = 'C'
        calibration_test.save()
        instrument = InstrumentInfo.objects.get(id=calibration_test.instrument_info_id)
        instrument.status = "A"
        instrument.save()
        if request.FILES:
            for file in request.FILES.getlist('upload_file'):
                Attachments.objects.create(
                    calibration_tests=calibration_test,
                    uploaded_file=file
                )
        messages.info(request, 'Calibration Test Completed Successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'eims/view_calibration_test.html', {
        'calibration_test': calibration_test,

    })


@login_required
def schedule_calibration_tests(request):
    calibration_tests = CalibrationInfo.objects.all()
    no_calibration_scheduled = not CalibrationReport.objects.filter(status='IP').exists()
    if request.method == 'POST':
        calibration_report_obj = CalibrationReport.objects.create()
        for obj in calibration_tests:
            instrument_info = obj.instrument_info
            calibration_test_name = obj.calibration_test_name
            interval = obj.interval
            gross_day = obj.gross_day

            schedule_dates = [obj.scheduled_at]
            date = obj.scheduled_at

            next_date = date + relativedelta(months=+interval)
            while next_date.year == date.year:
                schedule_dates.append(next_date)
                next_date += relativedelta(months=+interval)

            for date in schedule_dates:
                CalibrationTests.objects.create(
                    calibration_report=calibration_report_obj,
                    instrument_info=instrument_info,
                    calibration_test_name=calibration_test_name,
                    scheduled_at=date,
                    gross_day=gross_day
                )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'eims/schedule_calibration_tests.html', {
        'calibration_tests': calibration_tests,
        'no_calibration_scheduled': no_calibration_scheduled,
    })


@login_required
def add_calibration_info(request):
    instruments = InstrumentInfo.objects.all()
    if request.method == "POST":
        CalibrationInfo.objects.create(
            instrument_info=InstrumentInfo.objects.get(instrument_name=request.POST.get('select_instrument')),
            calibration_test_name=request.POST.get('calibration_test_name'),
            scheduled_at=request.POST.get('scheduled_at'),
            interval=request.POST.get('interval'),
            gross_day=request.POST.get('gross_day'),
        )
        messages.info(request, 'New Calibration Test added')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'eims/add_calibration_info.html', {
        'instruments': instruments,
    })


@login_required
def view_calibration_info(request, id):
    calibration_info = CalibrationInfo.objects.get(id=id)
    if request.method == "POST":
        calibration_info.scheduled_at=request.POST.get('scheduled_at')
        calibration_info.interval=request.POST.get('interval')
        calibration_info.gross_day=request.POST.get('gross_day')
        calibration_info.save()
        messages.info(request, 'Calibration Test Info has been modified')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'eims/view_calibration_info.html', {
        'calibration_info': calibration_info,
    })


