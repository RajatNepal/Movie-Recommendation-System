from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment



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



# Create array that holds possible choices
RATING_CHOICES=[('-1','dislike'),
         ('0','did not see'),
		 ('1','like')]


class RateMoviesForm(forms.Form):
	# Default widget style is dropdown, so I changed it to radio button
	movie1 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label = 'The Dark Knight')
	movie2 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label = '3 Idiots')
	movie3 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label = 'Frozen')
	movie4 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label = 'Django Unchained')
	movie5 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label = 'Titanic')
	movie6 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label = 'Star Wars Episode IV - A New Hope')
	movie7 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label = 'Inception')
	movie8 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label = '2001: A Space Odyssey')
	movie9 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label = 'The Matrix')
	movie10 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect, label = 'Back to the Future')

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)

	
	


	