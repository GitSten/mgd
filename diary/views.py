from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import DiaryEntry
from .forms import DiaryEntryForm

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.db import IntegrityError


@login_required
def entry_list(request):
    """
    View to display a list of diary entries specific to the logged-in user.
    """
    # Filter entries by the logged-in user
    entries = DiaryEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'diary/entry_list.html', {'entries': entries})


@login_required  # Ensure the user is logged in
def add_entry(request):
    if request.method == "POST":
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            diary_entry = form.save(commit=False)  # Don't save the form immediately
            diary_entry.user = request.user  # Associate the entry with the currently logged-in user
            diary_entry.save()  # Now save the diary entry
            return redirect('diary:entry_list')
    else:
        form = DiaryEntryForm()
    return render(request, 'diary/add_entry.html', {'form': form})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('diary:login')  # Ensure you're using the correct namespace and view name
    template_name = 'signup.html'

    def form_valid(self, form):
        try:
            # This is where the user record is actually saved. If the username is unique, it should succeed.
            return super().form_valid(form)
        except IntegrityError:
            # If a username clash occurs, add an error message on the username field
            form.add_error('username', 'This username is already taken. Please choose another.')
            return render(self.request, self.template_name, {'form': form})


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, pk=entry_id,
                              user=request.user)  # Ensure the entry belongs to the logged-in user
    if request.method == "POST":
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('diary:entry_list')  # Redirect to the entry list page
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'diary/edit_entry.html', {'form': form, 'entry': entry})

@login_required
def blog(request):
    return render(request, 'comingsoon.html')

@login_required
def recipes(request):
    return render(request, 'comingsoon.html')


@require_POST
def delete_entry(request, entry_id):
    entry = DiaryEntry.objects.get(pk=entry_id)
    # Ensure the user requesting the delete owns the entry
    if entry.user == request.user:
        entry.delete()
    return redirect('diary:entry_list')