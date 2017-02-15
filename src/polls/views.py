from django.db.models import F
from rest_framework import viewsets, mixins, generics, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from .models import Question, Choice
from .serializers import ChoiceSerializer, QuestionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ChoiceListViewSet(viewsets.GenericViewSet): # note that this view is accessed by question item.
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
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


    @detail_route(methods=['put'])
    def vote(self, request, pk=None):
        queryset = self.get_queryset()
        queryset.filter(pk=pk).update(votes=F('votes') + 1)
        return Response(status=status.HTTP_200_OK)
