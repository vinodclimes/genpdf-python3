class BlocTexte:
    """Un bloc de plusieurs lignes de texte dans un document.

    Un bloc possède une position fixée au sein de la page (en millimètres),
    ainsi qu'une police unique pour l'ensemble du texte qu'il contient.
    """

    def __init__(self, decalage_droite_mm, decalage_bas_mm, police):
        self.droite = decalage_droite_mm
        self.bas = decalage_bas_mm
        self.police = police
        self.lignes = []

    def ajouter_ligne(self, ligne_texte):
        self.lignes.append(ligne_texte)
