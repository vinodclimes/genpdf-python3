from .page import Page
from .police import Police
from .bloc import BlocTexte
from .ligne import LigneTexte


class Document:
    """Un document est une séquence de pages.

    Cette classe expose plusieurs méthodes de construction de document,
    basées sur le concept d'un curseur qu'on positionne avant d'écrire.

    Méthodes :
    - selectionner_page : pour se positionner sur une page avant écriture
    - positionner_curseur : pour choisir un emplacement où écrire dans la page
    - definir_police : pour choisir une police de caractères spécifique
    - ecrire_lignes : pour écrire les lignes de texte avec les réglages choisis

    Par défaut, l'écriture se fait sur la page 1, en haut à gauche,
    avec une police serif de taille 10 point.
    """

    MARGE = 25
    POLICE = 10

    def __init__(self):
        self.pages = []
        self.page_courante = None
        self.polices = []
        self.police_courante = None
        self.curseur = None

    def selectionner_page(self, numero_page):
        if numero_page > len(self.pages):
            pages_manquantes = numero_page - len(self.pages)
            for i in range(pages_manquantes):
                self.pages.append(Page())
        self.page_courante = numero_page - 1

    def verifier_page(self):
        if self.page_courante is None:
            self.selectionner_page(1)

    def definir_police(self, taille_pt, serif=True, gras=False):
        police_demandee = Police(taille_pt, serif, gras)
        existe = False
        for index_police in range(len(self.polices)):
            police_existante = self.polices[index_police]
            if police_existante == police_demandee:
                self.police_courante = index_police
                existe = True
                break
        if not existe:
            self.polices.append(police_demandee)
            self.police_courante = len(self.polices) - 1

    def verifier_police(self):
        if self.police_courante is None:
            self.definir_police(self.POLICE)

    def retrouver_index_police(self, police_recherchee):
        for index_police in range(len(self.polices)):
            police = self.polices[index_police]
            if police == police_recherchee:
                return index_police
        return None

    def positionner_curseur(self, decalage_droite_mm, decalage_bas_mm):
        self.curseur = (decalage_droite_mm, decalage_bas_mm)

    def verifier_curseur(self):
        if self.curseur is None:
            self.positionner_curseur(self.MARGE, self.MARGE)

    def ecrire_lignes(self, lignes):
        self.verifier_page()
        self.verifier_curseur()
        self.verifier_police()
        bloc_texte = BlocTexte(
            self.curseur[0], self.curseur[1],
            self.polices[self.police_courante])
        for index_ligne in range(len(lignes)):
            texte = lignes[index_ligne]
            bloc_texte.ajouter_ligne(LigneTexte(texte))
        page_courante = self.pages[self.page_courante]
        page_courante.ajouter_bloc_texte(bloc_texte)
