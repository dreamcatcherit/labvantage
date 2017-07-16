from itertools import zip_longest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from inventory.models import CustomerContact, EquipmentDetails, ElementalAnalysisTests, OilAnalysisTests
from oap.models import OAPReport, OilAnalysis, ElementalAnalysis, ProgressiveAnalysis
from oap.utils import oap_make_json as make_json


@login_required
def trend(request):
    customers = CustomerContact.objects.all()
    equipments = EquipmentDetails.objects.all()
    oatests = OilAnalysisTests.objects.all().only('test_name').values()
    eatests = ElementalAnalysisTests.objects.all().only('test_name').values()
    if request.method == "POST" and 'oa_button' in request.POST:
        customer = CustomerContact.objects.get(id=request.POST.get('customer'))
        equipment = EquipmentDetails.objects.get(id=request.POST.get('equipment'))
        previous_samples = OAPReport.objects.filter(
            customer_contact=customer,
            equipment_details=equipment,
            permission_status='Apr',
            ).order_by('progressive_analysis__date_reported')[::-1]
        ots = list()
        temp = []
        for pos, obj in enumerate(previous_samples):
            temp.append(ProgressiveAnalysis.objects.filter(oapreport=obj).values()[0])
            ots.append(OilAnalysis.objects.filter(
                oap_report=obj,
                test_name__in=request.POST.getlist('oatests')
            ))
        data = []
        if temp:
            for key, value in temp[0].items():
                if value is not None and value != "None":
                    data.append((key, value, temp[1].get(key), temp[2].get(key), temp[3].get(key), temp[4].get(key)))
        return render(request, 'trend/trend.html', {
            'customers': customers,
            'equipments': equipments,
            'eatests': eatests,
            'oatests': OilAnalysisTests.objects.filter(test_name__in=request.POST.getlist('oatests')),
            'chart_data': make_json(data, zip_longest(*ots)),
            'chart_data_ea': 0,

        })
    elif request.method == "POST" and 'ea_button' in request.POST:
        customer = CustomerContact.objects.get(id=request.POST.get('customer'))
        equipment = EquipmentDetails.objects.get(id=request.POST.get('equipment'))
        previous_samples = OAPReport.objects.filter(
            customer_contact=customer,
            equipment_details=equipment,
            permission_status='Apr',
        ).order_by('progressive_analysis__date_reported')[::-1]
        ets = list()
        temp = []
        for pos, obj in enumerate(previous_samples):
            temp.append(ProgressiveAnalysis.objects.filter(oapreport=obj).values()[0])
            ets.append(ElementalAnalysis.objects.filter(
                oap_report=obj,
                test_name__in=request.POST.getlist('eatests')
            ))
        data = []
        for key, value in temp[0].items():
            if value is not None and value != "None":
                data.append((key, value, temp[1].get(key), temp[2].get(key), temp[3].get(key), temp[4].get(key)))
        return render(request, 'trend/trend.html', {
            'customers': customers,
            'equipments': equipments,
            'eatests': ElementalAnalysisTests.objects.filter(
                test_name__in=request.POST.getlist('eatests')
            ),
            'oatests': oatests,
            'chart_data': 0,
            'chart_data_ea': make_json(data, zip_longest(*ets)),

        })

    return render(request, 'trend/trend.html', {
        'customers': customers,
        'equipments': equipments,
        'oatests': oatests,
        'eatests': eatests,

    })
