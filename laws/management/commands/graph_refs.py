from laws.models import Law
import json

import pydot
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """Export reference structure of the US code."""

    def handle(self, *args, **options):
        try:
            filename = args[0]
        except IndexError:
            filename = "refs.jpg"

        with open('refs.json') as f:
            self.refs = json.load(f)

        for title in range(1, 51):
            print title
            self.graph_title(title)

    def graph_title(self, title):
        s = set()
        l = []

        for ref in self.refs:
            if not ref[0].startswith("%s." % title):
                continue
            for to in ref[1]:
                if not to.startswith("%s." % title):
                    continue
                s.add((ref[0], to))
                l.append((ref[0], to))


        g = pydot.graph_from_edges(l, directed=True)
        #g.write_jpeg("graphs/%s.jpg" % title)
        g.write_pdf("graphs/default/%s.pdf" % title)

        g = pydot.graph_from_edges(s, directed=True)
        #g.write_jpeg("graphs/%s_no_dups.jpg" % title)
        g.write_pdf("graphs/no_dups/%s.pdf" % title)
