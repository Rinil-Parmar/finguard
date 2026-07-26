from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SavingsGoalForm
from .models import SavingsGoal


@login_required
def savings_goal_list(request):
    goals = SavingsGoal.objects.filter(user=request.user)
    active_goals = goals.filter(is_completed=False)
    completed_goals = goals.filter(is_completed=True)

    return render(request, 'savings/savings_goal_list.html', {
        'goals': goals,
        'active_count': active_goals.count(),
        'completed_count': completed_goals.count(),
    })


@login_required
def savings_goal_create(request):
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Savings goal added successfully.')
            return redirect('savings_goal_list')
    else:
        form = SavingsGoalForm()

    return render(request, 'savings/savings_goal_form.html', {
        'form': form,
        'page_title': 'Add savings goal',
        'button_label': 'Save goal',
    })


@login_required
def savings_goal_update(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Savings goal updated successfully.')
            return redirect('savings_goal_list')
    else:
        form = SavingsGoalForm(instance=goal)

    return render(request, 'savings/savings_goal_form.html', {
        'form': form,
        'page_title': 'Edit savings goal',
        'button_label': 'Update goal',
    })


@login_required
def savings_goal_delete(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Savings goal deleted successfully.')
        return redirect('savings_goal_list')

    return render(request, 'savings/savings_goal_confirm_delete.html', {'goal': goal})
