from apps.vins.models import MIN_ANY_COLLITA, MAX_ANY_COLLITA
from apps.vins.models import Vi
from django import forms
from django.forms.widgets import ClearableFileInput

# Widgets personalitzats per a la gestió d'imatges dels vins al formulari de creació i edició
class ViImatgeWidget(ClearableFileInput): 
    template_name = 'gestio/widgets/custom_clearable_file_input.html' # Template personalitzat per a mostrar l'imatge actual i les opcions de pujar/modificar/eliminar la imatge
    initial_text = 'Imatge actual:'
    input_text = 'Pujar o modificar imatge:'
    clear_checkbox_label = 'Eliminar imatge'

#Formulari basat en model Vi
class ViForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): # Sobrescrivim el mètode __init__ 
        super().__init__(*args, **kwargs) # Cridem al mètode __init__ de la classe base per a inicialitzar el formulari
        self.fields['any_collita'].widget.attrs.update( 
            {
                'min': MIN_ANY_COLLITA,
                'max': MAX_ANY_COLLITA,
            }
        )

    def clean_any_collita(self):
        any_collita = self.cleaned_data.get('any_collita') # Obtenim el valor de l'any de collita del formulari després de la validació bàsica

        if any_collita is None:
            return any_collita

        if any_collita < MIN_ANY_COLLITA or any_collita > MAX_ANY_COLLITA:
            raise forms.ValidationError(
                f"L'any de col·lita ha d'estar entre {MIN_ANY_COLLITA} i {MAX_ANY_COLLITA}."
            )

        return any_collita

    class Meta:
        model = Vi # El formulari està basat en el model Vi
        fields = [ # Camps del model que volem incloure al formulari
            'nom',
            'origen',
            'tipus',
            'preu',
            'stock',
            'any_collita',
            'imatge',
            'descripcio',
            'es_actiu',
        ]
        widgets = { # Widgets personalitzats per a alguns camps del formulari
            'descripcio': forms.Textarea(attrs={'rows': 4}),
            'imatge': ViImatgeWidget(),
            'es_actiu': forms.CheckboxInput(),
        }
