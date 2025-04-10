from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry
from .forms import EntryForm

def index(request):
    entries = Entry.objects.all()
    return render(request, 'DiaryApp/index.html', {'entries': entries})

def view_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    return render(request, 'DiaryApp/entry_detail.html', {'entry': entry})

def create_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = EntryForm()
    return render(request, 'DiaryApp/entry_form.html', {'form': form, 'form_title': "Create New Entry"})

def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('view_entry', entry_id=entry.id)
    else:
        form = EntryForm(instance=entry)
    return render(request, 'DiaryApp/entry_form.html', {'form': form, 'form_title': "Edit Entry"})

def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == "POST":
        entry.delete()
        return redirect('index')
    return render(request, 'DiaryApp/entry_detail.html', {'entry': entry})


