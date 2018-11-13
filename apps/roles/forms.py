import re
from django import forms
from displaykey.display_key import DisplayKey

class FORM_UserRoleAssignment(forms.Form):

    product_ids = forms.CharField(
        widget=forms.Textarea,
        required=True
    )

    def clean(self):
        data = self.cleaned_data
        prdIdListString = (data["product_ids"].replace(" ", "")).strip()
        if (re.match('^[MY0-9,]+$',prdIdListString) == None):
            self.add_error("product_ids", DisplayKey.get("invalid_characters_in_product_id_list"))
        return data