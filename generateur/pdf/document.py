from .composant import ComposantPDF


class DocumentPDF(ComposantPDF):
    """Le composant principal d'un document PDF.

    Un DocumentPDF contient tous les autres ComposantPDF qui constituent
    la structure d'un document complet.
    """

    SAUT_LIGNE = b"\n"
    LIGNE_VIDE = 2 * SAUT_LIGNE

    ESPACE = b" "

    LONGUEUR_MAX_LIGNE = 255
    LONGUEUR_MAX_TEXTE = LONGUEUR_MAX_LIGNE - len(SAUT_LIGNE)

    CLE_POSITION_FIN = "FIN"

    @classmethod
    def rechercher_saut(cls, octets):
        return octets.find(cls.SAUT_LIGNE)

    @classmethod
    def rechercher_espace_final(cls, octets):
        return octets.rfind(cls.ESPACE)

    @classmethod
    def decomposer_en_lignes(cls, octets):
        lignes = []
        position = cls.rechercher_saut(octets)
        while (position > -1):
            ligne = octets[:position]
            lignes.append(ligne)
            position_suivante = position + len(cls.SAUT_LIGNE)
            octets = octets[position_suivante:]
            position = cls.rechercher_saut(octets)
        lignes.append(octets)
        return lignes

    @classmethod
    def raccourcir_lignes(cls, lignes):
        lignes_courtes = []
        for ligne in lignes:
            while len(ligne) > cls.LONGUEUR_MAX_TEXTE:
                position_coupure = cls.LONGUEUR_MAX_TEXTE
                if ligne[position_coupure] != cls.ESPACE:
                    position_espace = cls.rechercher_espace_final(ligne)
                    if position_espace > -1:
                        position_coupure = position_espace
                lignes_courtes.append(ligne[:position_coupure])
                ligne = ligne[position_coupure:]
            lignes_courtes.append(ligne)
        return lignes_courtes

    @classmethod
    def normaliser_portion_document(cls, octets):
        lignes = cls.decomposer_en_lignes(octets)
        lignes = cls.raccourcir_lignes(lignes)
        return cls.SAUT_LIGNE.join(lignes)

    def __init__(self):
        super().__init__(separateur=self.LIGNE_VIDE)

    def __bytes__(self):
        octets = super().__bytes__()
        octets += self.SAUT_LIGNE
        return self.normaliser_portion_document(octets)

    def lire_positions_internes(self):
        positions_internes = {}
        octets = b""
        for element in self.elements:
            try:
                numero = element.numero_objet
                positions_internes[numero] = len(octets)
            except AttributeError:  # Pas un ObjetPDF.
                pass
            octets += bytes(element)
            octets += self.LIGNE_VIDE
            octets = self.normaliser_portion_document(octets)
        positions_internes[self.CLE_POSITION_FIN] = len(octets)
        return positions_internes
