from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q, Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import json
import logging

from .models import DiaryEntry
from .forms import DiaryEntryForm
from .serializers import DiaryEntrySerializer

logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # После регистрации - не логиним автоматически
            messages.success(request, 'Вы успешно зарегистрировались! Теперь войдите в систему.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'DiaryApp/register.html', {'form': form})

@login_required
def index(request):
    query = request.GET.get('q')
    mood_filter = request.GET.get('mood')

    entries = DiaryEntry.objects.filter(user=request.user)

    if query:
        entries = entries.filter(Q(title__icontains=query) | Q(content__icontains=query))

    if mood_filter:
        entries = entries.filter(mood=mood_filter)

    entries = entries.order_by('-created_at')
    moods = DiaryEntry.MOOD_CHOICES

    return render(request, 'DiaryApp/index.html', {
        'entries': entries,
        'moods': moods,
        'query': query,
        'selected_mood': mood_filter,
    })

@login_required
def entry_detail(request, entry_id):
    entry = get_object_or_404(DiaryEntry, pk=entry_id, user=request.user)
    content = entry.get_decrypted_content()
    return render(request, 'DiaryApp/entry_detail.html', {'entry': entry, 'decrypted': content})

@login_required
def create_entry(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            logger.info(f"▶️ Новая запись '{entry.title}' от {request.user.username}")
            entry.save()
            return redirect('index')
    else:
        form = DiaryEntryForm()
    return render(request, 'DiaryApp/entry_form.html', {'form': form})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES, instance=entry)
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

@login_required
def mood_chart(request):
    mood_stats = DiaryEntry.objects.filter(user=request.user).values('mood').annotate(count=Count('id'))
    labels = [dict(DiaryEntry.MOOD_CHOICES)[m['mood']] for m in mood_stats]
    counts = [m['count'] for m in mood_stats]

    return render(request, 'DiaryApp/mood_chart.html', {
        'labels': json.dumps(labels),
        'counts': json.dumps(counts),
    })

class DiaryEntryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DiaryEntrySerializer

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)
