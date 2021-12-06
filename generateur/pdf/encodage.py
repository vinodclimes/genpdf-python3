class EncodageWinAnsi:
    """L'encodage Windows ANSI (ou Windows-1252, ou CP-1252).

    C'est l'un des 4 encodages simples supportés par le format PDF, et le plus
    utile dans le cadre de la langue française (accents, symbole euro, etc).
    """

    CODE_INCONNU = ord(" ")

    AJOUTS_WINDOWS_ANSI = {
        ord("€"): 128,
        ord("…"): 133,
        ord("‰"): 137,
        ord("Œ"): 140,
        ord("•"): 149,
        ord("œ"): 156,
        ord("Ÿ"): 159,
    }

    @classmethod
    def convertir_unicode(cls, code_unicode):
        if code_unicode < 128:
            # Plage 0 => 127 : ASCII.
            # Caractères conservés à l'identique en Windows ANSI.
            return code_unicode
        elif code_unicode < 160:
            # Plage 128 => 159 : caractères de contrôles Latin1.
            # Caractères non conservés en Windows ANSI.
            return cls.CODE_INCONNU
        elif code_unicode < 256:
            # Plage 160 => 255 : caractères accentués/spéciaux Latin1.
            # Caractères conservés à l'identique en Windows ANSI.
            return code_unicode
        else:
            # Plage >= 256 : caractères Unicode hors Latin1.
            # Caractères non supportés, à l'exception de quelques caractères
            # déplacés par Windows ANSI dans la plage des contrôles Latin1.
            if code_unicode in cls.AJOUTS_WINDOWS_ANSI:
                return cls.AJOUTS_WINDOWS_ANSI[code_unicode]
            else:
                return cls.CODE_INCONNU
