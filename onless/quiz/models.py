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
    video = models.ForeignKey(Video, on_delete=models.PROTECT, null=True)
    img = models.ImageField(upload_to='quiz/img/%Y-%m-%d/')

    def __str__(self):
        return self.title

class ResultQuiz(models.Model):
    questions = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='result_questions', null=True)
    answers = models.ForeignKey(Answer,on_delete=models.CASCADE, related_name='result_questions', null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.questions} ning javobi {self.answers}"
