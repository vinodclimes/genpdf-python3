from .assistant import FIN_LIGNE, en_octets
from .ligne import LignePDF


class FermeturePDF:

    # Un fichier PDF se termine par 3 sections :
    # - un dictionnaire final dans la section "trailer"
    # - la position de la table des références dans la section "startxref"
    # - un marqueur de fin de fichier
    #
    # Exemple :
    #
    #     trailer
    #     <<
    #     ...
    #     >>
    #     startxref
    #     123
    #     %%EOF

    MARQUEUR_TRAILER = b"trailer"
    MARQUEUR_STARTXREF = b"startxref"
    MARQUEUR_EOF = b"%%EOF"

    def __init__(self, table_references, dictionnaire_fermeture):
        self.table = table_references
        self.dictionnaire = dictionnaire_fermeture

    def lire_octets(self):
        octets = b""
        octets += LignePDF(self.MARQUEUR_TRAILER).lire_octets()
        octets += self.dictionnaire.lire_octets()
        octets += LignePDF(self.MARQUEUR_STARTXREF).lire_octets()
        octets += LignePDF(en_octets(self.table.position)).lire_octets()
        octets += LignePDF(self.MARQUEUR_EOF).lire_octets()
        return octets