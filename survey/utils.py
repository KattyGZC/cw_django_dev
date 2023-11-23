from survey.models import Vote


def update_vote_counts(question):
    likes = Vote.objects.filter(question=question, is_like=True).count()
    dislikes = Vote.objects.filter(question=question, is_like=False).count()

    question.like = likes
    question.dislike = dislikes
    question.save()