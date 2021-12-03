from .composant import ComposantPDF
from .document import DocumentPDF
from .dictionnaire import DictionnairePDF
from .nom import NomPDF


class FluxPDF(ComposantPDF):
    """Un flux PDF (stream) permet d'encapsuler un contenu dans le document PDF.

    Le contenu est arbitraire : instructions de dessin, police, image, etc.
    Encapsulé dans un objet interne, le flux devient référençable dans le PDF.
    """

    OUVERTURE = "stream"
    FERMETURE = "endstream"

    def __init__(self):
        super().__init__(separateur=DocumentPDF.SAUT_LIGNE)
        self.composant_dictionnaire = DictionnairePDF()
        self.composant_flux = ComposantPDF(separateur=DocumentPDF.SAUT_LIGNE)
        super().inserer(self.composant_dictionnaire)
        super().inserer(self.OUVERTURE)
        super().inserer(self.composant_flux)
        super().inserer(self.FERMETURE)

    def inserer(self, element):
        self.composant_flux.inserer(element)

    def finaliser(self):
        longueur = len(bytes(self.composant_flux))
        self.composant_dictionnaire.inserer((NomPDF("Length"), longueur))
        return self
