from .nom import NomPDF
from .dictionnaire import DictionnairePDF


class CataloguePDF:

    # Un catalogue PDF est un dictionnaire avec des clés obligatoires :
    # - Type = Catalog
    # - Pages = une référence vers la page racine du document
    #
    # Exemple :
    #     <<
    #     /Type /Catalog
    #     /Pages 3 0 R
    #     ...
    #     >>

    def __init__(self, reference_page_racine):
        self.racine = reference_page_racine

    def lire_octets(self):
        dictionnaire = DictionnairePDF()
        dictionnaire.ajouter(NomPDF("Type"), NomPDF("Catalog").lire_octets())
        dictionnaire.ajouter(NomPDF("Pages"), self.racine.lire_octets())
        return dictionnaire.lire_octets()
