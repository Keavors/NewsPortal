from django import forms
from .models import Post
from django import forms
from .models import User

class TimezoneForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['timezone']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.post_type == 'news':
            self.instance.clean()  # Вызов метода валидации модели
        return cleaned_data