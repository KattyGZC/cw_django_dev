from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Question(models.Model):
    created = models.DateField('Creada', auto_now_add=True)
    author = models.ForeignKey(get_user_model(), related_name="questions", verbose_name='Pregunta',
                               on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')

    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('survey:question-list')


class Answer(models.Model):
    ANSWERS_VALUES = ((0, 'Sin Responder'),
                      (1, 'Muy Bajo'),
                      (2, 'Bajo'),
                      (3, 'Regular'),
                      (4, 'Alto'),
                      (5, 'Muy Alto'),)

    question = models.ForeignKey(
        Question, related_name="answers", verbose_name='Pregunta', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(
    ), related_name="answers", verbose_name='Autor', on_delete=models.CASCADE)
    value = models.PositiveIntegerField("Respuesta", default=0)
    comment = models.TextField("Comentario", default="", blank=True)


class Vote(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='votes', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='votes', on_delete=models.CASCADE)
    is_like = models.BooleanField()  # True for like, False for dislike
    created = models.DateTimeField(auto_now_add=True)
