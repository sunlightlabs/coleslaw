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

    first_order = {}
    second_order = {}
    mappings = {}
    for part in all_parts:
        for reference in part.references.exclude(order=0):
            first_order[reference.order] = reference
            mappings[start.pk] = mappings.get(start.pk, [])
            mappings[start.pk].append(reference.pk)

            for ref2 in reference.references.exclude(order=0):
                second_order[ref2.order] = ref2
                mappings[reference.pk] = mappings.get(reference.pk, [])
                mappings[reference.pk].append(ref2)

            if not reference.psection and reference.section:
                for sub_law in Law.objects.filter(title=reference.title,
                                                  section=reference.section):
                    for ref2 in sub_law.references.exclude(order=0):
                        second_order[ref2.order] = ref2
                        mappings[reference.pk] = mappings.get(reference.pk, [])
                        mappings[reference.pk].append(ref2)

    first_order = [v for k,v in sorted(first_order.iteritems())]
    second_order = [v for k,v in sorted(second_order.iteritems())]

    return render_to_response("laws/show.html", {
                'parts': all_parts,
                'first_order': first_order,
                'second_order': second_order,
                'mappings': mappings
            }, context_instance=RequestContext(request))
