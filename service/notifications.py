from content.models import Notification


def mark_read(notification, is_read=True):
    notification.is_read = is_read
    notification.save(update_fields=["is_read"])
    return notification


def mark_all_read(user):
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)


