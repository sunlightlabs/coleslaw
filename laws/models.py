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

    order = models.IntegerField(default=0, db_index=True)
    references = models.ManyToManyField('Law')

    def num_references(self):
        return self.references.exclude(order=0).count()

    def get_absolute_url(self):
        if self.section == "" and self.psection == "":
            return reverse("laws_title_index", args=([self.title]))
        else:
            url = reverse("laws_section", args=(self.title, self.section))
            if self.psection:
                url += "#" + self.psection
            return url

    def __unicode__(self):
        if self.section == "" and self.psection == "":
            return self.title
        return self.name

    def set_name(self, psection_parts=None):
        self.name = unicode(self.title)
        if self.section:
            self.name += u"§%s" % self.section
            self.name += ''.join(psection_parts or [])

    class Meta:
        ordering = ('order',)
        unique_together = (("title", "section", "psection", "order"),)
