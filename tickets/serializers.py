from rest_framework import serializers
from tickets.models import TicketComment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    id = serializers.ReadOnlyField()
    class Meta:
        model = TicketComment
        fields = ('text', 'ticket', 'author', 'id',)
