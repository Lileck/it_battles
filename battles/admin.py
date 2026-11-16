from django.contrib import admin
from .models import BattleEvent, Team, Submission, Vote

admin.site.register(BattleEvent)
admin.site.register(Team)
admin.site.register(Submission)
admin.site.register(Vote)