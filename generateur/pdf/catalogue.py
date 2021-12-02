from .nom import NomPDF
from .dictionnaire import DictionnairePDF


class CataloguePDF(DictionnairePDF):
    """Un catalogue PDF est un dictionnaire avec des clés obligatoires.

    Clés obligatoires :
    - Type = Catalog
    - Pages = une référence vers la page racine du document

    Exemple :

        <<
        /Type /Catalog
        /Pages 3 0 R
        ...
        >>

    """

    def __init__(self):
        super().__init__()
        self.inserer((NomPDF("Type"), NomPDF("Catalog")))
        self.reference_page_racine = None

    def definir_page_racine(self, reference_objet_pdf):
        self.reference_page_racine = reference_objet_pdf
        return self

    def finaliser(self):
        if self.reference_page_racine is not None:
            self.inserer((NomPDF("Pages"), self.reference_page_racine))
        return self
