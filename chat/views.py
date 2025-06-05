from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message


User = get_user_model()


def _room_name(user1, user2):
    ids = sorted([user1.id, user2.id])
    return f'{ids[0]}_{ids[1]}'


@login_required
def room(request, nickname):
    other_user = get_object_or_404(User, nickname=nickname)
    room_name = _room_name(request.user, other_user)
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    room.participants.add(request.user, other_user)
    messages = room.messages.all()
    return render(
        request,
        'chat/room.html',
        {'room_name': room_name, 'other_user': other_user, 'messages': messages},
    )
