from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(request, obj_list, obj_count=10):
    try:
        obj_list = list(obj_list)
    except:
        raise ValueError("object is not iterable")
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_list, obj_count)
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator.num_pages)
    return obj_list
