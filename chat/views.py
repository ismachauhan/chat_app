from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
from datetime import datetime  # ✅ required for datetime.min


@login_required
def chat_room(request, room_name):
    search_query = request.GET.get('search', '') 

    # Exclude the current user from the user list
    users = User.objects.exclude(id=request.user.id) 

    # Fetch messages between the logged-in user and the user in the URL (room_name)
    chats = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=room_name)) |
        (Q(receiver=request.user) & Q(sender__username=room_name))
    )

    # If a search query is provided, filter messages by content
    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))  

    # Sort the chats by timestamp (oldest to newest)
    chats = chats.order_by('timestamp') 

    user_last_messages = []

    # For each user (excluding self), get their last message with the logged-in user
    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    # ✅ FIXED: Sort by last_message timestamp, using datetime.min if None
    user_last_messages.sort(
        key=lambda x: x['last_message'].timestamp if x['last_message'] else datetime.min,
        reverse=True
    )

    return render(request, 'chat.html', {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query 
    })
