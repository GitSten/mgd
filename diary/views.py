from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import DiaryEntry, Trigger
from .forms import DiaryEntryForm

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.db import IntegrityError


@login_required
def entry_list(request):
    entry_list = DiaryEntry.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(entry_list, 7)  # Show 7 entries per page

    page_number = request.GET.get('page')
    entries = paginator.get_page(page_number)

    return render(request, 'diary/entry_list.html', {'entries': entries})


@login_required
def add_entry(request):
    if request.method == "POST":
        form = DiaryEntryForm(request.POST, request.FILES)
        if form.is_valid():
            diary_entry = form.save(commit=False)
            diary_entry.user = request.user
            diary_entry.save()
            form.save_m2m()  # Save the many-to-many data for the form.
            return redirect('diary:entry_list')  # Adjust the redirect as needed
    else:
        form = DiaryEntryForm()
    triggers_with_icons = Trigger.objects.all()
    return render(request, 'diary/add_entry.html', {'form': form, 'triggers_with_icons': triggers_with_icons})




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
    entry = get_object_or_404(DiaryEntry, pk=entry_id, user=request.user)
    if request.method == "POST":
        form = DiaryEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('diary:entry_list')  # Adjust the redirect as needed
    else:
        form = DiaryEntryForm(instance=entry)
    triggers_with_icons = Trigger.objects.all()
    # Create a set of trigger IDs associated with the entry
    trigger_ids = set(entry.triggers.values_list('id', flat=True))
    return render(request, 'diary/edit_entry.html', {'form': form, 'entry': entry, 'triggers_with_icons': triggers_with_icons, 'trigger_ids': trigger_ids})





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
