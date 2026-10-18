import re

DOMAINS_DIR = "programme/domaines"
ARBITRAGE_FILE = "programme/arbitrage.md"

def read_index_costs():
    costs = {}
    with open("programme/00-index.md", "r") as f:
        for line in f:
            if line.startswith('| 0') or line.startswith('| 1') or line.startswith('| 2') or line.startswith('| 3') or line.startswith('| 4'):
                parts = line.split('|')
                if len(parts) >= 5:
                    num = parts[1].strip()
                    # The name is inside brackets [Name](link)
                    match = re.search(r'\[(.*?)\]', parts[2])
                    domain_name = match.group(1) if match else parts[2].strip()
                    cost = parts[4].strip()
                    costs[num] = (domain_name, cost)
    return costs

def main():
    costs = read_index_costs()
    matrix_lines = []

    for num in sorted(costs.keys()):
        name, cost = costs[num]

        status = "🟢 Socle"
        if num in ["27", "01", "11", "24", "12", "08", "10", "31", "39", "30", "29", "32", "38", "44", "45"]:
            status = "🟡 Seconde vague (ou mixte)"
        if num == "06":
            status = "🟢 Socle (Recettes)"

        justif = "Impact direct sur l'emploi ou prérequis social séquencé."
        if int(num) in [20, 19, 28, 22, 34, 7, 13, 5, 11, 14, 15, 16, 39]:
            justif = "Relance économique, compétitivité ou emploi."
        elif int(num) in [3, 4, 27]:
            justif = "Régalien et sécurité publique."

        matrix_lines.append(f"| {num} - {name} | {status} | {cost} | {justif} |")

    with open(ARBITRAGE_FILE, 'r') as f:
        content = f.read()

    parts = content.split("## 3. Matrice d'arbitrage (Synthèse)\n\n| Mesure / Domaine | Statut | Coût 2032 | Justification (Critères : Emploi, Urgence, Faisabilité) |\n|---|---|---|---|\n")
    if len(parts) == 2:
        bottom_parts = parts[1].split("\n\n*(La matrice complète")
        new_content = parts[0] + "## 3. Matrice d'arbitrage (Synthèse)\n\n| Mesure / Domaine | Statut | Coût 2032 | Justification (Critères : Emploi, Urgence, Faisabilité) |\n|---|---|---|---|\n" + "\n".join(matrix_lines) + "\n\n*(La matrice complète" + bottom_parts[1]
        with open(ARBITRAGE_FILE, 'w') as f:
            f.write(new_content)

if __name__ == "__main__":
    main()
