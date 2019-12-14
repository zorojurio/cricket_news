from django import forms
from blog.models import Post, Comment, Category, SubCategory


class PostForm(forms.ModelForm):
    """Form definition for Post."""

    class Meta:
        """Meta definition for Postform."""

        model = Post
        fields = ('author', 'main_title', 'news_pic', 'video_link',
                  'short_description', 'long_description', 'category', 'sub_category')

        widgets = {
            'sub_title': forms.TextInput(attrs={'class': 'textinputclass medium-editor-textarea'}),
            'short_description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
            'long_description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea',
                                                      'rows': '50', 'cols': '50', 'id': 'editor',
                                                      }),
            "author": forms.HiddenInput()

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = SubCategory.objects.none()
        
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('sub_title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sub_category'].queryset = self.instance.category.subcategory_set.order_by('sub_title')




class CommentForm(forms.ModelForm):
    """Form definition for Comment."""

    class Meta:
        """Meta definition for Commentform."""

        model = Comment
        fields = ('author', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
