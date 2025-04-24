from django.shortcuts import render, get_object_or_404, redirect
from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import DiaryEntrySerializer

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'DiaryApp/register.html', {'form': form})

@login_required
def index(request):
    entries = DiaryEntry.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'DiaryApp/index.html', {'entries': entries})

@login_required
def entry_detail(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    return render(request, 'DiaryApp/entry_detail.html', {'entry': entry})

@login_required
def create_entry(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('index')
    else:
        form = DiaryEntryForm()
    return render(request, 'DiaryApp/entry_form.html', {'form': form})


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись обновлена.')
            return redirect('entry_detail', entry_id=entry.id)
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'DiaryApp/entry_form.html', {'form': form})

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Запись удалена.')
        return redirect('index')
    return render(request, 'DiaryApp/delete_confirm.html', {'entry': entry})

class DiaryEntryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DiaryEntrySerializer

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)
