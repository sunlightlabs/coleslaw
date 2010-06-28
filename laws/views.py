import re

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator

from laws.models import Law

def target(request, target):
    match = re.match(r'usc_(sec|sup_01)_(?P<title>\d+)'
                     r'(_(?P<section>\w+)-+(?P<rest>[a-zA-Z0-9])[-0]*)?'
                     r'(?P<psection>[a-zA-Z0-9_]+)?', target)
    if match:
        parts = ['laws']
        parts.append(match.group('title').lstrip('0'))
        if match.group('section'):
            section = match.group('section').lstrip('0')
            section += match.group('rest').lstrip('0')
            parts.append(section)
        if match.group('psection'):
            parts.append(match.group('psection'))
        return HttpResponseRedirect("/%s?%s" % (
                "/".join(parts), request.GET.urlencode()))
    raise Http404

def section(request, title, section, psection=None):
    sections = Law.objects.filter(title=title, section=section, order__gt=0)
    if psection != None:
        sections = sections.filter(psection=psection)
    sections = list(sections)
    try:
        section = sections[0]
    except IndexError:
        raise Http404

    if request.GET.get('context', None) == "hoverbubble":
        return HttpResponse(section.text)

    start = sections[0]
    end = sections[-1]

    all_parts = Law.objects.filter(order__gt=start.order,
                                   order__lte=end.order)
    

    first_order = {}
    mappings = {}
    for part in all_parts:
        for reference in part.references.exclude(order=0):
            first_order[reference.order] = reference
            mappings[start.pk] = mappings.get(start.pk, [])
            mappings[start.pk].append(reference.pk)
            
    first_order = [v for k,v in sorted(first_order.iteritems())]

    return render_to_response("laws/section.html", {
            'section': section,
            'references': first_order,
            'mappings': mappings},
        context_instance=RequestContext(request))

def title_index(request, title):
    parts = Law.objects.filter(title=title, psection="", order__gt=0).exclude(text="").order_by('order')
    try:
        page = Paginator(parts, 100).page(int(request.GET.get('p', 1)))
    except (EmptyPage, InvalidPage, ValueError):
        raise Http404

    return render_to_response("laws/title_index.html", {
        'title': title,
        'page': page,
    }, context_instance=RequestContext(request))

def index(request):
    titles = sorted(Law.objects.filter(section="", psection=""),
                    cmp=lambda l, r: cmp(int(l.title), int(r.title)))
    return render_to_response("laws/index.html", {
        'titles': titles,
    }, context_instance=RequestContext(request))
