from django import forms
from .models import items, gallery, cms, all_settings, testimonial, specialoffers, category, SubItems, gallery, AdminProfile


class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = '__all__'

class ItemForm(forms.ModelForm):

    class Meta:
        model = items
        fields = '__all__'
        # fields = ("image", "category_id")

class SubItemForm(forms.ModelForm):
    class Meta:
        model = SubItems
        fields = '__all__'

class GalleryForm(forms.ModelForm):
    class Meta:
        model = gallery
        fields = '__all__'

class ContentForm(forms.ModelForm):
    class Meta:
        model = cms
        fields = '__all__'

class AllSettingForm(forms.ModelForm):
    class Meta:
        model = all_settings
        fields = '__all__'

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = testimonial
        fields = '__all__'

class SpecialForm(forms.ModelForm):
    class Meta:
        model = specialoffers
        fields = '__all__'

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = '__all__'