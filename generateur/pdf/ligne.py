from .assistant import FIN_LIGNE


class LignePDF:

    # Les lignes sont limitées en longueur,
    # et se terminent par un marqueur de fin de ligne.

    LONGEUR_MAX = 255

    @classmethod
    def decouper_en_morceaux(cls, octets):
        morceaux = []
        longueur_disponible = cls.LONGEUR_MAX - len(FIN_LIGNE)

        morceaux_complets = len(octets) // longueur_disponible
        for index_ligne in range(morceaux_complets):
            debut = index_ligne * longueur_disponible
            fin = debut + longueur_disponible
            morceaux.append(octets[debut:fin])

        morceau_incomplet = (len(octets) % longueur_disponible > 0)
        if morceau_incomplet:
            debut = morceaux_complets * longueur_disponible
            morceaux.append(octets[debut:])

        return morceaux

    def __init__(self, octets):
        self.morceaux = self.decouper_en_morceaux(octets)

    def lire_octets(self):
        octets = b""
        for morceau in self.morceaux:
            octets += morceau
            octets += FIN_LIGNE
        return octets
