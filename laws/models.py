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
    title = models.IntegerField()
    section = models.IntegerField(default=0)
    psection = models.CharField(max_length=32, blank=True, default="")
    text = models.TextField()

    order = models.IntegerField()
    references = models.ManyToManyField('Law')

    def num_references(self):
        return self.references.count()

    def get_absolute_url(self):
        return reverse("laws_show_law", 
                args=(self.title, self.section, self.psection))

    def __unicode__(self):
        return u"%i§%i%s" % (
                self.title, 
                self.section, 
                "".join(["(%s)" % o for o in split(self.psection, '_')])
        )

    class Meta:
        ordering = order
        unique_together = (("title", "section", "psection", "order"),)

