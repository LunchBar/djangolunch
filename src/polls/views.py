from django.db.models import F
from rest_framework import viewsets, mixins, generics, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from .models import Question, Choice
from .serializers import ChoiceSerializer, QuestionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    '''
    questions endpoint

    create:
    questions endpoint

    ---
    required parameter:

    "question_text": question description
    '''
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceListViewSet(viewsets.GenericViewSet):
    '''
    list:
    questions endpoint
    '''
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def list(self, request, question_pk=None):
        choices = self.queryset.filter(question=question_pk) # or get_queryset ?
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)


class ChoiceBesidesListViewSet(viewsets.GenericViewSet,
                                    mixins.ListModelMixin, # for developing
                                    mixins.CreateModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin):
    '''
    choices endpoint except GET

    create:
    choices endpoint except GET

    ---
    required parameter:

    "choice": restaurant id

    "question": question id

    - "vote" will default to 0 if not given.

    list:
    This is for developing. please use /questions/{question_pk}/choices/
    '''
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


    @detail_route(methods=['put'])
    def vote(self, request, pk=None):
        """
        Vote for the choice will +1

        ---
        You don't need to send any json data to this endpoint.
        """
        queryset = self.get_queryset()
        queryset.filter(pk=pk).update(votes=F('votes') + 1)
        return Response(status=status.HTTP_200_OK)

