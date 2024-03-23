from django import forms
from .models import DiaryEntry, Trigger


class DiaryEntryForm(forms.ModelForm):
    triggers = forms.ModelMultipleChoiceField(
        queryset=Trigger.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = DiaryEntry
        fields = ['date', 'intensity', 'triggers', 'symptoms', 'notes', 'other_triggers']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'intensity': forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '10', 'class': 'form-control-range'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List your symptoms'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional notes'}),
            'other_triggers': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Other triggers'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            initial['triggers'] = instance.triggers.all()
            kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    # If you need to do any custom processing or validation, add it here
    # For example:
    def clean_intensity(self):
        intensity = self.cleaned_data.get('intensity')
        if not (1 <= intensity <= 10):
            raise forms.ValidationError('Intensity must be between 1 and 10.')
        return intensity

    # More custom methods can be added if needed