from .dictionnaire import DictionnairePDF
from .nom import NomPDF


class PolicePDF(DictionnairePDF):
    """Une police PDF, et ses caractéristiques.

    Cette classe est très limitée : elle expose seulement 4 polices standards.
    Les polices standards sont obligatoirement disponibles, ou substituées.
    """

    SERIF = "Times-Roman"
    SERIF_GRAS = "Times-Bold"
    SANS_SERIF = "Helvetica"
    SANS_SERIF_GRAS = "Helvetica-Bold"

    def __init__(self, taille_pt=12, serif=True, gras=False):
        super().__init__()
        self.taille = taille_pt
        self.nom_interne = None
        self.nom_standard = None
        if serif:
            if gras:
                self.nom_standard = self.SERIF_GRAS
            else:
                self.nom_standard = self.SERIF
        else:
            if gras:
                self.nom_standard = self.SANS_SERIF_GRAS
            else:
                self.nom_standard = self.SANS_SERIF

    def definir_nom_interne(self, nom):
        self.nom_interne = nom
        return self

    def finaliser(self):
        self.inserer("Type", NomPDF("Font"))
        self.inserer("Subtype", NomPDF("Type1"))
        self.inserer("BaseFont", NomPDF(self.nom_standard))
        return self
