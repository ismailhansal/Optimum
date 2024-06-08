from django.shortcuts import render, redirect, get_object_or_404
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import *


from django.shortcuts import render, redirect
from .forms import EmployeeForm


from django.contrib import messages


from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from .models import Employee, Certification, Projet, Departement, Poste, EquipeProjet
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect
from .models import EquipeProjet
from .forms import EquipeProjetForm














def index(request):

  context = {
    'segment'  : 'index',
    #'products' : Product.objects.all()
  }
  return render(request, "pages/index.html", context)

def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context)









def ajouter_employe(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Créez un utilisateur correspondant
                user = User.objects.create(
                    username=request.POST.get('username'),  # Utilisez le nom d'utilisateur fourni dans le formulaire
                    password=make_password(request.POST.get('password')),  # Utilisez le mot de passe fourni dans le formulaire
                    first_name=request.POST.get('prenom'),
                    last_name=request.POST.get('nom'),
                    email=request.POST.get('email'),
                )
                # Récupérez l'instance de Poste
                poste_id = request.POST.get('poste')
                poste = Poste.objects.get(id=poste_id)

                # Enregistrez l'employé dans la base de données
                employee = Employee.objects.create(
                    user=user,
                    nom=request.POST.get('nom'),
                    prenom=request.POST.get('prenom'),
                    date_naissance=request.POST.get('date_naissance'),
                    poste=poste,  # Assignez l'instance de Poste
                    departement_id=request.POST.get('departement'),
                    adresse=request.POST.get('adresse'),
                    telephone=request.POST.get('telephone'),
                    email=request.POST.get('email')
                )

                # Attribuez le rôle approprié à l'utilisateur, par exemple "employé"
                user.groups.add(Group.objects.get(name='Employes'))  # Assurez-vous d'avoir créé ce groupe au préalable

                # Redirigez l'utilisateur vers une page de confirmation ou une autre page
                return redirect('ajouter_employe')

        except IntegrityError as e:
            # Gérer l'erreur d'intégrité (par exemple, nom d'utilisateur ou email déjà existant)
            return render(request, 'pages/ajouter_employe.html', {'error': 'Erreur d\'intégrité : ' + str(e)})
        
        

    else:
        departements = Departement.objects.all()
        postes = Poste.objects.all()
        return render(request, 'pages/ajouter_employe.html', {'departements': departements, 'postes': postes})

    






def liste_employe(request):
    # Récupérez tous les employés à partir de la base de données
    employes = Employee.objects.all()
    # Passez les employés au contexte du modèle
    return render(request, 'pages/liste_employe.html', {'employes': employes})






def ajouter_projet(request):
    # Votre logique de vue ici
    if request.method == 'POST':
        # Récupérer l'utilisateur connecté
        employe = request.user.employee  # Supposant que chaque utilisateur a un profil d'employé associé

        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        date_realisation = request.POST.get('date_realisation')
        fichier = request.FILES.get('formFile')
        technologies_utilisees = request.POST.get('technologies')

        # Créer et sauvegarder la certification en l'associant à l'employé
        projet = Projet(
            nom=nom,
            description=description,
            date_realisation=date_realisation,
            fichier=fichier,
            technologies_utilisees=technologies_utilisees,
            employe=employe,  # Associez la certification à l'employé récupéré
        )
        projet.save()
    return render(request, 'pages/ajouter_projet.html')


   
def composer_equipe(request):
    if request.method == 'POST':
        type_application = request.POST.get('type_application')
        keywords = request.POST.get('keywords').split(', ')
        nom = request.POST.get('nom')
        description_projet = request.POST.get('description_projet')
        date_debut_projet = request.POST.get('date_debut_projet')
        besoin_chef_projet = 'besoin_chef_projet' in request.POST
        besoin_consultant = 'besoin_consultant' in request.POST
        nombre_employes_demandes = int(request.POST.get('nombre_employes', 1))

        employes_avec_info = []

        for employe in Employee.objects.all():
            certifie = any(keyword in employe.certification_set.values_list('technologies_utilisees', flat=True) for keyword in keywords)
            a_travaille = any(keyword in employe.projet_set.values_list('technologies_utilisees', flat=True) for keyword in keywords)
            fonction_correspond = False
            
            if type_application == 'Application Web':
                fonction_correspond = 'Développeur Web' in employe.poste.fonction
            elif type_application == 'Mobile':
                fonction_correspond = 'Développeur Mobile' in employe.poste.fonction
            elif type_application == 'Desktop':
                fonction_correspond = 'Développeur Desktop' in employe.poste.fonction
            
            # Vérifier si l'employé répond aux critères
            if (certifie or a_travaille) and fonction_correspond:
                employes_avec_info.append((employe, certifie, a_travaille))

        # Obtenir le nombre total d'employés
        nombre_total_employes = len(employes_avec_info)

        message = ""
        if nombre_total_employes == 0:
            message = "Aucun employé ne correspond aux critères de recherche."
        elif nombre_total_employes < nombre_employes_demandes:
            message = f"Seulement {nombre_total_employes} employés trouvés, moins que les {nombre_employes_demandes} demandés."

        employes = employes_avec_info[:nombre_employes_demandes]

        return render(request, 'pages/liste_employe_result.html', {
            'employes': employes,
            'message': message,
            'nombre_total_employes': nombre_total_employes,
            'nombre_employes_demandes': nombre_employes_demandes,
            'nom': nom,
            'description_projet': description_projet,
            'date_debut_projet': date_debut_projet,
            'besoin_chef_projet': besoin_chef_projet,
            'besoin_consultant': besoin_consultant,
            'keywords': keywords,
        })
    else:
        return render(request, 'pages/composer_equipe.html')


   

   


def liste_employe_result(request):
    # Votre logique de vue ici
    return render(request, 'pages/liste_employe_result.html')



def ajouter_certifications(request):
    if request.method == 'POST':
        # Récupérer l'utilisateur connecté
        employe = request.user.employee  # Supposant que chaque utilisateur a un profil d'employé associé

        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        date_obtention = request.POST.get('date_obtention')
        fichier = request.FILES.get('formFile')
        technologies_utilisees = request.POST.get('technologies')

        # Créer et sauvegarder la certification en l'associant à l'employé
        certification = Certification(
            nom=nom,
            description=description,
            date_obtention=date_obtention,
            fichier=fichier,
            technologies_utilisees=technologies_utilisees,
            employe=employe,  # Associez la certification à l'employé récupéré
        )
        certification.save()


    return render(request, 'pages/ajouter_certifications.html')





@login_required
def liste_certification(request):
    # Vérifier si l'utilisateur est connecté
    if request.user.is_authenticated:
        # Récupérer les certifications de l'utilisateur connecté
        certifications = Certification.objects.filter(employe=request.user.employee)
        return render(request, 'pages/liste_certification.html', {'certifications': certifications})
    


def liste_projet(request):
    # Vérifier si l'utilisateur est connecté
    if request.user.is_authenticated:
        # Récupérer les certifications de l'utilisateur connecté
        projets = Projet.objects.filter(employe=request.user.employee)
        return render(request, 'pages/liste_projet.html', {'projets': projets})
    



def valider_equipe(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description_projet = request.POST.get('description_projet')
        date_debut_projet = request.POST.get('date_debut_projet')
        employes_ids = request.POST.getlist('employes_ids')


        equipe_projet = EquipeProjet.objects.create(
            nom=nom,
            description=description_projet,
            date_debut=date_debut_projet,
        )

        employes = Employee.objects.filter(id__in=employes_ids)
        equipe_projet.employes.set(employes)
        equipe_projet.save()

        return redirect('page_confirmation_enregistrement')
    


def page_confirmation_enregistrement(request):
    return render(request, 'pages/confirmation.html')



def liste_equipes_projet(request):
    equipes_projet = EquipeProjet.objects.all()
    return render(request, 'pages/liste_equipes_projet.html', {'equipes_projet': equipes_projet})



def modifier_equipe_projet(request, equipe_projet_id):
    equipe_projet = get_object_or_404(EquipeProjet, id=equipe_projet_id)
    
    if request.method == 'POST':
        form = EquipeProjetForm(request.POST, instance=equipe_projet)  # Si vous utilisez un formulaire
        if form.is_valid():
            form.save()
            return redirect('liste_equipes_projet')
    else:
        form = EquipeProjetForm(instance=equipe_projet)  # Si vous utilisez un formulaire

    return render(request, 'pages/modifier_equipe_projet.html', {'form': form})


def supprimer_equipe_projet(request, equipe_projet_id):
    equipe_projet = get_object_or_404(EquipeProjet, id=equipe_projet_id)
    if request.method == 'POST':
        equipe_projet.delete()
        return redirect('liste_equipes_projet')
    return render(request, 'pages/supprimer_equipe_projet.html', {'equipe_projet': equipe_projet})
    

    
    
    






    




