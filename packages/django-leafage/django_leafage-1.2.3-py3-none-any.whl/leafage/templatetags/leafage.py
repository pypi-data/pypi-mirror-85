from django import template
from distutils.sysconfig import get_python_lib
from django.template import Library, loader, Context


register = template.Library()

@register.filter
def subtract(value, arg):
    try:
        output =  value - arg
    except:
        output = ''
    return output

@register.filter(name='paginator')
def paginator(object_list, request, style=None):
    path = 'paginator.html'
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
    html = loader.render_to_string(
        path,
        {
            'obj_list': object_list,
            'path': path,
            'style': style
        }
    )

    return html


@register.simple_tag(takes_context=True)
def paginate(context, object_list,request, **kwargs):
    template_name = 'paginator.html'
    style = ''
    if kwargs:
        style = kwargs.get('style', '')
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

    t = loader.get_template(template_name)
    return t.render({
        'obj_list': object_list,
        'path': path,
        'style': style
    })

