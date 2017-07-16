from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from inventory.models import ProductName, TestName, ProductTestList, CustomerContact, EquipmentDetails, ElementalAnalysisTests, OilAnalysisTests
from django.db import IntegrityError
from django.contrib import messages
from base.models import Account


@login_required
def add_new_product(request):
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_lab_manager or detect_user.is_deputy_lab_manager:
        if request.method == "POST":
            try:
                ProductName.objects.create(product_name=request.POST.get('product_name'))
                messages.info(request, 'new product added')
            except IntegrityError:
                messages.info(request, "product already exist", extra_tags='alert alert-error')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, "inventory/add_new_product.html")
    return HttpResponse('<h1>ERROR 403: Access Denied, Wanna <a href="/logout">logout?</a></h1>')


@login_required
def add_new_test(request):
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_lab_manager or detect_user.is_deputy_lab_manager:
        if request.method == "POST":
            try:
                TestName.objects.create(
                    test_name=request.POST.get('test_name'),
                    user_id=Account.objects.get(username=request.POST.get('username')),
                )

                messages.info(request, 'new test added')
            except IntegrityError:
                messages.info(request, "Test already exist and assigned",extra_tags='alert alert-error')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        verifiers = Account.objects.filter(is_verifier=True)
        return render(request, "inventory/add_new_test.html", {"verifiers": verifiers})
    return HttpResponse('<h1>ERROR 403: Access Denied, Wanna <a href="/logout">logout?</a></h1>')


@login_required
def add_test_info(request):
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_lab_manager or detect_user.is_deputy_lab_manager:
        if request.method == "POST":
            product_name_obj = ProductName.objects.get(product_name=request.POST.get('product_name'))
            test_name_obj = TestName.objects.get(test_name=request.POST.get('test_name'))
            product_list_object = ProductTestList(
                    product_name=product_name_obj,
                    test_name=test_name_obj,
                    method=request.POST.get('method'),
                    unit=request.POST.get('unit'),
                    mins=request.POST.get('mins'),
                    maxs=request.POST.get('maxs'),
                    typical=request.POST.get('typical'),
                    )
            product_list_object.save()
            messages.info(request, 'product test info added')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Access denied')  # TODO better error handling
    products = ProductName.objects.all()
    tests = TestName.objects.all()
    return render(request, "inventory/add_test_info.html", {'products': products, 'tests': tests})


@login_required
def view_products(request):
    products = ProductName.objects.all()
    return render(request, "inventory/view_products.html", {'products': products})


@login_required
def view_tests(request):
    tests = TestName.objects.prefetch_related('user_id')
    return render(request, "inventory/view_tests.html", {'tests': tests})

@login_required
def view_products_test_list(request):
    products = ProductTestList.objects.prefetch_related('test_name', 'product_name', 'test_name__user_id')
    return render(request, "inventory/view_products_test_list.html", {'products': products})


@login_required
def add_new_customer(request):
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_sampler:
        if request.method == "POST":
            try:
                CustomerContact.objects.create(
                    customer_name=request.POST.get('customer_name'),
                    customer_address=request.POST.get('customer_address'),
                    customer_contacts_name=request.POST.get('customer_contacts_name'),
                    customer_contact=request.POST.get('customer_contact'),
                    reference_contact_name=request.POST.get('reference_contact_name'),
                    reference_contact=request.POST.get('reference_contact'),
                )
                messages.info(request, 'new customer added')
            except IntegrityError:
                messages.info(request, "customer already exist", extra_tags='alert alert-error')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, "inventory/add_new_customer.html")
    return HttpResponse('<h1>ERROR 403: Access Denied, Wanna <a href="/logout">logout?</a></h1>')


@login_required
def view_customers(request):
    contacts = CustomerContact.objects.all()
    return render(request, "inventory/view_customer_contacts.html", {'contacts': contacts})


@login_required
def view_customer(request, id):
    contact = CustomerContact.objects.get(id=id)
    return render(request, "inventory/add_new_customer.html", {'view_contact': True, 'contact': contact})


@login_required
def add_new_equipment(request):
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_sampler:
        if request.method == "POST":
            try:
                EquipmentDetails.objects.create(
                    equipment_number=request.POST.get('equipment_number'),
                    equipment_model=request.POST.get('equipment_model'),
                    equipment_make=request.POST.get('equipment_make'),
                    component=request.POST.get('component'),
                    component_make=request.POST.get('component_make'),
                    component_model=request.POST.get('component_model'),
                    serial_number=request.POST.get('serial_number'),
                    lube_oil=ProductName.objects.get(product_name=request.POST.get('lube_oil')),
                    capacity=request.POST.get('capacity'),
                )
                messages.info(request, 'new equipment added')
            except IntegrityError:
                messages.info(request, "equipment already exist", extra_tags='alert alert-error')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, "inventory/add_new_equipment.html", {'products': ProductName.objects.all()})
    return HttpResponse('<h1>ERROR 403: Access Denied, Wanna <a href="/logout">logout?</a></h1>')


@login_required
def view_equipments(request):
    equipments = EquipmentDetails.objects.all()
    return render(request, "inventory/view_equipments.html", {'equipments': equipments})


@login_required
def view_equipment(request, id):
    equipment = EquipmentDetails.objects.get(id=id)
    return render(request, "inventory/add_new_equipment.html", {'view_equipment': True, 'equipment': equipment})


@login_required
def add_new_oap_test(request):
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_deputy_lab_manager or detect_user.is_lab_manager:
        if request.method == "POST":
            if request.POST.get('test_type') == 'EA':
                try:
                    ElementalAnalysisTests.objects.create(
                        test_name=request.POST.get('test_name'),
                        user_id=Account.objects.get(id=request.POST.get('user_id')),
                    )
                    messages.info(request, 'new Elemental Analysis Test added')
                except IntegrityError:
                    messages.info(request, "Test already exists!", extra_tags='alert alert-error')
            else:
                try:
                    OilAnalysisTests.objects.create(
                        test_name=request.POST.get('test_name'),
                        user_id=Account.objects.get(id=request.POST.get('user_id')),
                    )
                    messages.info(request, 'new Oil Analysis Test added')
                except IntegrityError:
                    messages.info(request, "Test already exists!", extra_tags='alert alert-error')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return render(request, "inventory/add_new_oap_report_field.html", {
            'testers': Account.objects.filter(is_verifier='True')
        })
    return HttpResponse('<h1>ERROR 403: Access Denied, Wanna <a href="/logout">logout?</a></h1>')


@login_required
def view_oap_tests(request):
    eatests = ElementalAnalysisTests.objects.all()
    oatests = OilAnalysisTests.objects.all()
    return render(request, "inventory/view_oap_tests.html", {'EATests': eatests, 'OATests': oatests})
