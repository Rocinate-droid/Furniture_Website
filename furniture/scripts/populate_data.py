# Now you can safely import your models
from furni.models import Room  # Replace with your app/model

room_names = [
    "Living Room",
    "Bed Room",
    "Dining Room",
    "Home Office",
    "Plastic Chairs",
    "Kitchen",
    "Decor",
    "Mattress",
    "Kids",
    "Pots and Plants"
]

for name in room_names:
    Room.objects.create(name=name)

print("Data inserted successfully.")