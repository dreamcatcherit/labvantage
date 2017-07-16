
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.datetime_safe import datetime
from lir.models import LabRequestForm, TestInfo, ProductInfo
from eims.models import CalibrationReport, CalibrationTests
from oap.models import OAPReport
from .models import Account
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages


@login_required
def home(request):
    current_report = CalibrationReport.objects.filter(status='IP')
    complete, incomplete = 0, 0
    completed_calibration_tests, incomplete_calibration_tests = None, None
    if current_report.exists():
        current_report = current_report[0]
        completed_calibration_tests = CalibrationTests.objects.filter(calibration_report=current_report,
                                                status="C")
        complete = completed_calibration_tests.count()
        incomplete_calibration_tests = CalibrationTests.objects.filter(calibration_report=current_report,status='IC')
        incomplete = incomplete_calibration_tests.count()

    oap = OAPReport.objects.all().prefetch_related('customer_contact', 'equipment_details')
    lrf = LabRequestForm.objects.all()
    pending_lrf = lrf.filter(permission_status='Pen')
    verified_lrf = lrf.filter(permission_status='Ver')
    approved_lrf = lrf.filter(permission_status='Apr')
    rejected_lrf = lrf.filter(permission_status='Rej')

    pending_oap = oap.filter(permission_status='Pen')
    verified_oap = oap.filter(permission_status='Ver')
    approved_oap = oap.filter(permission_status='Apr')
    rejected_oap = oap.filter(permission_status='Rej')

    lir = ProductInfo.objects.all()
    pending_lir = lir.filter(permission_status='Pen')
    verified_lir = lir.filter(permission_status='Ver')
    approved_lir = lir.filter(permission_status='Apr')
    rejected_lir = lir.filter(permission_status='Rej')
    num_of_lrf = lrf.count()
    num_of_lir = lir.count()
    data = {
        'oapPen': pending_oap.count(),
        'oapVer': verified_oap.count(),
        'oapApr': approved_oap.count(),
        'oapRej': rejected_oap.count(),
        'Pen': pending_lrf.count() + pending_lir.count(),
        'Ver': verified_lrf.count() + verified_lir.count(),
        'Apr': approved_lrf.count() + approved_lir.count(),
        'Rej': rejected_lrf.count() + rejected_lir.count(),
        'All': num_of_lir + num_of_lrf,
        'Per': 0 if (num_of_lrf + num_of_lir) == 0 else int(
            ((approved_lrf.count() + approved_lir.count()) * 100.00) / (num_of_lrf + num_of_lir)),
        'eqpC': complete,
        'eqpIC':incomplete,

    }

    # ["product_info__" + i.name for i in ProductInfo._meta.get_fields()]
    #  [ "lab_request_form__" + i.name for i in LabRequestForm._meta.get_fields()]
    temp = TestInfo.objects.prefetch_related('product_info')
    late_analysis = [i for i in temp
                     if i.product_info.lab_request_form.releasing_time < i.last_modified]
    return render(request, "base/dashboard.html", {
        'data': data,
        'pending': pending_lrf.order_by('releasing_time').values() if pending_lrf else None,
        'verified': verified_lrf.order_by('releasing_time').values() if verified_lrf else None,

        'recent': lir.prefetch_related('product_name__testinfo_set__product_info').order_by('updated_at').reverse() if lir else None,
        'oap_recent': oap.order_by('-last_modified').prefetch_related('customer_contact', 'equipment_details') if oap else None,
        'oap_approved': approved_oap.order_by('-last_modified') if approved_oap else None,
        'oap_pending': pending_oap.order_by('-last_modified') if pending_oap else None,
        'late': late_analysis,
        'completed_tests': completed_calibration_tests.order_by('scheduled_at') if completed_calibration_tests
        else None,
        'incomplete_tests': incomplete_calibration_tests.order_by('scheduled_at') if incomplete_calibration_tests else None,
        'current_tests': incomplete_calibration_tests.filter(scheduled_at__lte=datetime.now()).order_by('scheduled_at') if incomplete_calibration_tests else None,


    })  # TODO !!! optimize dashboard


@login_required
def create_user(request):
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_admin:
        if request.method == 'POST':
            acc = Account(username=request.POST.get('username'),
                          password=make_password(request.POST.get('password')))
            if request.POST.get('user_type') == 'S':
                acc.is_sampler = True
            elif request.POST.get('user_type') == 'LM':
                acc.is_lab_manager = True
            elif request.POST.get('user_type') == 'DLM':
                acc.is_deputy_lab_manager = True
            elif request.POST.get('user_type') == 'V':
                acc.is_verifier = True
            acc.save()
            messages.info(request, 'New User Created')
            return render(request, "base/create_user.html")
        return render(request, "base/create_user.html")
    return HttpResponse('Access Denied')


@login_required
def view_users(request):
    users = Account.objects.all()
    return render(request, "base/view_users.html", {'users': users.values()})
