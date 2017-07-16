from django.shortcuts import render
from lir.models import LabRequestForm, ProductInfo, TestInfo, ReleaseCertificateInfo
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from inventory.models import ProductName, TestName, ProductTestList
from base.models import Account
from .forms import ProductInfoForm
# Create your views here.


@login_required
def create_new_lrf(request):
    """
    Detect authorized user and redirect to their own template
    :param request:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    product_name = ProductName.objects.all()
    if detect_user.is_sampler:
        return render(request, "lir/sampler.html", {'product_name': product_name})
    elif detect_user.is_lab_manager or detect_user.is_deputy_lab_manager:
        verified_data = LabRequestForm.objects.filter(permission_status='Ver')
        return render(request, 'lir/lab_manager.html', {'verified_data': verified_data, 'product_name': product_name})
    elif detect_user.is_verifier:
        pending_data = LabRequestForm.objects.filter(permission_status='Pen')
        return render(request, "lir/verifier.html", {'pending_data': pending_data, 'product_name': product_name})
    return HttpResponse('Access denied')  # TODO better response


@login_required
def sampler(request):
    """
    View for sampler's save form
    :param request:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_sampler:
        if request.method == "POST":
            prod_name = ProductName.objects.get(product_name=request.POST.get('product_name'))
            obj = LabRequestForm(product_name=prod_name, ref_no=request.POST.get('ref_no'), date=request.POST.get('date'),
                                 batch_number=request.POST.get('batch_number'),
                                 sampling_time=request.POST.get('sampling_time'),
                                 lab_test_number=request.POST.get('lab_test_number'),
                                 sample_receiving_time=request.POST.get('sample_receiving_time'),
                                 sample_source=request.POST.get('sample_source'),
                                 tank_number=request.POST.get('tank_number'),
                                 batch_quantity=request.POST.get('batch_quantity'),
                                 formulation_number=request.POST.get('formulation_number'),
                                 sample_type=request.POST.get('sample_type'),
                                 releasing_time=request.POST.get('releasing_time')
                                 )
            obj.save()
            messages.info(request, 'Data Saved')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif request.method == 'GET':
            product_name = ProductName.objects.all()
            return render(request, 'lir/create_new_lrf.html', {'product_name': product_name})
    else:
        return HttpResponse('Access denied')  # TODO better error handling


@login_required
def sampler_pending_list(request, slug=None):
    """
    Shows pending data to sampler
    :param request:
    :param slug:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_sampler:
        if request.method == 'GET':
            product_name = ProductName.objects.all()
            pending_data = LabRequestForm.objects.filter(permission_status='Pen')
            return render(request, 'lir/sampler_pending_list.html', {'pending_data': pending_data, 'product_name': product_name})
        elif request.method == 'POST':     # such code much wow :D
            updated_data = LabRequestForm.objects.get(id=slug)
            updated_data.product_name = ProductName.objects.get(product_name=request.POST.get('product_name'))
            updated_data.ref_no = request.POST.get('ref_no')
            updated_data.date = request.POST.get('date')
            updated_data.batch_number = request.POST.get('batch_number')
            updated_data.sampling_time = request.POST.get('sampling_time')
            updated_data.lab_test_number = request.POST.get('lab_test_number')
            updated_data.sample_receiving_time = request.POST.get('sample_receiving_time')
            updated_data.sample_source = request.POST.get('sample_source')
            updated_data.tank_number = request.POST.get('tank_number')
            updated_data.batch_quality = request.POST.get('batch_quality')
            updated_data.formulation_number = request.POST.get('formulation_number')
            updated_data.sample_type = request.POST.get('sample_type')
            updated_data.releasing_time = request.POST.get('releasing_time')
            updated_data.save()
            messages.info(request, 'Data Updated')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('Access denied')


@login_required
def sampler_approved_list(request):
    """
    Shows approved data to sampler
    :param request:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_sampler:
        product_name = ProductName.objects.all()
        approved_data = LabRequestForm.objects.filter(permission_status='Apr')
        return render(request, 'lir/sampler_approved_list.html', {'approved_data': approved_data,
                                                                  'product_name': product_name})
    return HttpResponse('Access denied')


