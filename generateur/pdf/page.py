from .nom import NomPDF
from .liste import ListePDF
from .dictionnaire import DictionnairePDF


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

    LIMITES_A4 = (0, 0, 595, 842)

    def __init__(self):
        super().__init__()
        self.inserer((NomPDF("Type"), NomPDF("Page")))
        composant_liste_pdf_limites = ListePDF()
        for valeur in self.LIMITES_A4:
            composant_liste_pdf_limites.inserer(valeur)
        self.inserer((NomPDF("MediaBox"), composant_liste_pdf_limites))
        self.reference_page_parente = None

    def definir_page_parente(self, reference_objet_pdf):
        self.reference_page_parente = reference_objet_pdf
        return self

    def finaliser(self):
        if self.reference_page_parente is not None:
            self.inserer((NomPDF("Parent"), self.reference_page_parente))
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
        self.inserer((NomPDF("Type"), NomPDF("Pages")))
        self.liste_ref_pages_filles = []

    def ajouter_page_fille(self, reference_objet_pdf):
        self.liste_ref_pages_filles.append(reference_objet_pdf)
        return self

    def finaliser(self):
        composant_liste_pdf_references = ListePDF()
        for ref_page_fille in self.liste_ref_pages_filles:
            composant_liste_pdf_references.inserer(ref_page_fille)
        self.inserer((NomPDF("Kids"), composant_liste_pdf_references))
        self.inserer((NomPDF("Count"), len(self.liste_ref_pages_filles)))
        return self
