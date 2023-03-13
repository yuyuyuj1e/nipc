from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models.functions import TruncMonth, TruncYear
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from home.models import Vul

import json

# Create your views here.
from home.utils.pagination import Pagination


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def custom(request):
    return render(request, 'custom.html')


def report(request):
    return render(request, 'report.html')


def statistic(request):
    year_volume = Vul.objects.annotate(year=TruncYear('publishtime')).values('year').annotate(
        c=Count('id')).order_by('-year')[:20:-1]
    year_volume = [[i['year'].strftime('%y'), i['c']] for i in year_volume]
    year = [[i[0]] for i in year_volume]

    # 漏洞数量
    volumes = (
        Vul.objects
            .annotate(month=TruncMonth('publishtime'))
            .values('month', 'level')
            .annotate(c=Count('id'))
            .order_by('-month')[:48:-1]
    )
    volumes.reverse()

    temp_map = {}
    for item in volumes:
        if item['month'].strftime('%y-%m') not in temp_map.keys():
            if len(temp_map.keys()) == 12:
                break
            else:
                temp_map[item['month'].strftime('%y-%m')] = [0, 0, 0, 0]

        temp_map[item['month'].strftime('%y-%m')][item['level']] = item['c']

    date = []
    high = []
    middle = []
    low = []
    unknown = []
    for item in temp_map:
        date.append(item)
        unknown.append(temp_map[item][0])
        low.append(temp_map[item][1])
        middle.append(temp_map[item][2])
        high.append(temp_map[item][3])

    # 危险等级
    distr = Vul.objects.values('level').annotate(c=Count('id'))
    distr = {i['level']: i['c'] for i in distr}
    count = sum(distr.values())
    distr = [
        ['低危', distr[1]],
        ['中危', distr[2]],
        ['高危', distr[3]],
        ['未知', distr[0]]
    ]
    return render(request, 'statistic.html', context={
        'year_volume': year_volume, 'date': date, 'high': high, 'middle': middle, 'low': low,
        'unknown': unknown, 'distr': distr, 'count': count, 'year': year
    })


def vulnerability(request):
    data_dict = {}
    if request.method == 'POST':
        query = request.POST.get('query', '')
        level = request.POST.get('level', '')
        date_type = request.POST.get('date_type', '')
        startDate = request.POST.get('startDate', '')
        endDate = request.POST.get('endDate', '')
        # print("date_type:{},startDate:{},endDate:{}".format(date_type,startDate,endDate))
        if query:
            data_dict['cve__contains'] = query
        if level:
            data_dict['level'] = level
        if date_type and startDate and endDate:
            if datetime.strptime(startDate, '%Y-%m-%d') <= datetime.strptime(endDate, '%Y-%m-%d'):
                data_dict[f'{date_type}__gte'] = startDate
                data_dict[f'{date_type}__lte'] = endDate
        # print("data_dict:{}".format(data_dict))
        queryset = Vul.objects.values_list('id', 'no', 'level', 'name').filter(**data_dict).order_by('-publishtime')
        # 每次搜索跳转回第一页
        page_object = Pagination(request, queryset, query, 1, level, date_type, startDate, endDate)
        # print(page_object.page_queryset)
        context = {
            'queryset': page_object.page_queryset,
            'search_data': query,
            "page_string": page_object.html(),
        }
        return render(request, 'vulnerability.html', context)
    # 获取当前页码
    page = request.GET.get("page", "1")
    # 页码不是数字类型则将其转为数字
    if page.isdecimal():
        page = int(page)
    else:
        page = 1
    query = request.GET.get('query', '')
    level = request.GET.get('level', '')
    date_type = request.GET.get('date_type', '')
    startDate = request.GET.get('startDate', '')
    endDate = request.GET.get('endDate', '')
    # print("date_type:{},startDate:{},endDate:{}".format(date_type,startDate,endDate))
    if query:
        data_dict['cve__contains'] = query
    if level:
        data_dict['level'] = level
    if date_type and startDate and endDate:
        if datetime.strptime(startDate, '%Y-%m-%d') <= datetime.strptime(endDate, '%Y-%m-%d'):
            data_dict[f'{date_type}__gte'] = startDate
            data_dict[f'{date_type}__lte'] = endDate

    queryset = Vul.objects.values_list('id', 'no', 'level', 'name').filter(**data_dict).order_by('-publishtime')
    page_object = Pagination(request, queryset, query, page, level, date_type, startDate, endDate)
    context = {
        'queryset': page_object.page_queryset,
        'search_data': query,
        "page_string": page_object.html(),
    }
    return render(request, 'vulnerability.html', context)


def vulnerability_detail(request, vid):
    vul = Vul.objects.filter(id=vid).first()
    top_vul = Vul.objects.values_list('id', 'name', 'publishtime').filter(level=3)[:5]
    if vul.clicknum:
        vul.clicknum += 1
    else:
        vul.clicknum = 1
    vul.save()
    context = {
        'vul': vul,
        'top_vul': top_vul,
    }
    return render(request, 'vulnerability_detail.html', context)


def user(request):
    return render(request, 'user.html')
