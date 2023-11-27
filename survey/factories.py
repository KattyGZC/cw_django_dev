import factory
from django.contrib.auth.models import User

from survey.models import Question

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')

class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    title = factory.Sequence(lambda n: f'Pregunta {n}')
    description = factory.Faker('text')
    author = factory.SubFactory(UserFactory)

