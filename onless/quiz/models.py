from django.db import models
from user.models import User
from video.models import Video
from . import fields

class Answer(models.Model):
    text = models.CharField(max_length=600)
    questions = models.ForeignKey('Question', on_delete=models.SET_NULL, related_name='answers', null=True)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Question(models.Model):
    title = models.CharField(max_length=600)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(upload_to='quiz/img/%Y-%m-%d/', blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_test = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title

class Bilet(models.Model):
    number = models.IntegerField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.number}"

BILET_SAVOL = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
)

class Savol(models.Model):
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True)
    bilet = models.ForeignKey(Bilet, on_delete=models.SET_NULL, null=True)
    bilet_savol = models.CharField(max_length=2, choices=BILET_SAVOL)
    title_uz = models.CharField(max_length=1000, blank=True)
    title_kr = models.CharField(max_length=1000, blank=True)
    title_ru = models.CharField(max_length=1000, blank=True)
    photo = models.ImageField(upload_to='quiz/img/', blank=True, default='')
    is_photo = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title_uz}"

    class Meta:
        verbose_name = 'Test savoli'
        verbose_name_plural = 'Test savollari'

class Javob(models.Model):
    text_uz = models.CharField(max_length=1000, blank=True)
    text_kr = models.CharField(max_length=1000, blank=True)
    text_ru = models.CharField(max_length=1000, blank=True)
    savol = models.ForeignKey(Savol, on_delete=models.SET_NULL,null=True, related_name='answers')
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text_uz}"

    class Meta:
        verbose_name = 'Test javobi'
        verbose_name_plural = 'Test javoblari'

# class Result(models.Model):
#     question = models.ForeignKey(Savol, on_delete=models.CASCADE, related_name='result_savol', null=True)
#     answer = models.ForeignKey(Javob, on_delete=models.SET_NULL, related_name='result_javob', null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='result_user', blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.user}"
#
#     class Meta:
#         verbose_name = 'Test natijasi'
#         verbose_name_plural = 'Test natijalari'

class ResultQuiz(models.Model):
    question = models.ForeignKey(Savol, on_delete=models.CASCADE, related_name='result_question', null=True)
    answer = models.ForeignKey(Javob, on_delete=models.SET_NULL, related_name='result_answer', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='result_user', blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Test natijasi'
        verbose_name_plural = 'Test natijalari'

# class Attempt(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempt_user', null=True)
#     allowed = fields.IntegerRangeField(verbose_name='Ruxsat berilgan urinishlar',default=2, max_value=3)
#     solved = fields.IntegerRangeField(verbose_name='Bajarilgan urinishlar',default=0)
#
#     def __str__(self):
#         return f"{self.user}: {self.allowed}"
#
#     class Meta:
#         verbose_name = 'Urinish'
#         verbose_name_plural = 'Urinishlar'

class ResultJavob(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='resultjavob_user', null=True)
    bilet = models.ForeignKey(Bilet, on_delete=models.SET_NULL, related_name='resultjavob_bilet', null=True)
    j_1 = models.BooleanField(default=False)
    j_2 = models.BooleanField(default=False)
    j_3 = models.BooleanField(default=False)
    j_4 = models.BooleanField(default=False)
    j_5 = models.BooleanField(default=False)
    j_6 = models.BooleanField(default=False)
    j_7 = models.BooleanField(default=False)
    j_8 = models.BooleanField(default=False)
    j_9 = models.BooleanField(default=False)
    j_10 = models.BooleanField(default=False)


class CheckTestColor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bilet = models.ForeignKey(Bilet, on_delete=models.CASCADE,)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bilet}"