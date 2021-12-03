class DistancePDF:
    """Une distance dans une page PDF.

    L'initialisation se fait à partir d'une valeur en millimètres.

    La valeur est automatiquement convertie puis exprimée en unités PDF.
    L'unité PDF est le "point" : 1 point = 1/72e pouce (1 pouce = 25,4mm).
    """

    @staticmethod
    def convertir(valeur_mm):
        return (valeur_mm * 72 / 25.4)

    def __init__(self, valeur_mm):
        self.valeur_points = self.convertir(valeur_mm)

    def __str__(self):
        return f"{self.valeur_points:.1f}"


class PositionPDF:
    """Une position dans une page PDF (au format A4).

    L'initialisation se fait à partir de deux distances :
    - la distance depuis le bord gauche de la page, vers la droite, en mm
    - la distance depuis le haut de la page, vers le bas, en mm

    La position est automatiquement convertie puis exprimée en coordonnées PDF.
    Le point d'origine du PDF est situé au coint inférieur gauche de la page.
    L'axe X est dirigé vers la droite, et l'axe Y est dirigé vers le haut.
    Les distances sont exprimées en unités PDF (voir DistancePDF).
    """

    LARGEUR_A4 = 210
    HAUTEUR_A4 = 297

    def __init__(self, decalage_droite_mm, decalage_bas_mm):
        self.x = DistancePDF(decalage_droite_mm)
        self.y = DistancePDF(self.HAUTEUR_A4 - decalage_bas_mm)

    def __str__(self):
        return f"{self.x} {self.y}"
