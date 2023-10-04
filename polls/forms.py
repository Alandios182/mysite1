from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Choice

# Create your forms here.

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
      
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']  # Añade otros campos si es necesario

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text','suspended']  # Añade otros campos si es necesario

ChoiceFormSet = forms.inlineformset_factory(Question, Choice, form=ChoiceForm, extra=1, can_delete=True)
	
	