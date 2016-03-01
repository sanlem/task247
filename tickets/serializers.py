from rest_framework import serializers
from tickets.models import TicketComment, Attachment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    id = serializers.ReadOnlyField()
    class Meta:
        model = TicketComment
        fields = ('text', 'ticket', 'author', 'id',)


class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField(source='attachment.url')
    ticket = serializers.ReadOnlyField(source='ticket.id')
    id = serializers.ReadOnlyField()
    class Meta:
        model = Attachment
        fields = ('id', 'name', 'url', 'ticket',)
