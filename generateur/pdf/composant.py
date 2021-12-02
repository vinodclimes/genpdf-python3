class ComposantPDF:
    """Un composant à intégrer dans la structure d'un document PDF.

    Le composant contient un ou plusieurs éléments internes.
    On peut lui ajouter des éléments avec l'opérateur d'addition.
    Les éléments peuvent être des composants, du texte, des nombres, etc.

    La représentation binaire s'obtient par un appel à bytes().
    Les éléments représentés peuvent être séparés par un séparateur.
    """

    def __init__(self, premier_element=None, separateur=b""):
        self.separateur = separateur
        self.elements = []
        if premier_element is not None:
            self.inserer(premier_element)

    def inserer(self, element):
        self.elements.append(element)

    def __bytes__(self):
        octets = []
        for element in self.elements:
            if isinstance(element, bytes):
                octets.append(element)
            elif isinstance(element, ComposantPDF):
                octets.append(bytes(element))
            else:
                octets.append(bytes(str(element), "ascii"))
        return self.separateur.join(octets)
