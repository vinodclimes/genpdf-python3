from .composant import ComposantPDF


class ListePDF(ComposantPDF):
    """Une liste de valeurs dans la structure d'un document PDF.

    Les listes PDF s'écrivent entre crochets.
    Les éléments sont séparés par des espaces.
    Les élements peuvent être de types différents.

    Exemple :
    Une liste contenant 4 éléments : [1 2.3 txt /Catalog]
    """

    SEPARATEUR_ELEMENTS = b" "
    OUVERTURE = "["
    FERMETURE = "]"

    def __init__(self, premier_element=None):
        super().__init__()
        self.composant_interne_sequence = (
            ComposantPDF(premier_element, separateur=self.SEPARATEUR_ELEMENTS))
        super().inserer(self.OUVERTURE)
        super().inserer(self.composant_interne_sequence)
        super().inserer(self.FERMETURE)

    def inserer(self, element):
        self.composant_interne_sequence.inserer(element)
