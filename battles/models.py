from django.db import models


class BattleEvent(models.Model):
    STATUS_WAITING = 'waiting'
    STATUS_ACTIVE = 'active'
    STATUS_VOTING = 'voting'
    STATUS_FINISHED = 'finished'

    STATUS_CHOICES = [
        (STATUS_WAITING, 'Ожидание'),
        (STATUS_ACTIVE, 'Приём решений'),
        (STATUS_VOTING, 'Голосование'),
        (STATUS_FINISHED, 'Завершено'),
    ]

    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_WAITING,
    )

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    event = models.ForeignKey(BattleEvent, on_delete=models.CASCADE)
    code_snapshot = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.team.name} — {self.event.title}'


class Vote(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    voter_key = models.CharField(max_length=100)
    score = models.IntegerField(default=1)

    def __str__(self):
        return f'Голос за {self.submission.team.name}'