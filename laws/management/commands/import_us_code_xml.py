# -*- coding: utf-8 -*-
import re
import os
import lxml.etree

from django.core.management.base import BaseCommand
from django.utils.encoding import force_unicode

from laws.models import Law

import htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

class Command(BaseCommand):
    help = """Import the US legal code from Cornel's XML format."""

    def handle(self, *args, **options):
        if not len(args) > 0:
            print "Please supply the directory of extracted XML files as the first argument."
            return

        dirname = args[0]
        self.ordering = 0

#        self.import_xml("/home/tc1/Desktop/uscxml/uscode06/T06F00257.XML")
#        return

        count = 0
        for root, dirs, files in os.walk(dirname):
            for filename in files:
                if not filename.lower().endswith(".xml"):
                    continue
                path = os.path.join(root, filename)
                count += 1
                print path, "%.02f" % (count / 600.)
                self.import_xml(path)


    def import_xml(self, filename):
        parser = lxml.etree.XMLParser(dtd_validation=False, load_dtd=False,
                                      resolve_entities=False, encoding="utf8")
        with open(filename) as f:
            source = os.path.basename(filename)
            file_contents = unescape(f.read())
            file_contents = re.sub('''^<\?xml version="1.0" encoding="UTF-8"\s*\??>''', 
                    '', file_contents)
            file_contents = file_contents.replace("&", "&amp;")
            xml = lxml.etree.fromstring(file_contents, parser=parser)

            try:
                self.title = xml.attrib['titlenum'].lstrip('0')
            except KeyError:
                return

            try:
                title_section = xml.xpath('//hdsupnest')[0].text
                match = re.match("TITLE (?P<title>\w+)\s*(?:-|&mdash;)\s*(?P<name>\w+)", 
                        title_section)
                if match:
                    result = Law.objects.get_or_create(
                                              title=match.group('title').lstrip('0'),
                                              section="",
                                              psection="",
                                              defaults={
                                                  'text': title_section,
                                                  'order': self.ordering,
                                                  'level': 0,
                                              })
                    self.ordering += 1
            except IndexError:
                pass

            sections = xml.xpath('//section')
            if len(sections) == 0:
                return
            self.section = sections[0].attrib['num']

            law = Law(level=0, 
                      order=self.ordering, 
                      title=self.title,
                      section=self.section,
                      text=unicode(xml.xpath('string(//section/head)')),
                      source=source)
            law.set_name()
            law.save()

            for psection in xml.xpath('//section/sectioncontent/psection'):
                self.parse_psection(psection, [], source)

    def parse_psection(self, psection, parts, source):
        parts.append(psection.xpath('string(enum)'))
        psection_id = psection.attrib['id']

        # Get references
        ref_laws = []
        for ref in psection.xpath('text/aref'):
            for subref in ref.xpath('subref'):
                if subref.attrib['type'] == 'title':
                    match = re.match( r"usc_sup_01_([^_])", 
                            subref.attrib['target'])
                    if match:
                        (title,) = match.groups()
                        title = title.lstrip('0')
                        section = ""
                        ref_psec_id = ""
                    else:
                        continue

                elif subref.attrib['type'] in ['sec', 'psec']:
                    match = re.match(
                        r"usc_sec_(?P<title>\d+)_(?P<section>[^-]+)-*(?P<section2>[0-9A-Za-z]*)-?(?:\#(?P<psection>\w+))?",
                        subref.attrib['target'])
                    if not match:
                        continue
                    (title, sec1, sec2, ref_psec_id) = match.groups()
                    title = title.lstrip('0')
                    section = sec1.lstrip('0') + sec2.rstrip('0')
                    ref_psec_id = ref_psec_id or ""

                else:
                    continue

                matches = Law.objects.filter(
                    title=title,
                    section=section,
                    psection=ref_psec_id)
                if len(matches) == 0:
                    ref_law = Law.objects.create(
                            title=title,
                            section=section,
                            psection=ref_psec_id,
                            order=0)
                else:
                    ref_law = matches[0]
                ref_laws.append(ref_law)

        for sub_element in psection:
            if sub_element.tag in ["text", "head"]:
                self.ordering += 1
                matches = Law.objects.filter(
                        title=self.title,
                        section=self.section,
                        psection=psection_id)
                if len(matches) == 1 and not matches[0].source:
                    law = matches[0]
                else:
                    law = Law(
                        title=self.title,
                        section=self.section,
                        psection=psection_id)
                law.level = int(psection.attrib['lev'])
                law.text = sub_element.text or ""
                law.order = self.ordering
                law.source = source
                law.set_name(parts)
                law.save()
            elif sub_element.tag == "psection":
                self.parse_psection(sub_element, parts, source)
        if ref_laws:
            first = Law.objects.filter(title=self.title, section=self.section, 
                    psection=psection_id)[0]
            first.references = ref_laws
        parts.pop()
