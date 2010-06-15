import re
import os
import json

from django.core.management.base import BaseCommand

from laws.models import Law

class Command(BaseCommand):
    help = """Export reference structure of the US code."""

    def handle(self, *args, **options):
        refs = {}
        for law in Law.objects.exclude(title="", section="").filter(psection=""):
            if not law.name:
                continue

            all_refs = []
            for sub_law in Law.objects.filter(title=law.title,
                                              section=law.section):
                all_refs.extend(["%s.%s" % (ref.title, ref.section) for ref
                                 in sub_law.references.all()
                                 if ref.title and ref.section])

            refs["%s.%s" % (law.title, law.section)] = all_refs

        with open('refs.json', 'w') as f:
            json.dump(refs, f)

