from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from django.utils import timezone


User = get_user_model()


def _room_name(user1, user2):
    ids = sorted([user1.id, user2.id])
    return f'{ids[0]}_{ids[1]}'


@login_required
def chat_list(request):
    search_query = request.GET.get('q')
    rooms = ChatRoom.objects.filter(participants=request.user)
    room_info = []
    for room in rooms:
        other = room.participants.exclude(id=request.user.id).first()
        if other:
            room_info.append({'room': room, 'user': other})

    search_results = None
    if search_query:
        search_results = (
            User.objects.filter(nickname__icontains=search_query)
            .exclude(id=request.user.id)
        )

    request.user.last_message_read_time = timezone.now()
    request.user.save(update_fields=['last_message_read_time'])

    context = {
        'rooms': room_info,
        'search_results': search_results,
        'query': search_query,
    }

    return render(request, 'chat/list.html', context)


@login_required
def room(request, nickname):
    other_user = get_object_or_404(User, nickname=nickname)
    room_name = _room_name(request.user, other_user)
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    room.participants.add(request.user, other_user)
    messages = room.messages.all()
    request.user.last_message_read_time = timezone.now()
    request.user.save(update_fields=['last_message_read_time'])
    return render(
        request,
        'chat/room.html',
        {'room_name': room_name, 'other_user': other_user, 'messages': messages},
    )
