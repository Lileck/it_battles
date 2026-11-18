from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from pygments.formatters import HtmlFormatter
from .forms import SubmissionForm
from .models import BattleEvent, Submission
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Vote
from django.views.decorators.csrf import csrf_exempt


def submit_solution(request, event_id):
    event = get_object_or_404(BattleEvent, id=event_id)

    if event.status != BattleEvent.STATUS_ACTIVE:
        messages.error(request, 'Приём решений закрыт.')
        return render(request, 'battles/submit.html', {'event': event, 'form': None})

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            team = form.cleaned_data['team']
            code = form.cleaned_data['code_snapshot']


            submission = Submission.objects.filter(team=team, event=event).first()
            if submission:
                submission.code_snapshot = code
                submission.save()
                messages.success(request, 'Решение обновлено.')
            else:
                Submission.objects.create(team=team, event=event, code_snapshot=code)
                messages.success(request, 'Решение принято.')

            return redirect('submit_solution', event_id=event.id)
    else:
        form = SubmissionForm()

    return render(request, 'battles/submit.html', {'event': event, 'form': form})
def host_dashboard(request, event_id):
    event = get_object_or_404(BattleEvent, id=event_id)
    return render(request, 'battles/host.html', {'event': event})


def results_fragment(request, event_id):
    event = get_object_or_404(BattleEvent, id=event_id)
    submissions = event.submission_set.all()


    for sub in submissions:
        sub.vote_count = sub.vote_set.count()

    submissions = sorted(submissions, key=lambda s: s.vote_count, reverse=True)


    pygments_css = HtmlFormatter(style='monokai').get_style_defs('.highlight')

    return render(request, 'battles/results.html', {
        'event': event,
        'submissions': submissions,
        'pygments_css': pygments_css,
    })
def vote_page(request, event_id):
    event = get_object_or_404(BattleEvent, id=event_id)

    if event.status != BattleEvent.STATUS_VOTING:
        return render(request, 'battles/vote_closed.html', {'event': event})

    if not request.session.session_key:
        request.session.create()
    voter_key = request.session.session_key

    submissions = event.submission_set.all()


    for sub in submissions:
        sub.has_voted = Vote.objects.filter(
            submission=sub,
            voter_key=voter_key,
        ).exists()

    return render(request, 'battles/vote.html', {
        'event': event,
        'submissions': submissions,
    })

@csrf_exempt
@require_POST
def cast_vote(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    event = submission.event

    if event.status != BattleEvent.STATUS_VOTING:
        return HttpResponse('<div class="badge">Голосование закрыто</div>')

    if not request.session.session_key:
        request.session.create()
    voter_key = request.session.session_key

    already_voted = Vote.objects.filter(
        submission__event=event,
        voter_key=voter_key,
    ).exists()

    if already_voted:
        return HttpResponse('<div class="badge">Вы уже голосовали</div>')

    Vote.objects.create(submission=submission, voter_key=voter_key)
    return HttpResponse('<div class="badge">Голос учтён!</div>')