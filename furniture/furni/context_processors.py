from .models import Room


def room_types(requestr):
    rooms = Room.objects.all()
    return {'rooms': rooms}