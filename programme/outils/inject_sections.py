import sys
import re

def inject_sections(filepath, arbitration, relance_desc, is_revenue=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "## Chiffrage détaillé" in content:
        return

    # Split to insert before '## Sources' if exists, otherwise at the end
    parts = re.split(r'## Sources\n', content)

    main_part = parts[0].strip()
    sources_part = parts[1].strip() if len(parts) > 1 else ""

    injection = f"""

## Chiffrage détaillé

| Mesure | Coût brut / Rendement | Recettes / Économies propres | Coût net (2032) | Hypothèses de calcul |
|---|---|---|---|---|
| Mesures du domaine | [À VÉRIFIER] | [À VÉRIFIER] | [À VÉRIFIER] | Calcul basé sur coûts unitaires (cf annexes macro) |

## Justification et Faisabilité

- **Justification** : [À VÉRIFIER] Impact social et économique attendu.
- **Faisabilité** : [À VÉRIFIER] Mise en œuvre et contraintes juridiques évaluées.

## Arbitrage et Relance

- **Statut d'arbitrage** : {arbitration}
- **Lien avec la relance économique** : {relance_desc}
"""

    new_content = main_part + injection + "\n## Sources\n\n- [À VÉRIFIER] Compléter les sources précises.\n" + sources_part + "\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    filepath = sys.argv[1]
    arbitration = sys.argv[2]
    relance_desc = sys.argv[3]
    inject_sections(filepath, arbitration, relance_desc)
