from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # to specify objects on other apps we need three info
    # type(product, video, article, etc.,), id of the object and the object itsself, 
    # we use generic class ContentType for this purpose
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # the following will not work if the object is uuid instead of int
    object_id = models.PositiveIntegerField()
    # to get the actual object value tagged use GenericForeignKey
    content_object = GenericForeignKey()