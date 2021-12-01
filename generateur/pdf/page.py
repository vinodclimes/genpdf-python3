from .assistant import en_octets
from .nom import NomPDF
from .reference import ReferenceObjetPDF
from .liste import ListePDF
from .dictionnaire import DictionnairePDF


class PagePDF:

    # Une page PDF est un dictionnaire avec des clés obligatoires :
    # - Type = Page
    # - Parent = une référence sur l'objet parent (une page racine)
    # - MediaBox = la définition des limites de la page
    #
    # Exemple :
    #
    #     <<
    #     /Type /Page
    #     /Parent 3 0 R
    #     /MediaBox [0 0 595 842]
    #     ...
    #     >>

    LIMITES_A4 = (0, 0, 595, 842)

    @staticmethod
    def limites_en_octets(limites):
        liste = ListePDF()
        for valeur in limites:
            liste.ajouter(en_octets(valeur))
        return liste.lire_octets()

    def __init__(self, reference_parent):
        self.parent = reference_parent

    def lire_octets(self):
        limites = self.limites_en_octets(self.LIMITES_A4)
        dictionnaire = DictionnairePDF()
        dictionnaire.ajouter(NomPDF("Type"), NomPDF("Page").lire_octets())
        dictionnaire.ajouter(NomPDF("Parent"), self.parent.lire_octets())
        dictionnaire.ajouter(NomPDF("MediaBox"), limites)
        return dictionnaire.lire_octets()


class PageRacinePDF:

    # Une page racine PDF est un dictionnaire avec des clés obligatoires :
    # - Type = Pages
    # - Kids = la liste des références vers les pages filles
    # - Count = le nombre de pages filles
    #
    # Exemple :
    #
    #     <<
    #     /Type /Pages
    #     /Kids [4 0 R]  <== référence vers 1 page fille : l'objet n°4 version 0
    #     /Count 1
    #     ...
    #     >>

    @staticmethod
    def pages_filles_en_octets(objets_pages_pdf):
        liste = ListePDF()
        for objet in objets_pages_pdf:
            reference = ReferenceObjetPDF(objet.numero, objet.version)
            liste.ajouter(reference.lire_octets())
        return liste.lire_octets()

    def __init__(self):
        self.pages = []

    def ajouter_page_fille(self, objet_page_pdf):
        self.pages.append(objet_page_pdf)

    def lire_octets(self):
        pages_filles = self.pages_filles_en_octets(self.pages)
        dictionnaire = DictionnairePDF()
        dictionnaire.ajouter(NomPDF("Type"), NomPDF("Pages").lire_octets())
        dictionnaire.ajouter(NomPDF("Kids"), pages_filles)
        dictionnaire.ajouter(NomPDF("Count"), en_octets(len(self.pages)))
        return dictionnaire.lire_octets()
