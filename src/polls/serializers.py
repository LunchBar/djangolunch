from django.db import models
from rest_framework import serializers

from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice', 'votes', 'note', 'question']

class QuestionSerializer(serializers.ModelSerializer):
    choices_url = serializers.HyperlinkedIdentityField(
        view_name='choice-list',
        lookup_url_kwarg='question_pk'
    )

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'note', 'choices_url']
