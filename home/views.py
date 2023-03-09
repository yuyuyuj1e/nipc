from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
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
    return render(request, 'statistic.html')


def vulnerability(request):
    queryset = Vul.objects.all()
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        "page_string": page_object.html(),
    }
    # 获取level值为0且name不为空的数据
    # queryset = Vul.objects.filter(level=0).filter(~Q(name = ''))
    return render(request, 'vulnerability.html', context)

def vulnerability_detail(request, vid):
    vul = Vul.objects.filter(id=vid).first()
    vul.clicknum += 1
    vul.save()
    context = {
        'vul': vul,
    }
    return render(request, 'vulnerability_detail.html', context)


def vulnerabilitys_list(request):
    # limit = int(request.GET.get('limit', 10))  # limit指分页查询，一页10个
    # offset = int(request.GET.get('offset', 0))  # 从第一条数据开始查 （offset,limit）从第offset（从0开始）条数据开始查，共查limit个
    # newest = Vul.objects
    # if request.GET.get('t'):
    #     search = {request.GET.get('search_field', 'name') + '__icontains': request.GET.get('t')}
    #     newest = newest.filter(**search)     #filter()方法返回一个新的数组，新数组的元素是原数组中通过符合制定筛选条件的所有元素
    # total = sum(i['c'] for i in newest.values('level').annotate(c=Count('*')))  #通过level分组并计算每组的个数，最后求和。total是筛选出的漏洞总条数
    # newest = newest.raw('''select * from (select id from vul_new order by publishtime desc limit %d, %d) a left join vul_new b on a.id=b.id''' % (offset, limit))
    # newest = [{'id': i.id, 'name': i.name, 'visit': 10, 'severity': i.level, 'publishtime': i.publishtime and i.publishtime.strftime(
    #     '%Y-%m-%d'), 'clicknum': i.clicknum} for i in newest]
    # return HttpResponse(json.dumps({"total": total, 'rows': newest}))

    return render(request, 'vulnerability.html')


def user(request):
    return render(request, 'user.html')
