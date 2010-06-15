from django.shortcuts import render_to_response
from django.http import Http404
from django.template import RequestContext

from laws.models import Law

def show_law(request, title, section, psection=""):
    print [title, section]
    filter_on = {'title': title, 'section': section, 'order__gt': 0}
    if psection:
        filter_on['psection'] = psection

    top_level_parts = list(Law.objects.filter(**filter_on))
    if len(top_level_parts) == 0:
        raise Http404

    start = top_level_parts[0]
    end = top_level_parts[-1]

    all_parts = Law.objects.filter(order__gte=start.order, 
            order__lte=end.order)

    return render_to_response("laws/show.html", {
                'parts': all_parts,
            }, context_instance=RequestContext(request))
