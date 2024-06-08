from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import ajouter_employe
from .views import *



urlpatterns = [
  path(''       , views.index,  name='index'),
  path('ajouter_certifications/', views.ajouter_certifications, name='ajouter_certifications'),
  path('ajouter_projet/', views.ajouter_projet, name='ajouter_projet'),
  path('composer_equipe/', views.composer_equipe, name='composer_equipe'),
  path('liste_certification/', views.liste_certification, name='liste_certification'),
  path('liste_projet/', views.liste_projet, name='liste_projet'),
  path('liste_employe_result/', views.liste_employe_result, name='liste_employe_result'),


  path('composer_equipe/', views.composer_equipe, name='composer_equipe'),
  path('confirmation/', views.page_confirmation_enregistrement, name='page_confirmation_enregistrement'),
  path('valider_equipe/', views.valider_equipe, name='valider_equipe'),

  path('liste_equipes_projet/', views.liste_equipes_projet, name='liste_equipes_projet'),





  path('ajouter_employe/', views.ajouter_employe, name='ajouter_employe'),
  path('liste_employe/', views.liste_employe, name='liste_employe'),



  path('equipe_projet/<int:equipe_projet_id>/modifier/', views.modifier_equipe_projet, name='modifier_equipe_projet'),
  path('equipe_projet/<int:equipe_projet_id>/supprimer/', views.supprimer_equipe_projet, name='supprimer_equipe_projet'),




  
]
