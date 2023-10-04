from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Address
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import Address
# Create your forms here.
	
class CustomUserChangeForm(UserChangeForm):
	password = forms.CharField(widget=forms.PasswordInput(),required= False) 
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'password']  
		
	def save(self, commit=True):
		user = super(CustomUserChangeForm, self).save(commit=commit) 
		password = self.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		return user
		
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'postal_code']  # Ajusta los campos según tu modelo Address

   
	
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user

