from django import template
from distutils.sysconfig import get_python_lib
from django.template import Library, loader, Context


register = template.Library()

@register.filter
def subtract(value, arg):
    try:
        arg = int(arg)
    except:
        arg = 1
    try:
        output = value - arg
    except:
        output = ''
    return output

@register.filter(name='paginator')
def paginator(object_list, request, **kwargs):
    path = 'paginator.html'
    kw = dict()
    for k,v in kwargs.items():
        kw[k] = v
    path = request.build_absolute_uri()
    # path.replace('')
    path_list = path.split('?page')
    path = path_list[0]
    path_list = path.split('&page')
    path = path_list[0]
    if '?' in path :
        path = path + '&'
    if '?' not in path:
        path = path + '?'
    # path.replace('&page=', '')
    # path.replace('?page=', '')
    data = {
        'obj_list': object_list,
        'path': path
    }
    data.update(kw)
    html = loader.render_to_string(
        path,
        data
    )

    return html


@register.simple_tag(takes_context=True)
def paginate(context, object_list,request, **kwargs):
    template_name = 'paginator.html'
    kw = dict()
    for k,v in kwargs.items():
        kw[k] = v
    path = request.build_absolute_uri()
    # path.replace('')
    path_list = path.split('?page')
    path = path_list[0]
    path_list = path.split('&page')
    path = path_list[0]
    if '?' in path :
        path = path + '&'
    if '?' not in path:
        path = path + '?'
    # path.replace('&page=', '')
    # path.replace('?page=', '')
    data = {
        'obj_list': object_list,
        'path': path
    }
    data.update(kw)
    t = loader.get_template(template_name)
    return t.render(data)

