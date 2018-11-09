from django import forms
from apps.users.models import EN_Contacts

class FORM_LoginDetails(forms.Form) :
    username = forms.CharField(min_length=4, max_length=20, required=True)
    password = forms.CharField(min_length=5, max_length=20, required=True)
    def clean(self):
        data = self.cleaned_data
        username = data["username"]
        password = data["password"]
        if username == None:
            self.add_error("username", "Username is required")
        if password == None:
            self.add_error("password", "Password is required")
        return data

class FORM_ResetPassword(forms.Form) :
    email = forms.CharField (max_length=30, min_length=6, required=True)
    def clean(self):
        data = self.cleaned_data
        email = data["email"]
        if email == None:
            self.add_error("email", "Email is required")
        else:
            try:
                EN_Contacts.objects.get(email_id=email)
            except:
                self.add_error("email", "Entered EmailId Is Not Registered With Myshishya")
        return data