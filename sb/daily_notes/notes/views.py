from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def scrapbook(request):
    notes = Note.objects.filter(user1=request.user).union(Note.objects.filter(user2=request.user)).union(Note.objects.filter(last_editor=request.user)).order_by('-date')  # Use '-last_updated' to order by last updated date
    return render(request, 'notes/scrapbook.html', {'notes': notes, 'current_year': timezone.now().year})
@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.content = request.POST['content']
        note.last_editor = request.user
        note.save()
        messages.success(request, 'Note updated successfully!')
        return redirect('scrapbook')
    return render(request, 'notes/edit_note.html', {'note': note})

def register_page_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'registration/register.html')

        user = User.objects.create_user(username=username,  password=password)
        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')
    return render(request, 'registration/register.html')

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('scrapbook')
    return render(request, 'notes/delete_note.html', {'note': note})

@login_required
def create_note(request):
    if request.method == 'POST':
        content = request.POST['content']
        user2_id = request.POST.get('user2')  # Get the selected user ID

        try:
            user2 = User.objects.get(id=user2_id)  # Get the user2 object
        except User.DoesNotExist:
            messages.error(request, "The selected user does not exist.")
            return redirect('create_note')  # Redirect back to the create note page

        note = Note(user1=request.user, user2=user2, content=content)  # Assign the logged-in user as user1
        note.save()
        messages.success(request, 'Note created successfully!')
        return redirect('scrapbook')

    # Get a list of users to share notes with (for user2 selection)
    users = User.objects.exclude(id=request.user.id)  # Exclude the logged-in user
    return render(request, 'notes/create_note.html', {'users': users})

