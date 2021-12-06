class Page:
    """Une page d'un document, avec son contenu.

    Le contenu d'une page est défini par un ensemble de blocs de texte.
    """

    def __init__(self):
        self.blocs = []

    def ajouter_bloc_texte(self, bloc_texte):
        self.blocs.append(bloc_texte)
