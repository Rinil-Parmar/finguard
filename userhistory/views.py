from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import UserActivity


@login_required
def history_detail(request):
    activities = UserActivity.objects.filter(user=request.user)[:25]
    visit_count = request.session.get('visit_count', 0)
    previous_visit = request.session.get('previous_visit')

    return render(request, 'userhistory/history_detail.html', {
        'activities': activities,
        'visit_count': visit_count,
        'previous_visit': previous_visit,
    })
