from django.urls import reverse
from django.test import RequestFactory, TestCase
from django.test import Client
from .factories import QuestionFactory, UserFactory


class QuestionListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.users = UserFactory.create_batch(6)
        self.questions = []
        for user in self.users:
            questions_for_user = QuestionFactory.create_batch(4, author=user)
            self.questions.extend(questions_for_user)

    def test_view_status_code(self):
        response = self.client.get(reverse('survey:question-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_returns_top_20_questions(self):
        response = self.client.get(reverse('survey:question-list'))
        self.assertEqual(len(response.context['object_list']), 20)


class QuestionCreateViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client.force_login(self.user)

    def test_question_create_view(self):
        response = self.client.post(reverse('survey:question-create'), {
            'title': 'Nueva Pregunta',
            'description': 'Descripción de la pregunta'
        })

        self.assertEqual(response.status_code, 302)


class QuestionUpdateViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        self.question = QuestionFactory(author=self.user)

    def test_question_update_view(self):
        response = self.client.post(reverse('survey:question-edit', args=[self.question.id]), {
            'title': 'Título Actualizado',
            'description': 'Descripción actualizada'
        })

        self.assertEqual(response.status_code, 302)


class AnswerQuestionViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        self.question = QuestionFactory()

    def test_answer_question_view(self):
        response = self.client.post(
            reverse('survey:question-answer', args=[self.question.id, '3']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
                         "message": "Respuesta registrada correctamente."})
