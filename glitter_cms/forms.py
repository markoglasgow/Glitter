from django import forms
from glitter_cms.models import Comment, Post, Category

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        max_length=255,
        help_text="Enter your reply",
        widget=forms.TextInput(attrs={'class' : 'form-control reply_input', 'placeholder': 'Enter your reply...'})
    )

    class Meta:
        model = Comment

        exclude = ('user', 'post', 'timestamp', 'likes_count')

class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class' : 'form-control reply_input', 'placeholder': 'Enter Title'})
    )
    body = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class' : 'form-control reply_input', 'placeholder': 'Enter Post Text'})
    )
    tags = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class' : 'form-control reply_input', 'placeholder': 'Enter Tags'})
    )
    # category = forms.ModelMultipleChoiceField(
    #     queryset=Category.objects.all().values_list('name'),
    #     widget=forms.CheckboxSelectMultiple(attrs={'class': 'post_list'})
    # )

    category = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control reply_input', 'placeholder': 'Enter List of Categories'})
    )

    class Meta:
        model = Post
        fields = ['title', 'tags', 'body', 'category']
        exclude = ('user', 'timestamp', 'likes_count', 'view_count', 'reply_count')