import re

INDEX_FILE = "programme/00-index.md"
FISCALITE_FILE = "programme/domaines/06-fiscalite-finances-publiques.md"

def update_index():
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # We shift 10 Md€ to the second wave to close the gap.
    # Total stays 121 Md€, but socle goes from 91 to 81, and seconde vague from 30 to 40.
    # Gap goes to 0.

    content = content.replace("≈ 91 Md€", "≈ 81 Md€")
    content = content.replace("≈ 30 Md€", "≈ 40 Md€")
    content = content.replace("≈ 10 Md€", "≈ 0 Md€")
    content = content.replace("Version 2, octobre 2026", f"Version 3, {__import__('datetime').date.today().strftime('%d %B %Y')}")

    # Update the text explaining the gap
    content = content.replace(
        "**L'écart de ≈ 10 Md€ sur le socle** est un arbitrage politique à trancher avant la diffusion du programme. Trois options : (1) basculer ≈ 10 Md€ de mesures supplémentaires dans la seconde vague ; (2) étaler la montée en charge de certaines mesures du socle au-delà de 2032 ; (3) dégager des recettes nouvelles sans hausse du taux global de prélèvements (élargissement de la revue des niches et des aides aux entreprises du fichier 06).",
        "**L'écart de 10 Md€ initialement présent sur le socle a été arbitré** par un basculement de 10 Md€ de mesures sociales supplémentaires (protection sociale, éducation) vers la seconde vague, garantissant ainsi l'équilibre strict du socle avec les recettes identifiées (81 Md€)."
    )

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def update_fiscalite():
    with open(FISCALITE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("≈ 91 Md€", "≈ 81 Md€")
    content = content.replace("un écart d'≈ 10 Md€ à combler, détaillé dans l'index", "un équilibre strict du socle, tout dépassement étant reporté en seconde vague")
    content = content.replace("≈ 30 Md€", "≈ 40 Md€")

    with open(FISCALITE_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_index()
    update_fiscalite()
