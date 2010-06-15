import re
import os
import lxml.etree
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

for root, dirs, files in os.walk("/home/tc1/Desktop/uscxml/"):
    for filename in files:
        path = os.path.join(root, filename)
        with open(path) as fh:
            try:
                file_contents = unescape(fh.read())
            except UnicodeDecodeError:
                print path, "ASCII ERROR!!!!"
                continue
            file_contents = re.sub('''^<\?xml version="1.0" encoding="UTF-8"\s*\??>''',
                '', file_contents)
            file_contents = file_contents.replace("&", u"&amp;")
            try:
                parser = lxml.etree.XMLParser(dtd_validation=False, 
                        load_dtd=False, resolve_entities=False, 
                        encoding="utf8")
            except lxml.etree.XMLSyntaxError:
                print path, "XML ERROR!!!!"

xml = lxml.etree.fromstring(file_contents, parser=parser)

