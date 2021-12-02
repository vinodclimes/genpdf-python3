from .composant import ComposantPDF


class OuverturePDF(ComposantPDF):
    """Un fichier PDF commence par un indicateur de version. """

    INDICATEUR_VERSION = "%PDF-1.4"

    def __init__(self):
        super().__init__(self.INDICATEUR_VERSION)
