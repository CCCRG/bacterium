from django import forms
from cub.models import Edge

class EdgeForm(forms.ModelForm):
    class Meta:
        model = Edge
        fields = '__all__'
