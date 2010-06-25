import re

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext

from laws.models import Law

def target(request, target):
    match = re.match(r'usc_sec_(?P<title>\d+)_(?P<section>\w+)'
                     r'-+(?P<rest>[a-zA-Z0-9])-*(?P<anchor>(#\w+)?)', target)
    if match:
        title = match.group('title').lstrip('0')
        section = match.group('section').lstrip('0')
        section += match.group('rest').lstrip('0')
        anchor = match.group('anchor')
        if anchor == '#':
            anchor = ''
        return HttpResponseRedirect('/laws/%s/%s%s/?%s' % (
                title, section, anchor, request.GET.urlencode()))
    raise Http404

def section(request, title, section):
    sections = list(Law.objects.filter(title=title, section=section,
                                       order__gt=0))
    
    try:
        section = sections[0]
    except IndexError:
        raise Http404

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
            'mappings': mappings})
