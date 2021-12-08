from generateur.sources.description import DescriptionCourrier
from generateur.document.generateur import GenerateurDocumentPDF


if __name__ == "__main__":

    fichier_source = "exemple/courrier.txt"
    fichier_sortie = "exemple/courrier.pdf"

    description = DescriptionCourrier(fichier_source)
    courrier = description.preparer_courrier()
    document_pdf = GenerateurDocumentPDF.generer_courrier(courrier)

    octets_pdf = bytes(document_pdf)

    with open(fichier_sortie, "wb") as fichier:
        n = fichier.write(octets_pdf)
        print(f"Fichier PDF généré : {fichier_sortie} ({n} octets). ")
