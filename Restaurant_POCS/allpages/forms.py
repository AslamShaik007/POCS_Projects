from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib.auth import authenticate

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = [
            "name", "email", "password",
            "mobile", "confirm_password"
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError({"password": "Password fields didn't match."})

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
        return user


# class LoginForm(forms.Form):
#     username = forms.CharField(label="Email")
#     password = forms.CharField(widget=forms.PasswordInput())

#     def clean(self):
#         cleaned_data = super().clean()
#         username = cleaned_data.get("username")
#         password = cleaned_data.get("password")
#         print("USER NAME",username)

#         if username and password:
#             self.user = authenticate(username=username, password=password)
#             print("USER",self.user)
#             if not self.user:
#                 raise forms.ValidationError("Invalid login credentials. Please try again.")

#     def get_user(self):
#         return self.user if self.is_valid() else None

class LoginForm(forms.Form):
    username = forms.CharField(label="Email or Mobile Number")
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            # Try to authenticate with email
            user = authenticate(username=username, password=password)

            if user is None:
                # If not authenticated with email, try with mobile number
                try:
                    user = CustomUser.objects.get(mobile=username)
                    user = authenticate(username=user.email, password=password)
                except CustomUser.DoesNotExist:
                    user = None

            if not user:
                raise forms.ValidationError("Invalid login credentials. Please try again.")

            self.user = user

    def get_user(self):
        return self.user if self.is_valid() else None