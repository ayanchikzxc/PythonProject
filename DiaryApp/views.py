from django.shortcuts import render, get_object_or_404, redirect
from .models import DiaryEntry
from .forms import DiaryEntryForm

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
            return redirect('entry_detail', entry_id=entry.id)
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'DiaryApp/entry_form.html', {'form': form})

def delete_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('index')
    return render(request, 'DiaryApp/delete_confirm.html', {'entry': entry})