@login_required
def verifier_list(request):
    """
    Shows verified data to verifier
    :param request:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_verifier:
        product_name = ProductName.objects.all()
        verified_list = LabRequestForm.objects.filter(permission_status='Ver')
        return render(request, 'lir/verified_list.html', {'verified_list': verified_list, 'product_name': product_name})
    return HttpResponse('Access denied')


@login_required
def lab_manager_list(request):
    """
    Shows approved data to lab manager or deputy lab manager
    :param request:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_lab_manager or detect_user.is_deputy_lab_manager:
        product_name = ProductName.objects.all()
        approved_list = LabRequestForm.objects.filter(permission_status='Apr')
        return render(request, 'lir/lab_manager_list.html', {'approved_list': approved_list, 'product_name': product_name})
    return HttpResponse('Access denied')


@login_required
def lab_manager(request, slug):
    """
    Saves lab manager's edit form
    :param request:
    :param slug:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_lab_manager or detect_user.is_deputy_lab_manager:
        if request.method == 'POST':
            pending_data = LabRequestForm.objects.get(id=slug)
            pending_data.product_name = ProductName.objects.get(product_name=request.POST.get('product_name'))
            pending_data.ref_no = request.POST.get('ref_no')
            pending_data.date = request.POST.get('date')
            pending_data.batch_number = request.POST.get('batch_number')
            pending_data.sampling_time = request.POST.get('sampling_time')
            pending_data.lab_test_number = request.POST.get('lab_test_number')
            pending_data.sample_receiving_time = request.POST.get('sample_receiving_time')
            pending_data.sample_source = request.POST.get('sample_source')
            pending_data.tank_number = request.POST.get('tank_number')
            pending_data.batch_quality = request.POST.get('batch_quality')
            pending_data.formulation_number = request.POST.get('formulation_number')
            pending_data.sample_type = request.POST.get('sample_type')
            pending_data.releasing_time = request.POST.get('releasing_time')
            pending_data.comments = request.POST.get('comments')
            pending_data.permission_status = request.POST.get('permission_status')
            pending_data.save()
            if pending_data.permission_status == 'Apr':
                ProductInfo(lab_request_form=pending_data).save()
            messages.info(request, 'Data saved.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse('Access denied')  # TODO better error handling
    return HttpResponse('Access denied')


@login_required
def verifier(request, slug):
    """
    Saves verifier's edit form
    :param request:
    :param slug:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_verifier:
        if request.method == 'POST':
            approved_data = LabRequestForm.objects.get(id=slug)
            approved_data.product_name = ProductName.objects.get(product_name=request.POST.get('product_name'))
            approved_data.ref_no = request.POST.get('ref_no')
            approved_data.date = request.POST.get('date')
            approved_data.batch_number = request.POST.get('batch_number')
            approved_data.sampling_time = request.POST.get('sampling_time')
            approved_data.lab_test_number = request.POST.get('lab_test_number')
            approved_data.sample_receiving_time = request.POST.get('sample_receiving_time')
            approved_data.sample_source = request.POST.get('sample_source')
            approved_data.tank_number = request.POST.get('tank_number')
            approved_data.batch_quality = request.POST.get('batch_quality')
            approved_data.formulation_number = request.POST.get('formulation_number')
            approved_data.sample_type = request.POST.get('sample_type')
            approved_data.releasing_time = request.POST.get('releasing_time')
            approved_data.comments = request.POST.get('comments')
            approved_data.permission_status = request.POST.get('permission_status')
            approved_data.save()
            messages.info(request, 'Data saved.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse('GET is denied')  # TODO better error handling
    return HttpResponse('Access denied')


@login_required
def select_report(request):
    """
    Select product name view for report
    :param request:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_sampler:
        product_name = ProductName.objects.all()
        return render(request, 'lir/report.html', {'product_name': product_name})


@login_required
def report(request, slug):
    """
    Report generate
    :param request:
    :param slug:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_sampler:
        product_name = ProductName.objects.get(product_name=slug)
        reports = ProductTestList.objects.filter(product_name=product_name)
        return render(request, 'lir/selected_report.html', {'product_name': product_name, 'reports': reports})


@login_required
def report_save(request):
    """
    Save sampler's report input data
    :param request:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_sampler:
        if request.method == 'POST':
            product_name = ProductName.objects.get(product_name=request.POST.get('product_name'))
            product_info = ProductInfo.objects.get(id=request.POST.get('id'))
            product_info.product_name = product_name
            product_info.batch_number = request.POST.get('batch_number')
            product_info.sample_number = request.POST.get('sample_number')
            product_info.test_type = request.POST.get('test_type')
            product_info.serial_number = request.POST.get('serial_number')
            product_info.tank_number = request.POST.get('tank_number')
            product_info.batch_size = request.POST.get('batch_size')
            product_info.date_tested = request.POST.get('date_tested')
            product_info.time_in_date = request.POST.get('time_in_date')
            product_info.time_out_date = request.POST.get('time_out_date')
            product_info.blending_date = request.POST.get('blending_date')
            product_info.initial = True
            product_info.save()
            methods = request.POST.getlist('table_method')
            units = request.POST.getlist('table_unit')
            test_names = request.POST.getlist('table_test_name')
            min_s = request.POST.getlist('table_mins')
            max_s = request.POST.getlist('table_maxs')
            typicals = request.POST.getlist('table_typical')
            for method, unit, mins, maxs, typical, test_name in zip(methods, units, min_s, max_s, typicals, test_names):
                TestInfo.objects.create(product_info=product_info,
                                        product_name=product_name,
                                        test_name=TestName.objects.get(test_name=test_name),
                                        method=method,
                                        unit=unit,
                                        mins=mins,
                                        maxs=maxs,
                                        typical=typical
                                        )
            messages.info(request, 'Data Saved')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# @login_required
# def report_save(request):
#     """
#     Save sampler's report input data
#     :param request:
#     :return:
#     """
#     detect_user = Account.objects.get(id=request.user.id)
#     if detect_user.is_sampler:
#         if request.method == 'POST':
#             product_name = ProductName.objects.get(product_name=request.POST.get('product_name'))
#             product_info = ProductInfo.objects.get(id=request.POST.get('id'))
#             product_info_form = ProductInfoForm(request.POST, instance=product_info)
#             product_info_form_obj = product_info_form.save(commit=False)
#             product_info_form_obj.product_name = product_name
#             product_info_form_obj.initial = True
#             if product_info_form_obj.is_valid():
#                 product_info_form_obj.save()
#                 methods = request.POST.getlist('table_method')
#                 units = request.POST.getlist('table_unit')
#                 test_names = request.POST.getlist('table_test_name')
#                 min_s = request.POST.getlist('table_mins')
#                 max_s = request.POST.getlist('table_maxs')
#                 typicals = request.POST.getlist('table_typical')
#                 for method, unit, mins, maxs, typical, test_name in zip(methods, units, min_s, max_s, typicals,
#                                                                         test_names):
#                     TestInfo.objects.create(product_info=product_info,
#                                             product_name=product_name,
#                                             test_name=TestName.objects.get(test_name=test_name),
#                                             method=method,
#                                             unit=unit,
#                                             mins=mins,
#                                             maxs=maxs,
#                                             typical=typical
#                                             )
#                 messages.info(request, "Data Saved")
#             else:
#                 messages.error(request, "Form is not valid")
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def report_verify(request):
    """
    Show pending report to verifier
    :param request:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_verifier:
        test_info = TestInfo.objects.filter(test_name__user_id=detect_user)
        return render(request, 'lir/verified_report.html', {'test_info': test_info})
    else:
        return HttpResponse('Access Denied')


@login_required
def report_verify_save(request):
    """
    Verify pending report
    :param request:
    :return:
    """
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_verifier:
        if request.method == 'POST':
            pks = request.POST.getlist('table_id')
            results = request.POST.getlist('table_result')
            for pk, result in zip(pks, results):
                test_info = TestInfo.objects.get(id=pk)
                test_info.result = result
                test_info.sign = detect_user
                test_info.save()
                filtered = [i. result for i in TestInfo.objects.filter(product_info__batch_number=test_info.product_info.batch_number)]
                if (None not in filtered) and ('' not in filtered):
                    prod = ProductInfo.objects.get(id=test_info.product_info.id)
                    prod.permission_status = 'Ver'
                    prod.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse('Access Denied')


@login_required
def report_approved_save(request):
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_lab_manager or detect_user.is_deputy_lab_manager:
        if request.method == 'POST':
            product_info = ProductInfo.objects.get(id=request.POST.get('product_id'))
            product_info.permission_status = request.POST.get('permission_status')
            product_info.save()
            if product_info.permission_status == "Apr":
                return render(request, 'lir/release_certificate.html', {'report': product_info, 'initial': True})
            else:
                request.method = 'GET'
                return view_lir(request)


@login_required
def view_lrf(request):
    lrf_data = LabRequestForm.objects.all()
    return render(request, 'lir/view_lrf.html', {'lrf_data': lrf_data})


@login_required
def pending(request):
    pending_data = LabRequestForm.objects.filter(permission_status="Pen")
    return render(request, 'lir/view_lrf.html', {'lrf_data': pending_data})


@login_required
def verified(request):
    verified_data = LabRequestForm.objects.filter(permission_status="Ver")
    return render(request, 'lir/view_lrf.html', {'lrf_data': verified_data})


@login_required
def approved(request):
    """
    Show all approved data
    :param request:
    :return:
    """
    approved_data = LabRequestForm.objects.filter(permission_status="Apr")
    return render(request, 'lir/view_lrf.html', {'lrf_data': approved_data})


@login_required
def rejected(request):
    """
    Show all rejected data
    :param request:
    :return:
    """
    rejected_data = LabRequestForm.objects.filter(permission_status="Rej")
    return render(request, 'lir/view_lrf.html', {'lrf_data': rejected_data})


@login_required
def reference_number(request, slug):
    detect_user = Account.objects.get(id=request.user.id)
    report = LabRequestForm.objects.get(ref_no=slug)
    product_name = ProductName.objects.all()
    if detect_user.is_verifier:
        return render(request, 'lir/verifier_lrf.html', {'product_name': product_name, 'report': report})
    elif detect_user.is_sampler:
        return render(request, 'lir/sampler_lrf.html', {'product_name': product_name, 'report': report})
    elif detect_user.is_lab_manager or detect_user.is_deputy_lab_manager:
        return render(request, 'lir/lab_manager_lrf.html', {'product_name': product_name, 'report': report})
    return HttpResponse('Access Denied')


@login_required
def view_lir(request):
    lir_data = ProductInfo.objects.all()
    return render(request, 'lir/view_lir.html', {'lir_data': lir_data})


@login_required
def view_lir_by_id(request, pk):
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_sampler:
        lir = ProductInfo.objects.get(id=pk)
        product_test_list = ProductTestList.objects.filter(product_name=lir.lab_request_form.product_name)
        return render(request, 'lir/create_new_lir.html', {'lir': lir, 'product_test_list': product_test_list})
    elif detect_user.is_verifier:
        lir = ProductInfo.objects.get(id=pk)
        test_info = TestInfo.objects.filter(product_info__id=pk, test_name__user_id=detect_user)
        return render(request, 'lir/verifier_lir.html', {'lir': lir, 'test_info': test_info})
    elif detect_user.is_deputy_lab_manager or detect_user.is_lab_manager:
        lir = ProductInfo.objects.get(id=pk)
        test_info = TestInfo.objects.filter(product_info__id=pk)
        return render(request, 'lir/lab_manager_lir.html', {'lir': lir, 'test_info': test_info, "product_id": pk})
    return HttpResponse('Access denied')


@login_required
def release(request):
    user = Account.objects.get(id=request.user.id)
    if user.is_lab_manager:

        ReleaseCertificateInfo.objects.create(
            product_name=request.POST.get('product_name'),
            sample_source=request.POST.get('sample_source'),
            batch_number=request.POST.get('batch_number'),
            sampling_time=request.POST.get('sampling_time'),
            sample_tested=request.POST.get('sample_tested'),
            filling_weight_calculations=request.POST.get('filling_weight_calculations'),
            head_of_qa=request.POST.get('head_of_qa')
        )
        release_certificates = ReleaseCertificateInfo.objects.all()
        return render(request, 'lir/view_released.html', {'released': release_certificates})
    return HttpResponse('Error 403: You are not Authorized to see this page!')


@login_required
def view_released(request):
    released = ReleaseCertificateInfo.objects.all()
    return render(request, 'lir/view_released.html', {'released': released})


@login_required
def view_release_certificate(request, id):
    data = ReleaseCertificateInfo.objects.get(id=id)
    return render(request, 'lir/release_certificate.html', {'report': data, 'initial': False})
