from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(
        label='Vaše meno',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Meno Priezvisko'
        })
    )

    phone = forms.CharField(
        label='Telefón',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+421XXXXXX'
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@gmail.com'
        })
    )  

class ContactForm(forms.Form):
    name2 = forms.CharField()
    email2 = forms.EmailField()
    message2 = forms.CharField(widget=forms.Textarea)