from .assistant import FIN_LIGNE, en_octets
from .ligne import LignePDF


class ObjetPDF:

    # Un objet PDF possède un numéro, une version, et un contenu
    # placé entre deux marqueurs : "obj" et "endobj".
    #
    # Exemple : objet n°1 version 0
    #
    #     1 0 obj
    #     ... contenu ...
    #     endobj

    SEPARATEUR = b" "
    PREFIXE = b"obj"
    SUFFIXE = b"endobj"

    def __init__(self, numero, contenu=None, version=0):
        self.numero = numero
        self.version = version
        self.contenu = contenu

    def lire_octets(self):
        premiere_ligne = (en_octets(self.numero)
                          + self.SEPARATEUR
                          + en_octets(self.version)
                          + self.SEPARATEUR
                          + self.PREFIXE)
        octets = b""
        octets += LignePDF(premiere_ligne).lire_octets()
        octets += self.contenu.lire_octets()
        octets += FIN_LIGNE
        octets += LignePDF(self.SUFFIXE).lire_octets()
        return octets
