from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import FraudAlert


@login_required
def alert_list(request):
    alerts = FraudAlert.objects.filter(user=request.user)
    open_count = alerts.filter(is_resolved=False).count()
    resolved_count = alerts.filter(is_resolved=True).count()

    return render(request, 'alerts/alert_list.html', {
        'alerts': alerts,
        'open_count': open_count,
        'resolved_count': resolved_count,
    })


@login_required
def alert_resolve(request, pk):
    alert = get_object_or_404(FraudAlert, pk=pk, user=request.user)
    if request.method == 'POST':
        alert.is_resolved = True
        alert.save(update_fields=['is_resolved', 'updated_at'])
        messages.success(request, 'Alert marked as resolved.')
    return redirect('alert_list')
