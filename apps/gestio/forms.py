from datetime import date
from django import forms
from django.forms.widgets import ClearableFileInput

from apps.vins.models import Vi


class ViImatgeWidget(ClearableFileInput):
    template_name = 'gestio/widgets/custom_clearable_file_input.html'
    initial_text = 'Imatge actual:'
    input_text = 'Pujar o modificar imatge:'
    clear_checkbox_label = 'Eliminar imatge'


class ViForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        any_actual = date.today().year
        self.fields['any_collita'].widget.attrs.update(
            {
                'min': 1800,
                'max': any_actual,
            }
        )

    def clean_any_collita(self):
        any_collita = self.cleaned_data.get('any_collita')
        any_actual = date.today().year

        if any_collita is None:
            return any_collita

        if any_collita < 1800 or any_collita > any_actual:
            raise forms.ValidationError(
                f"L'any de col·lita ha d'estar entre 1800 i {any_actual}."
            )

        return any_collita

    class Meta:
        model = Vi
        fields = [
            'nom',
            'origen',
            'tipus',
            'preu',
            'stock',
            'any_collita',
            'imatge',
            'descripcio',
        ]
        widgets = {
            'descripcio': forms.Textarea(attrs={'rows': 4}),
            'imatge': ViImatgeWidget(),
        }
