import re

from django.core.management.base import BaseCommand
from laws.models import Law
import lxml.etree

class Command(BaseCommand):
    help = """Import the US legal code from Cornel's XML format."""

    def handle(self, **options):
        parser = lxml.etree.XMLParser(dtd_validation=False, load_dtd=False,
                                      resolve_entities=False)

        with open('/Users/mike/Downloads/uscode19/T19F00927.XML') as f:
            xml = lxml.etree.fromstring(f.read(), parser=parser)

            self.title = int(xml.attrib['titlenum'])
            self.section = int(xml.xpath('//section')[0].attrib['num'])

            self.ordering = 1

            law = Law(level=0, order=0, title=self.title,
                      section=self.section,
                      text=xml.xpath('string(//section/head)'))
            law.set_name()
            law.save()

            for psection in xml.xpath('//section/sectioncontent/psection'):
                self.parse_psection(psection, [])

    def parse_psection(self, psection, parts):
        self.ordering += 1
        parts.append(psection.xpath('enum')[0].text)

        law = Law(level=int(psection.attrib['lev']),
                  order=self.ordering,
                  title=self.title,
                  section=self.section,
                  psection=psection.attrib['id'],
                  text=psection.xpath('string(text)'))
        law.set_name(parts)
        law.save()

        for ref in psection.xpath('text/aref'):
            for subref in ref.xpath('subref'):
                if subref.attrib['type'] == 'title':
                    pass
                elif subref.attrib['type'] in ['sec', 'psec']:
                    (title, sec1, sec2, psec_id) = re.match(
                        r"usc_sec_(?P<title>\d+)_(?P<section>[^-]+)-*(?P<section2>[0-9A-Za-z]*)-?(?:\#(?P<psection>\w+))?",
                        subref.attrib['target']).groups()

                    section = sec1.lstrip('0') + sec2.rstrip('0')

                    ref_law, created = Law.objects.get_or_create(
                        title=title,
                        section=section,
                        psection=psec_id or "")

                    law.references.add(ref_law)
                else:
                    pass

        for sub_psection in psection.xpath('psection'):
            self.parse_psection(sub_psection, parts)

        parts.pop()
