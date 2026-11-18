from django.core.management.base import BaseCommand
from django.utils import timezone
from battles.models import BattleEvent, Team, Submission, Vote

class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными для демонстрации'

    def handle(self, *args, **kwargs):
        self.stdout.write('Очистка старых данных...')
        Vote.objects.all().delete()
        Submission.objects.all().delete()
        Team.objects.all().delete()
        BattleEvent.objects.all().delete()

        self.stdout.write('Создание баттла...')
        event = BattleEvent.objects.create(
            title='Осенний ИТ-баттл 2026',
            date=timezone.now(),
            status=BattleEvent.STATUS_VOTING
        )

        self.stdout.write('Создание команд и решений...')
        team1 = Team.objects.create(name='Lambda')
        team2 = Team.objects.create(name='Recursion')
        team3 = Team.objects.create(name='Pointers')

        sub1 = Submission.objects.create(
            team=team1, event=event,
            code_snapshot='def fizzbuzz(n):\n    return ["Fizz"*(i%3==0) + "Buzz"*(i%5==0) or i for i in range(1, n+1)]'
        )
        sub2 = Submission.objects.create(
            team=team2, event=event,
            code_snapshot='def factorial(n):\n    return 1 if n <= 1 else n * factorial(n - 1)'
        )
        sub3 = Submission.objects.create(
            team=team3, event=event,
            code_snapshot='def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr'
        )

        self.stdout.write('Добавление голосов...')
        Vote.objects.create(submission=sub1, voter_key='user_1')
        Vote.objects.create(submission=sub1, voter_key='user_2')
        Vote.objects.create(submission=sub2, voter_key='user_3')
        Vote.objects.create(submission=sub2, voter_key='user_4')
        Vote.objects.create(submission=sub3, voter_key='user_5')
        Vote.objects.create(submission=sub2, voter_key='user_6')
        Vote.objects.create(submission=sub1, voter_key='user_7')

        self.stdout.write(self.style.SUCCESS(f'Успешно! Создан баттл "{event.title}" (ID: {event.id}).'))