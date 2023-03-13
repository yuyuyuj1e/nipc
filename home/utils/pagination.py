"""
自定义的分页组件

在视图函数中：
    def pretty_list(request):

        # 1.根据自己的情况去筛选自己的数据
        queryset = models.PrettyNum.objects.all()

        # 2.实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html()       # 生成页码
        }
        return render(request, 'pretty_list.html', context)

在HTML页面中

    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>
"""
import base64
from django.core.paginator import Paginator, EmptyPage
from django.utils.safestring import mark_safe
# 整合使用游标查询，减少由于limit/offset所造成的查询时间久的问题
# from cursor_pagination import CursorPaginator


class Pagination(object):

    def __init__(self, request, queryset, query=None, page=None, level=None, date_type=None,
                 start_date=None, end_date=None, page_size=10,  page_param="page", query_param="query",
                 level_param="level", date_time_param="date_type", start_date_param="startDate", end_date_param="endDate", plus=3):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/etty/list/?page=12
        :param plus: 显示当前页的 前或后几页（页码）
        """

        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param
        self.query_param = query_param
        self.level_param = level_param
        self.date_time_param = date_time_param
        self.start_date_param = start_date_param
        self.end_date_param = end_date_param

        self.page = page
        self.query = query
        self.level = level
        self.date_type = date_type
        self.start_date = start_date
        self.end_date = end_date
        # 每页的数据
        self.page_size = page_size

        # 划分每页的第一条，最后一条数据
        self.start = (page - 1) * page_size
        self.end = page * page_size

        # 测试程序运行时间
        # import time
        # start_time = time.perf_counter()

        # 返回前台的一页数据(获取要返回的页数据)
        # 法一： 直接对查询结果集切片
        # self.page_queryset = queryset[self.start:self.end]

        # 法二： 使用Paginator类
        self.page_object = Paginator(queryset, page_size)
        try:
            self.page_queryset = self.page_object.page(page)
        except EmptyPage:
            # 若当前页page超出了数据范围，则将其指向最后一页
            max_page = self.page_object.num_pages
            self.page_queryset = self.page_object.page(max_page)

        # 法三：使用游标分页(排序后的分页数据的游标不好定位， 随意不排序的数据可以使用它)
        # paginator = CursorPaginator(queryset, ordering=['id'])
        # start_cursor = base64.b64encode(str(self.start).encode('utf-8')).decode('utf-8')
        # end_cursor = base64.b64encode(str(self.end).encode('utf-8')).decode('utf-8')
        # self.page_queryset = paginator.page(first=page_size, after=start_cursor, before=end_cursor)

        # end_time = time.perf_counter()
        # print("Total running time:", end_time - start_time, "seconds")

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出，显示当前页的前5页、后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少，都没有达到11页。
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库中的数据比较多 > 11页。

            # 当前页<5时（小极值）
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页 > 5
                # 当前页+5 > 总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        if self.query:
            self.query_dict.setlist(self.query_param, [self.query])
        if self.level:
            self.query_dict.setlist(self.level_param, [self.level])
        if self.date_type and self.start_date and self.end_date:
            self.query_dict.setlist(self.date_time_param, [self.date_type])
            self.query_dict.setlist(self.start_date_param, [self.start_date])
            self.query_dict.setlist(self.end_date_param, [self.end_date])

        page_str_list.append(
            '<li class="page-item"><a class="page-link" href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li class="page-item"><a class="page-link" href="?{}"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li class="page-item"><a class="page-link" href="?{}"><span aria-hidden="true">&laquo;</span></a></a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(prev)

        # 页面
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="page-item active"><a class="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            else:
                ele = '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li class="page-item"><a class="page-link" href="?{}"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li class="page-item"><a class="page-link" href="?{}"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(prev)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append(
            '<li class="page-item"><a class="page-link" href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = """
            <li>
                
                <form style="float: left;margin-left: -1px;display: flex;">
                    <input name="page" style="order: 1;position: relative;float:left;display: inline-block;width: 55px;height: 34px !important;border-radius: 0;"
                        type="text" class="form-control rounded text-center" value="1">
                    <span style="order: 2;margin-top: 7px;margin-left: 5px;"> 页</span>
                    <button style="order: 0;border-radius: 0" class="btn btn-default" type="submit">跳转至第</button>
                    
                </form>
            </li>
            """

        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
