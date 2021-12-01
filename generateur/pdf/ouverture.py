from .ligne import LignePDF


class OuverturePDF:

    # Un fichier PDF commence par un indicateur de version.

    MARQUEUR_VERSION = b"%PDF-1.4"

    def lire_octets(self):
        return LignePDF(self.MARQUEUR_VERSION).lire_octets()
