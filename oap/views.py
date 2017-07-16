from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import CustomerContact, EquipmentDetails, ElementalAnalysisTests, OilAnalysisTests
from oap.models import OAPReport, OilAnalysis, ElementalAnalysis, ProgressiveAnalysis
from base.models import Account
from django.utils import timezone
from itertools import zip_longest
from oap.utils import oap_make_json as make_json


@login_required
def create_new_oap(request):
    detect_user = Account.objects.get(id=request.user.id)
    if detect_user.is_sampler:
        if request.method == "POST":
            progressive_analysis_obj = ProgressiveAnalysis.objects.create()
            customer = CustomerContact.objects.get(customer_name=request.POST.get('customer_name'))
            equipment = EquipmentDetails.objects.get(equipment_number=request.POST.get('equipment_number'))
            oap_obj = OAPReport.objects.create(
                customer_contact=customer,
                equipment_details=equipment,
                progressive_analysis=progressive_analysis_obj,
                permission_status="Ini",
            )
            oil_analysis_tests = request.POST.getlist('oil_analysis_tests')
            elemental_analysis_tests = request.POST.getlist('elemental_analysis_tests')
            for test in oil_analysis_tests:
                OilAnalysis.objects.create(
                    oap_report=oap_obj,
                    test_name=test,
                    user_id=OilAnalysisTests.objects.get(test_name=test).user_id
                )
            for test in elemental_analysis_tests:
                ElementalAnalysis.objects.create(
                    oap_report=oap_obj,
                    test_name=test,
                    user_id=ElementalAnalysisTests.objects.get(test_name=test).user_id
                )
            request.method = 'GET'
            return view_oap_report(request, oap_obj.id)

    return render(request, 'oap/create_new_oap.html', {
        'customers': CustomerContact.objects.all(),
        'equipments':  EquipmentDetails.objects.all(),
        'eatests': ElementalAnalysisTests.objects.all(),
        'oatests': OilAnalysisTests.objects.all(),

    })


@login_required
def view_oap_reports(request):
    return render(request, 'oap/view_oap_reports.html', {
        'oap_reports': OAPReport.objects.all().prefetch_related(
            'progressive_analysis',
            'customer_contact',
            'equipment_details'
            ),
    })


@login_required
def view_oap_report(request, id):
    oap_obj = OAPReport.objects.get(id=id)
    customer = oap_obj.customer_contact
    equipment = oap_obj.equipment_details
    user = Account.objects.get(id=request.user.id)
    if user.is_sampler:
        if request.method == "POST":
            permission_status = request.POST.get('permission_status')
            progressive_analysis = ProgressiveAnalysis.objects.get(oapreport=oap_obj)
            progressive_analysis.date_sampled = None if request.POST.get('date_sampled') == '' \
                else request.POST.get('date_sampled')
            progressive_analysis.date_received = None if request.POST.get('date_received') == '' \
                else request.POST.get('date_received')
            progressive_analysis.lab_number = request.POST.get('lab_number')
            progressive_analysis.oil_life = request.POST.get('oil_life')
            progressive_analysis.component_life = request.POST.get('component_life')
            progressive_analysis.filter_life = request.POST.get('filter_life')
            progressive_analysis.daily_top_up = request.POST.get('daily_top_up')
            progressive_analysis.oil_changed = request.POST.get('oil_changed')
            progressive_analysis.date_of_oil_renewed = None if \
                request.POST.get('date_of_oil_renewed') == '' else request.POST.get('date_of_oil_renewed')
            progressive_analysis.sump_capacity = request.POST.get('sump_capacity')
            progressive_analysis.reservoir_temperature = request.POST.get('reservoir_temperature')
            progressive_analysis.oil_in = request.POST.get('oil_in')
            progressive_analysis.oil_out = request.POST.get('oil_out')
            progressive_analysis.coolant_in = request.POST.get('coolant_in')
            progressive_analysis.coolant_out = request.POST.get('coolant_out')
            progressive_analysis.save()
            oap_obj.permission_status = permission_status
            oap_obj.save()
        return render(request, 'oap/view_oap_sampler.html', {
        'customer': customer,
        'equipment': equipment,
        'oap_report': oap_obj,
        })
    elif user.is_verifier:
        oatests = OilAnalysis.objects.filter(oap_report=oap_obj, user_id=user.id)
        eatests = ElementalAnalysis.objects.filter(oap_report=oap_obj, user_id=user.id)
        if request.method == 'POST':
            results = []
            for test, result in zip(oatests, request.POST.getlist('oaresult')):
                test.result = result
                test.save()
            for test, result in zip(eatests, request.POST.getlist('earesult')):
                test.result = result
                test.save()

            for ob in OilAnalysis.objects.filter(oap_report=oap_obj):
                result = ob.result
                if result == 'None' or (result is None) or result == '':
                    results.append(result)
            for ob in ElementalAnalysis.objects.filter(oap_report=oap_obj):
                result = ob.result
                if result == 'None' or (result is None) or result == '':
                    results.append(result)
            if not results:
                oap_obj.permission_status = 'Ver'
                pa = ProgressiveAnalysis.objects.get(oapreport=oap_obj)
                pa.date_reported = timezone.now()
                pa.save()
            oap_obj.comment = request.POST.get('comment')
            oap_obj.save()
        return render(request, 'oap/view_oap_verifier.html', {
            'customer': customer,
            'equipment': equipment,
            'oap_report': oap_obj,
            "oatests": oatests,
            'eatests': eatests,
        })
    else:
        if request.method == 'POST':
            oap_obj.permission_status = request.POST.get('permission_status')
            oap_obj.save()
        oatests = OilAnalysis.objects.filter(oap_report=oap_obj)
        eatests = ElementalAnalysis.objects.filter(oap_report=oap_obj)
        permission_status = oap_obj.permission_status
        if permission_status == 'Apr':
            previous_samples = OAPReport.objects.filter(
                customer_contact=customer,
                equipment_details=equipment,
                permission_status='Apr',
                progressive_analysis__date_reported__lt=oap_obj.progressive_analysis.date_reported
            ).order_by('progressive_analysis__date_reported')[:4][::-1]
            ots = list()
            ots.append(list(OilAnalysis.objects.filter(oap_report=oap_obj)))
            ets = list()
            ets.append(list(ElementalAnalysis.objects.filter(oap_report=oap_obj)))
            temp = [ProgressiveAnalysis.objects.filter(oapreport=oap_obj).values()[0], {}, {}, {}, {}]
            for pos, obj in enumerate(previous_samples):
                temp[pos+1] = ProgressiveAnalysis.objects.filter(oapreport=obj).values()[0]
                ots.append(list(OilAnalysis.objects.filter(oap_report=obj)))
                ets.append(ElementalAnalysis.objects.filter(oap_report=obj))
            data = []
            for key, value in temp[0].items():
                if value is not None and value != "None":
                    data.append((key, value, temp[1].get(key), temp[2].get(key), temp[3].get(key), temp[4].get(key)))
            return render(request, 'oap/view_oap_report.html', {
                "oatests": zip_longest(*ots),
                'eatests': zip_longest(*ets),
                'customer': customer,
                'equipment': equipment,
                'data': data,
                'oap_report': oap_obj,
                'ea_chart_data': make_json(data, zip_longest(*ets)),
                'oa_chart_data': make_json(data, zip_longest(*ots)),

            })
        else:
            return render(request, 'oap/view_oap_report.html', {
                "oatests": oatests,
                'eatests': eatests,
                'customer': customer,
                'equipment': equipment,
                'oap_report': oap_obj,
            })