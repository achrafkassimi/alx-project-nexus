import graphene
from graphene_django.types import DjangoObjectType
from chat.models import Message
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")

class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = ("id", "sender", "receiver", "content", "timestamp")

class Query(graphene.ObjectType):
    messages = graphene.List(MessageType, other_user_id=graphene.Int(required=True))

    def resolve_messages(self, info, other_user_id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication required")

        return Message.objects.filter(
            models.Q(sender=user, receiver_id=other_user_id) |
            models.Q(sender_id=other_user_id, receiver=user)
        ).order_by("timestamp")

class SendMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        receiver_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, receiver_id, content):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication required")
        msg = Message.objects.create(sender=user, receiver_id=receiver_id, content=content)
        return SendMessage(message=msg)

class Mutation(graphene.ObjectType):
    send_message = SendMessage.Field()


