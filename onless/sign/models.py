from django.db import models

CHOICES = (
    ('1', 'Ogohlantiruvchi belgilar'),
    ('2', 'Imtiyoz belgilari'),
    ('3', 'Taqiqlovchi belgilar'),
    ('4', 'Buyuruvchi belgilar'),
    ('5', 'Axborot Ishora belgilari'),
    ('6', 'Servis belgilari'),
    ('7', "Qo'shimcha Axborot belgilari"),
)


class SignCategory(models.Model):
    title = models.CharField(choices=CHOICES, max_length=30)
    text = models.TextField(max_length=5000, blank=True)
    photo = models.ImageField(upload_to='sign/')
    sort = models.IntegerField(default=1, null=True)

    def __str__(self):
        return self.title


class Sign(models.Model):
    category = models.ForeignKey(SignCategory, on_delete=models.PROTECT, related_name='sign_cateogories')
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=5000, blank=True)
    photo = models.ImageField(upload_to="sign/")
    sort = models.IntegerField(default=1)

    def __str__(self):
        return self.title
