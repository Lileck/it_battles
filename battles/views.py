from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from pygments.formatters import HtmlFormatter
from .forms import SubmissionForm
from .models import BattleEvent, Submission


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