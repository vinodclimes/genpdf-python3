from .assistant import FIN_LIGNE, en_octets
from .ligne import LignePDF


class TableReferencesPDF:

    # La table des références contient les positions des autres objets.
    #
    # Elle démarre par le marqueur "xref".
    # La ligne suivante indique son premier indice (0) et sa taille (1+N).
    # Elle comporte une entrée "zéro", suivie de N entrées d'indices 1 à N.
    # L'entrée d'indice <i> indique la position et la version de l'objet <i>.
    #
    # Exemple :
    #
    #     xref
    #     0 4
    #     0000000000 65535 f
    #     0000025914 00000 n    <== Objet n°1 version 0, situé en 25914
    #     0000026000 00000 n    <== Objet n°2 version 0, situé en 26000
    #     0000000192 00000 n    <== Objet n°3 version 0, situé en 192

    MARQUEUR_XREF = b"xref"
    ENTREE_0 = b"0000000000 65535 f"
    SEPARATEUR = b" "
    MARQUEUR_OBJET = b"n"

    @classmethod
    def entree_en_octets(cls, position, version=0):
        octets_position = en_octets(f"{position:010}")
        octets_version = en_octets(f"{version:05}")
        return (octets_position
                + cls.SEPARATEUR
                + octets_version
                + cls.SEPARATEUR
                + cls.MARQUEUR_OBJET)

    @classmethod
    def finaliser_entree(cls, octets):
        # Un séparateur final est nécessaire pour atteindre 20 octets
        # si le marqueur de fin de ligne ne fait pas 2 octets de long.
        if len(FIN_LIGNE) < 2:
            return octets + cls.SEPARATEUR
        else:
            return octets

    def __init__(self, position):
        self.position = position
        self.references = []

    def ajouter_reference(self, position):
        self.references.append(position)

    def lire_octets(self):
        taille = 1 + len(self.references)

        octets = b""
        octets += LignePDF(self.MARQUEUR_XREF).lire_octets()
        octets += b"0" + self.SEPARATEUR + en_octets(taille) + FIN_LIGNE
        octets += LignePDF(self.finaliser_entree(self.ENTREE_0)).lire_octets()

        for position in self.references:
            entree = self.entree_en_octets(position)
            octets += LignePDF(self.finaliser_entree(entree)).lire_octets()

        return octets
