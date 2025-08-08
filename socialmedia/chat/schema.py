import graphene
from graphene_django.types import DjangoObjectType
from chat.models import Message
from django.contrib.auth import get_user_model

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
    messages = graphene.List(MessageType, user1_id=graphene.Int(required=True), user2_id=graphene.Int(required=True))

    def resolve_messages(self, info, user1_id, user2_id):
        return Message.objects.filter(
            (Q(sender_id=user1_id) & Q(receiver_id=user2_id)) |
            (Q(sender_id=user2_id) & Q(receiver_id=user1_id))
        ).order_by("timestamp")

class SendMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        receiver_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, receiver_id, content):
        sender = info.context.user
        if sender.is_anonymous:
            raise Exception("Authentication required")

        message = Message.objects.create(sender=sender, receiver_id=receiver_id, content=content)
        return SendMessage(message=message)

class Mutation(graphene.ObjectType):
    send_message = SendMessage.Field()
