from .models import Message

def unread_message_indicator(request):
    if not request.user.is_authenticated:
        return {'has_unread_messages': False}

    last_read = getattr(request.user, 'last_message_read_time', None)
    qs = Message.objects.filter(room__participants=request.user).exclude(sender=request.user)
    if last_read:
        qs = qs.filter(timestamp__gt=last_read)
    has_unread = qs.exists()
    return {'has_unread_messages': has_unread}
