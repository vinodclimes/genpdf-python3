from .composant import ComposantPDF


class ReferenceObjetPDF(ComposantPDF):
    """Une référence vers un objet interne au document PDF.

    Exemple :
    La référence vers l'objet interne n°42 en version 0, s'écrit : 42 0 R
    """

    SEPARATEUR_ELEMENTS = b" "
    MARQUEUR_REFERENCE = "R"

    def __init__(self, numero, version=0):
        super().__init__(separateur=self.SEPARATEUR_ELEMENTS)
        self.inserer(numero)
        self.inserer(version)
        self.inserer(self.MARQUEUR_REFERENCE)
