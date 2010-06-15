from laws.models import Law

import pydot
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """Export reference structure of the US code."""

    def handle(self, *args, **options):
        try:
            filename = args[0]
        except IndexError:
            filename = "refs.jpg"

        refs = []
        for law in Law.objects.exclude(section="", title="").filter(
            psection=""):

            local_refs = set(["%s.%s" % (ref.title, ref.section) for ref
                          in law.references.all()])

            law_name = "%s.%s" % (law.title, law.section)
            refs.extend([[law_name, local_ref] for local_ref in local_refs])

        graph = pydot.graph_from_edges(refs)
        graph.write_jpeg(filename, prog='dot')
