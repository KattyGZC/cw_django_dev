from datetime import timezone, datetime
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Case, When, IntegerField, F, Sum, Value, Q, ExpressionWrapper
from django.db.models.functions import Coalesce
from survey.models import Question, Answer, Vote
from survey.utils import update_vote_counts


class QuestionListView(ListView):
    model = Question

    def get_queryset(self):
        today = datetime.now(timezone.utc)
        queryset = Question.objects.annotate(
            num_answers=Count('answers'),
            num_likes=Count('votes', filter=Q(votes__is_like=True)),
            num_dislikes=Count('votes', filter=Q(votes__is_like=False)),
            extra_points=Case(
                When(created=today, then=Value(10)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).annotate(
            ranking=ExpressionWrapper(
                Coalesce(F('num_answers'), 0) * 10 +
                Coalesce(F('num_likes'), 0) * 5 -
                Coalesce(F('num_dislikes'), 0) * 3 +
                F('extra_points'),
                output_field=IntegerField()
            )
        ).order_by('-ranking')[:20]

        if self.request.user.is_authenticated:
            user_votes = Vote.objects.filter(
                user=self.request.user, question__in=queryset)
            liked_questions = set(user_votes.filter(
                is_like=True).values_list('question_id', flat=True))
            disliked_questions = set(user_votes.filter(
                is_like=False).values_list('question_id', flat=True))

            for question in queryset:
                question.user_has_liked = question.id in liked_questions
                question.user_has_disliked = question.id in disliked_questions

        return queryset


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'description']
    redirect_url = ''

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['title', 'description']
    template_name = 'survey/question_form.html'


def answer_question(request, question_pk, value):
    user = request.user
    question = Question.objects.get(pk=question_pk)
    if not user.is_authenticated:
        return JsonResponse({'Error': 'Para responder el usuario debe estar autenticado.'}, status=403)

    if value in '012345':
        answer, created = Answer.objects.get_or_create(
            question=question, author=user, defaults={'value': value})
        if not created:
            answer.value = value
            answer.save()

    return JsonResponse({"message": "Respuesta registrada correctamente."})


def like_dislike_question(request, question_pk, vote_type):
    user = request.user
    question = Question.objects.get(pk=question_pk)

    if not user.is_authenticated:
        return JsonResponse({'Error': 'Para votar el usuario debe estar autenticado.'}, status=403)

    if vote_type in ['like', 'dislike']:
        vote, created = Vote.objects.get_or_create(
            user=user, question=question,
            defaults={'is_like': vote_type == 'like'}
        )
        if not created:
            vote.is_like = vote_type == 'like'
            vote.save()
    elif vote_type == 'none':
        Vote.objects.filter(user=user, question=question).delete()

    update_vote_counts(question)

    return JsonResponse({"message": "Voto registrado correctamente."})
