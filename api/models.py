import uuid
from django.db import models

# we set some choices
PETS_TYPE_CHOICES = (("cat", "cat"), ("dog", "dog"))
PETS_SEX_CHOICES = (("boy", "boy"), ("girl", "girl"))

# pets photo model
class PetsPhoto(models.Model):
    # the pet object must be created before adding the photo
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(to="Pets", on_delete=models.CASCADE)
    url = models.URLField(max_length=300, null=False)


# this can be optimized  by adding the type and the name to
# a seperated table linking them through foreign key instead of choices
class Pets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, choices=PETS_SEX_CHOICES)
    age = models.IntegerField()
    type = models.CharField(max_length=20, choices=PETS_TYPE_CHOICES)
    photos = models.ManyToManyField(PetsPhoto, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
