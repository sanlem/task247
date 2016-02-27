from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegistrationForm(UserCreationForm):
    class Meta:
        fields = ['username', 'email', 'password1', 'password2']
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'class': 'form-control'
                })
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        # new users should be activated by admin
        user.is_active = False
        if commit:
            user.save()
        return user
