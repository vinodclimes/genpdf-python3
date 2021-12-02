from .composant import ComposantPDF


class NomPDF(ComposantPDF):
    """Un nom PDF est un texte précédé d'une barre oblique. """

    PREFIXE = "/"

    def __init__(self, nom):
        super().__init__()
        self.inserer(self.PREFIXE)
        self.inserer(nom)
