from django.shortcuts import render, get_object_or_404, redirect
from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.contrib.auth import login
from .forms import RegisterForm
from .serializers import DiaryEntrySerializer
from rest_framework import viewsets

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'DiaryApp/register.html', {'form': form})

def index(request):
    entries = DiaryEntry.objects.all().order_by('-created_at')
    return render(request, 'DiaryApp/index.html', {'entries': entries})

def entry_detail(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    return render(request, 'DiaryApp/entry_detail.html', {'entry': entry})

def create_entry(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DiaryEntryForm()
    return render(request, 'DiaryApp/entry_form.html', {'form': form})

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

def delete_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('index')
    return render(request, 'DiaryApp/delete_confirm.html', {'entry': entry})

class DiaryEntryViewSet(viewsets.ModelViewSet):
    queryset = DiaryEntry.objects.all()
    serializer_class = DiaryEntrySerializer