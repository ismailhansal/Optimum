from django import forms
from .models import Employee, EquipeProjet




class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['nom', 'prenom', 'date_naissance', 'poste', 'departement', 'adresse', 'telephone', 'email']



class EquipeProjetForm(forms.ModelForm):
    class Meta:
        model = EquipeProjet
        fields = ['nom', 'description', 'date_debut']  # Les champs que vous souhaitez permettre de modifier
