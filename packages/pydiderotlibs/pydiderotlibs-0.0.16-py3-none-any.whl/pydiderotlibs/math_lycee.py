# -*- coding: utf-8 -*-
#
# Version 1.1
"""
Module avec les fonctions de la classe de Seconde 2018 pour le lycée diderot (marseille).
On prend comme fichier de départ le module de l'irem d'Amiens
http://download.tuxfamily.org/amienspython/lycee.py
Licence http://www.cecill.info/
"""


import math

from .arithmetique import *
from .trigo import *
from .stats_proba import *
from .fonctions_usuelles import *
from .vecteurs import *
from .chaines import *
from .listes import *
from random import random

print("""
Merci d'utiliser la librairie lycee du module pydiderot.\n
N'hésitez pas à consulter la documentation en ligne:\n
https://pydiderotlibs.rtfd.io/librairies/lycee.html
""")

pi = math.pi


def repeter(f, n):
    """Appelle `n` fois la fonction ``f``.

    Alias disponible: ``repeat()``
    """
    for i in range(n):
        f()

def repeat(f, n):
    repeter(f, n)
    
def alea_entre_bornes(a,b,p=15):
    """Choisit un nombre (pseudo) aléatoire entre ``a`` et ``b`` avec ``p`` décimales.
    
    Arguments:
        a (float): valeur minimale   
        b (float): valeur maximale    
        p (integer, optionnel): nombre de décimales s'il est compris entre 0 et 15. (``15`` par défaut)    
        
    Alias disponible : ``random_between()``
    """
    c=random()*(b-a)+a
    if p>=0 and p<15 :
        p=int(p)
        c=int(c*10**p)/10**p
    return c
    
def random_between(a,b,p=0):
    alea_entre_bornes(a,b,p)
