from django.db import models

# Create your models here.

class Date(models.Model):
	elo_date = models.DateTimeField('date published')


class ELO(models.Model):
	team_elo = models.IntegerField(default=0)

