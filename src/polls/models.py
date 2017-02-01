from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200, default='下禮拜呷蝦米?')
    pub_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, default='')

    # def __str__(self):
    #     return self.question_text

class Choice(models.Model):
    class Meta:
        ordering = ['votes']

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    choice = models.OneToOneField('restaurants.Restaurant', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    note = models.TextField(blank=True, default='')

    # def __str__(self):
    #     return self.choice
