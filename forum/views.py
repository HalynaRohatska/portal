from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from .models import Thread, Message

def is_moderator_or_admin(user):
    return user.is_staff or user.is_superuser

def forum_index(request):
    threads = Thread.objects.all().order_by('-created_at')
    return render(request, 'forum/index.html', {'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    messages = thread.messages.all().order_by('created_at')
    return render(request, 'forum/thread_detail.html', {'thread': thread, 'messages': messages})

@login_required
def create_message(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        text = request.POST.get('text', '')
        message = Message(thread=thread, text=text, author=request.user)
        try:
            message.full_clean()
            message.save()
        except ValidationError as e:
            return render(request, 'forum/thread_detail.html', {
                'thread': thread, 
                'messages': thread.messages.all(),
                'error': e.messages
            })
    return redirect('forum:thread_detail', thread_id=thread.id)

@login_required
@user_passes_test(is_moderator_or_admin)
def create_thread(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        thread = Thread(title=title, author=request.user)
        try:
            thread.full_clean()
            thread.save()
            return redirect('forum:forum_index')
        except ValidationError as e:
            return render(request, 'forum/create_thread.html', {'error': e.messages})
    return render(request, 'forum/create_thread.html')

@login_required
@user_passes_test(is_moderator_or_admin)
def delete_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    thread.delete()
    return redirect('forum:forum_index')
