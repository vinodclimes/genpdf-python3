class Police:
    """Une police de caractères.

    Les paramètres disponibles sont la taille (en points), ainsi que
    le type de police (serif / sans-serif), et l'épaisseur (normal / gras).
    """

    def __init__(self, taille_pt=10, serif=True, gras=False):
        self.taille = taille_pt
        self.serif = serif
        self.gras = gras

    def __eq__(self, autre_police):
        return (self.taille == autre_police.taille
                and self.serif == autre_police.serif
                and self.gras == autre_police.gras)
