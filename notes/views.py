from .models import Note
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import User
import uuid


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(user_name=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        user = User(user_name=username, user_email=email)
        user.set_password(password)  # Hash password before saving
        user.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use .get() to avoid KeyError
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please fill in both fields.")
            return redirect('login')

        try:
            user = User.objects.get(user_name=username)
            if user.check_password(password):
                request.session['user_id'] = str(user.user_id)  # Store user session
                messages.success(request, "Login successful!")
                return redirect('home')  # Redirect to notes page
            else:
                messages.error(request, "Invalid username or password!")
        except User.DoesNotExist:
            messages.error(request, "User does not exist!")

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()  # Clear session
    messages.success(request, "Logged out successfully!")
    return redirect('login')


def home(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = User.objects.get(user_id=request.session['user_id'])
    notes = Note.objects.filter(user=user)  # Show only notes for logged-in user
    return render(request, 'home.html', {'user': user, 'notes': notes})

# @login_required
def create_note(request):
    if 'user_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user = User.objects.get(user_id=request.session['user_id'])  # Get the logged-in user

        Note.objects.create(user=user, note_title=title, note_content=content)  # Assign user
        return redirect('home')

    return render(request, 'create.html')

def edit_note(request, note_id):
    note = get_object_or_404(Note, note_id=uuid.UUID(str(note_id)))  # Convert to UUID

    if request.method == 'POST':
        note.note_title = request.POST['note_title']
        note.note_content = request.POST['note_content']
        note.save()
        return redirect('home')

    return render(request, 'edit_note.html', {'note': note})

def delete_note(request, note_id):
    note = get_object_or_404(Note, note_id=uuid.UUID(str(note_id)))
    note.delete()
    return redirect('home')