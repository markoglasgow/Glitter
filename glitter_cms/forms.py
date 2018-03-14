from django import forms
from glitter_cms.models import Comment

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        max_length=255,
        help_text="Enter your reply",
        widget=forms.TextInput(attrs={'class' : 'form-control reply_input', 'placeholder': 'Enter your reply...'})
    )

    class Meta:
        model = Comment

        exclude = ('user', 'post', 'timestamp', 'likes_count')