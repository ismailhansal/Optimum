from django.db import models
from django.contrib.auth.models import User


# Create your models here.


from django.db import models

class Departement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nom




    




class Poste(models.Model):
    fonction = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)


    def __str__(self):
        return self.fonction
    

class Employee(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    poste = models.ForeignKey(Poste, on_delete=models.SET_NULL, null=True)  # Utilisation de ForeignKey avec Poste
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}-{self.poste}"


class Certification(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_obtention = models.DateField()
    fichier = models.FileField(upload_to='certifications/')
    technologies_utilisees = models.CharField(max_length=255, blank=True)  # Champ pour les technologies utilisées
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Champ pour lier la certification à un employé



    def __str__(self):
        return f"{self.nom} {self.technologies_utilisees} {self.date_obtention}"
    





class Projet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_realisation = models.DateField()
    fichier = models.FileField(upload_to='projets/')
    technologies_utilisees = models.CharField(max_length=255, blank=True)  # Champ pour les technologies utilisées
    employe = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Champ pour lier la certification à un employé



    def __str__(self):
        return f"{self.nom} {self.technologies_utilisees} {self.date_realisation}"
    



class EquipeProjet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_debut = models.DateField()
    employes = models.ManyToManyField('Employee', related_name='equipes_projet')



 


   