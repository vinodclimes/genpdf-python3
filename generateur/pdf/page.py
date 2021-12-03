from .nom import NomPDF
from .liste import ListePDF
from .dictionnaire import DictionnairePDF
from .mesure import DistancePDF, PositionPDF
from .composant import ComposantPDF
from .document import DocumentPDF


class PagePDF(DictionnairePDF):
    """Une page PDF est un dictionnaire avec des clés obligatoires.

    Clés obligatoires :
    - Type = Page
    - Parent = une référence sur l'objet parent (une page racine)
    - MediaBox = la définition des limites de la page

    Exemple :

        <<
        /Type /Page
        /Parent 3 0 R
        /MediaBox [0 0 595 842]
        ...
        >>

    """

    LIMITES_A4 = (0, 0, PositionPDF.LARGEUR_A4, PositionPDF.HAUTEUR_A4)

    def __init__(self):
        super().__init__()
        self.inserer("Type", NomPDF("Page"))
        composant_liste_pdf_limites = ListePDF()
        for valeur in self.LIMITES_A4:
            composant_liste_pdf_limites.inserer(DistancePDF(valeur))
        self.inserer("MediaBox", composant_liste_pdf_limites)
        self.reference_page_parente = None
        self.police = None
        self.reference_police = None
        self.reference_contenu = None

    def definir_page_parente(self, reference_objet_pdf):
        self.reference_page_parente = reference_objet_pdf
        return self

    def definir_police(self, police, reference_objet_pdf):
        self.police = police
        self.reference_police = reference_objet_pdf
        return self

    def definir_contenu(self, reference_objet_pdf):
        self.reference_contenu = reference_objet_pdf
        return self

    def finaliser(self):
        if self.reference_page_parente is not None:
            self.inserer("Parent", self.reference_page_parente)
        if self.police is not None and self.reference_police is not None:
            dictionnaire_polices = DictionnairePDF()
            dictionnaire_polices.inserer(
                self.police.nom_interne, self.reference_police)
            dictionnaire_ressources = DictionnairePDF()
            dictionnaire_ressources.inserer("Font", dictionnaire_polices)
            self.inserer("Resources", dictionnaire_ressources)
        if self.reference_contenu is not None:
            self.inserer("Contents", self.reference_contenu)
        return self


class PageRacinePDF(DictionnairePDF):
    """Une page racine PDF est un dictionnaire avec des clés obligatoires.

    Clés obligatoires :
    - Type = Pages
    - Kids = la liste des références vers les pages filles
    - Count = le nombre de pages filles

    Exemple :

        <<
        /Type /Pages
        /Kids [4 0 R]  <== référence vers 1 page fille : l'objet n°4 version 0
        /Count 1
        ...
        >>

    """

    def __init__(self):
        super().__init__()
        self.inserer("Type", NomPDF("Pages"))
        self.liste_ref_pages_filles = []

    def ajouter_page_fille(self, reference_objet_pdf):
        self.liste_ref_pages_filles.append(reference_objet_pdf)
        return self

    def finaliser(self):
        composant_liste_pdf_references = ListePDF()
        for ref_page_fille in self.liste_ref_pages_filles:
            composant_liste_pdf_references.inserer(ref_page_fille)
        self.inserer("Kids", composant_liste_pdf_references)
        self.inserer("Count", len(self.liste_ref_pages_filles))
        return self


class ContenuPagePDF(ComposantPDF):
    """Le contenu d'une page PDF est une suite d'opérations de dessin.

    Cette classe réalise les opérations de préparation/finalisation d'une page :
    - définition d'une épaisseur de trait
    - délimitation d'un rectangle de dessin
    - sauvegarde/restauration d'un contexte

    Du contenu texte peut être inséré dans la page via des objets BlocTextePDF.
    """

    SEPARATEUR_COORD = b" "
    OPERATION_EPAISSEUR_TRAIT = "0.1 w"  # Epaisseur de 0.1 point.
    OPERATION_SAUVEGARDE_CONTEXTE = "q"
    OPERATION_RESTAURATION_CONTEXTE = "Q"
    OPERATEUR_RECTANGLE = "re"
    OPERATION_DELIMITATION = "W* n"

    def __init__(self):
        super().__init__(separateur=DocumentPDF.SAUT_LIGNE)
        self.inserer(self.OPERATION_EPAISSEUR_TRAIT)
        self.inserer(self.OPERATION_SAUVEGARDE_CONTEXTE)
        composant_delimitation = ComposantPDF(separateur=self.SEPARATEUR_COORD)
        for valeur in PagePDF.LIMITES_A4:
            composant_delimitation.inserer(DistancePDF(valeur))
        composant_delimitation.inserer(self.OPERATEUR_RECTANGLE)
        self.inserer(composant_delimitation)
        self.inserer(self.OPERATION_DELIMITATION)

    def finaliser(self):
        self.inserer(self.OPERATION_RESTAURATION_CONTEXTE)
        return self
