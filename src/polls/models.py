from django.db import models

# Create your models here.
class Question(models.Model):
    # question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # def __str__(self):
    #     return self.question_text

class Choice(models.Model):
    class Meta:
        ordering = ['votes']

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.choice
