from django.shortcuts import render, get_object_or_404, redirect
from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.contrib.auth import login
from .forms import RegisterForm
from .serializers import DiaryEntrySerializer
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'DiaryApp/register.html', {'form': form})

@login_required
def index(request):
    entries = DiaryEntry.objects.all().order_by('-created_at')
    return render(request, 'DiaryApp/index.html', {'entries': entries})

@login_required
def entry_detail(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    return render(request, 'DiaryApp/entry_detail.html', {'entry': entry})

@login_required
def create_entry(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DiaryEntryForm()
    return render(request, 'DiaryApp/entry_form.html', {'form': form})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entry_detail', entry_id=entry.id)  # <-- важная часть
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'DiaryApp/entry_form.html', {'form': form})

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('index')
    return render(request, 'DiaryApp/delete_confirm.html', {'entry': entry})

class DiaryEntryViewSet(viewsets.ModelViewSet):
    queryset = DiaryEntry.objects.all()
    serializer_class = DiaryEntrySerializer