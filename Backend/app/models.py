from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import UUID, Text, DateTime
import uuid
from datetime import datetime


class User(Model):
    username = Text(primary_key=True)
    password = Text(required=True)
    last_active = DateTime(default=datetime.now)


class Room(Model):
    room_id = UUID(primary_key=True, default=uuid.uuid4)
    name = Text(required=True)
    created_at = DateTime(default=datetime.now)


class Message(Model):
    room_id = UUID(partition_key=True)
    created_at = DateTime(
        primary_key=True, clustering_order="ASC", default=datetime.now
    )
    message_id = UUID(default=uuid.uuid4)
    username = Text(required=True)
    content = Text(required=True)


class RoomUser(Model):
    room_id = UUID(partition_key=True)
    username = Text(primary_key=True)
    joined_at = DateTime(default=datetime.now)
