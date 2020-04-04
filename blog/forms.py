from django import forms

from blog.models import Comment, Post
from category.models import Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from subcategory.models import SubCategory


class PostForm(forms.ModelForm):
    """Form definition for Post."""

    class Meta:
        """Meta definition for Postform."""
        long_description = forms.CharField(widget=CKEditorUploadingWidget(
            attrs={'required': False}))

        model = Post
        fields = ('author', 'main_title', 'slug', 'news_pic', 'video_link',
                  'short_description', 'long_description', 'category', 'sub_category')

        widgets = {
            "author": forms.HiddenInput()

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(
                    category_id=category_id).order_by('sub_title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sub_category'].queryset = self.instance.category.subcategory_set.order_by(
                'sub_title')


class SearchForm(forms.Form):
    q = forms.CharField()


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields = ('content', )
