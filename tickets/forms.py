from django import forms
from tickets.models import Ticket, TicketComment, Attachment


class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        widgets = {
        	'description': forms.Textarea(attrs={'rows': 5})
        }
        fields = ['name', 'points', 'owner', 'goal', 'status', 'priority', 'description']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'class': 'form-control'
                })	
	

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['attachment', 'name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }