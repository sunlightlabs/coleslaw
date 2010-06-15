# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse

class Law(models.Model):
    #
    #  Note that there can be multiple entries with the same title, section,
    #  and psection, because of the nested structure.
    #   
    #  Title 1, sec 13               # order 1
    #     psection (a)(b)(c)         # order 2
    #  Title 1, sec 13 continued...  # order 3
    #     psection (a)(b)(d)         # order 4
    #  ...
    #
    title = models.CharField(max_length=8)
    section = models.CharField(max_length=255, blank=True, default="")
    psection = models.CharField(max_length=255, blank=True, default="")
    level = models.IntegerField(default=0)
    name = models.CharField(max_length=255, blank=True, default="")
    text = models.TextField()
    source = models.CharField(max_length=255)

    order = models.IntegerField(default=0)
    references = models.ManyToManyField('Law')

    def num_references(self):
        return self.references.count()

    def get_absolute_url(self):
        return reverse("laws_show_law", 
                args=(self.title, self.section, self.psection))

    def __unicode__(self):
        return self.name

    def set_name(self, psection_parts=None):
        self.name = unicode(self.title)
        if self.section:
            self.name += u"§%s" % self.section
            self.name += ''.join(psection_parts or [])

    class Meta:
        ordering = ('order',)
        unique_together = (("title", "section", "psection", "order"),)

