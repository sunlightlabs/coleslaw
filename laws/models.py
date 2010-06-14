from django.db import models
from django.core.urlresolvers import reverse

class Law(models.Model):
    title = models.IntegerField()
    section = models.IntegerField()
    psection = models.CharField(max_length=32)
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

