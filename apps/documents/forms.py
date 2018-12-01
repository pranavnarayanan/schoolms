from django import forms

class FORM_Document(forms.Form):

    file = forms.FileField(required=True)