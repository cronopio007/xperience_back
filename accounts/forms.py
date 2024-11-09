from django import forms 
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter Password',
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirma Password',
    }))
    class Meta:
        model =Account
        # los campos son los nombres de las variables de models.py
        fields = ['first_name', 'last_name','phone_number','email','password']

        # les da a todos los de fields la clase 'from-control' para que use su css y se vea bien
    def __init__(self, *args, **kwargs):
            super(RegistrationForm, self).__init__(*args, **kwargs)
            # ejemplo de modificacion de la clase de 1 elemento
            self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'
    
    def clean(self):
         cleaned_data = super(RegistrationForm, self).clean()
         password = cleaned_data.get('password')
         confirm_password = cleaned_data.get('confirm_password')

         if password != confirm_password:
              raise forms.ValidationError(
                   'password and confirm password should be same')