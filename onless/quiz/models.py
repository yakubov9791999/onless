from django.db import models
from user.models import User
from video.models import Video


class Answer(models.Model):
    text = models.CharField(max_length=600)
    questions = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers', null=True)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Question(models.Model):
    title = models.CharField(max_length=600)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(upload_to='quiz/img/%Y-%m-%d/', blank=True, default='')
    is_active = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title


class ResultQuiz(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='result_questions', null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='result_answer', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='result_user', blank=True, null=True)

    def __str__(self):
        return f"{self.question} ning javobi {self.answer}"

    class Meta:
        verbose_name = 'Test javobi'
        verbose_name_plural = 'Test javoblari'
