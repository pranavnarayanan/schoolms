from django import forms
from apps.documents.models import EN_Documents
class documentform(forms.Form):
    file=forms.FileField()