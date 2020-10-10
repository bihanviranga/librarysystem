from django.forms import ModelForm
from . import models

class BookForm(ModelForm):
    class Meta:
        model = models.Book
        fields = '__all__'

class AuthorForm(ModelForm):
    class Meta:
        model = models.Author
        fields = '__all__'

