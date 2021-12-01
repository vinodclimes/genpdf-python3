from .ligne import LignePDF


class DictionnairePDF:

    # Exemple : un dictionnaire avec 3 entrées (Type, Size, Info).
    #
    #     <<
    #     /Type /Catalog
    #     /Size 88
    #     /Info 87 0 R
    #     >>

    PREFIXE = b"<<"
    SUFFIXE = b">>"
    SEPARATEUR = b" "

    def __init__(self):
        self.cles_valeurs = {}

    def ajouter(self, nom_pdf, objet_pdf):
        cle = nom_pdf.lire_octets()
        self.cles_valeurs[cle] = (nom_pdf, objet_pdf)

    def lire_octets(self):
        lignes = []
        lignes.append(self.PREFIXE)

        for cle in self.cles_valeurs:
            (nom_pdf, objet_pdf) = self.cles_valeurs[cle]
            ligne = nom_pdf.lire_octets()
            ligne += self.SEPARATEUR
            ligne += objet_pdf.lire_octets()
            lignes.append(ligne)

        lignes.append(self.SUFFIXE)

        octets = b""
        for ligne in lignes:
            octets += LignePDF(ligne).lire_octets()

        return octets
