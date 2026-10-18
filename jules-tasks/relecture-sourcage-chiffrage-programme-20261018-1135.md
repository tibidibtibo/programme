# Jules task — Relecture, sourçage, chiffrage et arbitrage du programme « Refaire Nation »

## Contexte

Le dépôt contient un programme politique social-démocrate à la française, « Refaire Nation » (version 2, octobre 2026), écrit en **français**, en Markdown :

- `programme/00-index.md` : synthèse, diagnostic, six principes, table des 45 domaines (mesure phare + coût net 2032), **budget consolidé** (≈ 121 Md€ de mesures nouvelles nettes dont socle ≈ 91 Md€ et seconde vague ≈ 30 Md€ ; recettes identifiées ≈ 81 Md€ ; écart du socle ≈ 10 Md€ non tranché), calendrier, méthode et limites.
- `programme/programme-v1.md` : première version de synthèse (référence historique, ne pas supprimer).
- `programme/domaines/01-…md` à `45-…md` : un fichier par domaine. Structure type : `Constat chiffré` (tableau Indicateur/Valeur/Source) → `Ce qui marche ailleurs` → `Mesures` → `Coût et financement` → `Indicateurs de réussite en 2032` → `Sources`.
- Le fichier `06-fiscalite-finances-publiques.md` contient le tableau de recettes (≈ 81 Md€) qui finance le socle.

Principe politique directeur du programme : « L'argent est au service de l'homme, mais l'homme doit travailler » ; pas de hausse du taux global de prélèvements ; pas de mesure sans financement ; règle d'or budgétaire à la suédoise.

Aveu du programme lui-même (index, « Méthode et limites ») : les chiffres sont des ordres de grandeur, arrondis, à **vérifier et mettre à jour avant diffusion**. C'est exactement l'objet de cette tâche.

## Demande de l'utilisateur (reformulée)

Relire TOUS les fichiers du programme, sourcer et vérifier chaque chiffre et affirmation, développer davantage chaque domaine. Tout doit être **justifié, budgétisé et réaliste**. Il faut **arbitrer** entre les sujets. **Priorité absolue à la relance de l'économie, pour financer les volets sociaux** (la croissance et l'emploi d'abord, le social financé par la création de richesse). Indiquer clairement ce qui est retenu / différé / abandonné et garantir la cohérence budgétaire globale.

## Objectif

Produire une version 3 du programme dont :
1. chaque chiffre est vérifié ou signalé comme non vérifié, avec source précise ;
2. chaque domaine est plus développé (mesures détaillées, chiffrage ligne à ligne, hypothèses, calendrier de montée en charge, risques) ;
3. le budget global est cohérent, arbitré et réaliste, avec une **logique « économie d'abord »** : relance de l'offre et de l'emploi en premier, volets sociaux dimensionnés et séquencés en fonction des recettes que cette relance génère.

## Travail à réaliser

### Phase 1 — Audit (relecture complète)
Lire intégralement `00-index.md`, `programme-v1.md` et les 45 fichiers de domaines. Produire `programme/audit/audit-chiffres.md` : un tableau par domaine listant chaque chiffre/affirmation factuelle, sa source citée, son statut (✅ vérifié / ⚠️ à corriger / ❓ non vérifiable / 🔄 périmé) et la correction proposée avec source exacte (organisme, titre du document, année, URL si possible). Relever aussi : incohérences entre fichiers (ex. un même coût donné différemment dans l'index et dans le domaine ; doublons de mesures entre domaines, p. ex. 08/31, 23/33, 01/27/28), sommes qui ne tombent pas juste, mesures sans coût, mesures sans financement, mesures juridiquement impossibles (droit européen, Constitution).

### Phase 2 — Vérification et sourçage
- Utiliser en priorité des sources officielles/primaires : INSEE, DREES, DARES, Eurostat, OCDE, FMI, Cour des comptes, Haut Conseil des finances publiques, Conseil d'analyse économique, France Stratégie, Conseil des prélèvements obligatoires, PLF/PLFSS (« Voies et moyens », jaunes budgétaires, annexes), lois de programmation, rapports parlementaires, Banque de France, SIPRI/OTAN pour la défense, etc.
- Mettre à jour les chiffres avec les **dernières données disponibles** (le document est daté d'octobre 2026 mais cite surtout 2024-2025 : vérifier PLF 2027, comptes nationaux 2025, dernières prévisions de croissance/déficit/dette/charge d'intérêts).
- **Ne jamais inventer une source ni un chiffre.** Si une donnée n'est pas trouvable ou vérifiable, la marquer explicitement `[À VÉRIFIER]` avec l'hypothèse retenue et sa justification. Distinguer clairement donnée sourcée / estimation du programme / hypothèse.
- Chaque fichier doit se terminer par une section `## Sources` complète et précise (pas de « INSEE » seul : titre, année, indicateur).
- Les liens de navigation entre fichiers (`[← Index](../00-index.md)`) et les ancres doivent rester valides.

### Phase 3 — Développement de chaque domaine
Pour chacun des 45 domaines, enrichir le fichier en conservant la structure existante et en ajoutant :
- **Chiffrage détaillé** : tableau mesure par mesure (coût brut, recettes/économies propres, coût net, année de pleine charge, montée en charge annuelle 2027→2032), avec **hypothèses explicites** (unité × volume × coût unitaire, source du coût unitaire).
- **Justification** : pourquoi cette mesure, quelle évaluation d'impact (études, comparaisons internationales avec chiffres), quel effet attendu sur l'emploi/la croissance/le social.
- **Faisabilité** : contraintes juridiques (UE, Constitution, CEDH), capacités de mise en œuvre (recrutements, formation, foncier, délais), risques et plan B.
- **Statut d'arbitrage** de chaque mesure (voir Phase 4) : 🟢 Socle / 🟡 Seconde vague (conditionnelle) / 🔵 Différé (après 2032 ou hors mandat) / 🔴 Abandonné ou fusionné — avec la raison.
- **Lien avec la relance économique** : la mesure est-elle un investissement productif, un soutien à l'emploi/offre, ou une dépense sociale ? Quel effet retour (avec hypothèse de multiplicateur sourcée) ?
Les domaines les plus lourds budgétairement (08 protection sociale/retraites, 12 santé, 10 éducation, 11 supérieur-recherche, 27 défense, 24 service civique, 07 travail, 06 fiscalité) doivent recevoir le traitement le plus approfondi. Le contenu doit rester lisible : tableaux, phrases courtes, pas de remplissage.

### Phase 4 — Arbitrage « économie d'abord »
Créer `programme/arbitrage.md` (et le lier depuis l'index) contenant :
1. **Doctrine d'arbitrage** : ordre de priorité explicite — (1) relance de l'économie : compétitivité, industrie (20), énergie (19), souveraineté (28), numérique (22), PME (34), emploi/formation (07), logement (13) comme levier de mobilité et de construction, finance au service de l'économie réelle (05), recherche (11), simplification/État efficace (39), transports et infrastructures (14-16) ; (2) sécurité/régalien indispensable (défense, justice, sécurité) au niveau nécessaire ; (3) volets sociaux (08, 09, 31, 32, 30, 29, 12, 10…) dimensionnés **en fonction des recettes** effectivement dégagées par la relance et les réformes de financement ; (4) le reste.
2. **Matrice d'arbitrage** : toutes les mesures (≈ toutes celles des 45 fichiers) classées 🟢/🟡/🔵/🔴 avec coût 2032 et justification en une ligne. Critères : effet sur la croissance/l'emploi, rendement social par euro, urgence, réversibilité, faisabilité juridique et administrative, financement identifié.
3. **Règle de séquencement** : les dépenses sociales de la seconde vague sont déclenchées par des **seuils chiffrés** (croissance, déficit, taux d'emploi, recettes constatées), pas par une date. Définir ces seuils.
4. **Trajectoire macro-budgétaire 2027-2032** (tableau annuel) : PIB, croissance, taux d'emploi, recettes, dépenses, déficit (% PIB), dette (% PIB), charge d'intérêts, avec hypothèses explicites et sourcées (cadrage HCFP, COR, Commission européenne, OFCE, Banque de France). Montrer la compatibilité avec le retour du déficit sous 3 % et les règles budgétaires européennes (nouveau cadre de gouvernance, trajectoire d'ajustement). Fournir un scénario central, un scénario bas (croissance −0,5 pt) et un scénario haut, et dire ce qui saute dans le scénario bas.
5. **Chiffrage des effets de la relance** : décomposer les ≈ 12 Md€ d'« effets retour emploi et croissance » (fichier 06) avec une méthode explicite (hausse du taux d'emploi × recettes marginales par emploi, multiplicateurs). Si le chiffre n'est pas défendable, le corriger et propager.

### Phase 5 — Cohérence budgétaire globale
- **Fermer l'écart de ≈ 10 Md€ du socle** (index, « Budget consolidé ») en choisissant et justifiant une des trois options (ou une combinaison) et propager le choix dans tous les fichiers concernés.
- Recalculer le **budget consolidé** à partir des tableaux détaillés des domaines (somme vérifiée par script ou tableau, sans double compte) et mettre à jour `00-index.md` : colonne « Coût net annuel en 2032 » des 45 domaines, totaux socle / seconde vague, recettes, solde. Les chiffres de l'index, de `06-fiscalite-finances-publiques.md` et de chaque domaine doivent **concorder exactement**.
- Vérifier les **recettes** (≈ 81 Md€) une par une : niches (18), aides aux entreprises (20), fraude (8), impôt sur les patrimoines (6), successions (6), finance (5), pertinence des soins (5), taxes comportementales (1), effets retour (12). Pour chaque ligne : rendement défendable (fourchette basse/centrale/haute), risque de comportement (évasion, délocalisation), compatibilité avec le principe « pas de hausse du taux global de prélèvements » et avec la priorité « relance » (une recette qui pèse sur l'investissement ou l'emploi doit être réexaminée). Retenir une estimation **prudente** ; ne pas gonfler les recettes pour équilibrer.
- Vérifier la crédibilité de l'effort d'économies de ≈ 40 Md€ (règle de dépense) : décomposer par poste, source de comparaison, réalisme politique.
- Ajouter à l'index un tableau « Socle / Seconde vague / Différé / Abandonné » synthétique, et mettre à jour « Méthode et limites » (ce qui a été vérifié, date de vérification, ce qui reste `[À VÉRIFIER]`).
- Ajouter `programme/annexes/hypotheses-macro.md` (hypothèses communes : inflation, croissance, taux d'intérêt, indexations, PIB de référence, valeur d'un point d'indice, coût d'un ETP, etc.) pour que tous les domaines utilisent les **mêmes paramètres**.

### Phase 6 — Version et traçabilité
- Passer l'index en « Version 3 » avec la date du jour de la tâche.
- Créer `programme/CHANGELOG.md` résumant les corrections de chiffres majeures (ancien → nouveau, raison, source) et les arbitrages modifiés.
- Garder `programme-v1.md` intact (éventuellement ajouter un bandeau « archive »).

## Critères d'acceptation

- [ ] Les 45 fichiers de domaines + l'index ont tous été relus ; `programme/audit/audit-chiffres.md` existe et couvre tous les domaines.
- [ ] Chaque chiffre clé de chaque domaine a une source précise ou est marqué `[À VÉRIFIER]` ; aucune source inventée.
- [ ] Chaque domaine contient un chiffrage détaillé mesure par mesure avec hypothèses, un statut d'arbitrage 🟢/🟡/🔵/🔴 par mesure, une analyse de faisabilité, et une section `Sources` complète.
- [ ] `programme/arbitrage.md` existe : doctrine « économie d'abord », matrice d'arbitrage exhaustive, seuils de déclenchement de la seconde vague, trajectoire macro 2027-2032 avec trois scénarios.
- [ ] `programme/annexes/hypotheses-macro.md` existe et les domaines s'y réfèrent.
- [ ] Les montants de `00-index.md`, `06-fiscalite-finances-publiques.md`, `arbitrage.md` et des 45 domaines sont **cohérents** (aucune divergence ; sommes exactes) ; l'écart de ≈ 10 Md€ du socle est fermé et justifié.
- [ ] Le budget global est présenté de façon réaliste : recettes prudemment estimées, effets retour justifiés, scénario bas documenté, pas d'hypothèse de croissance optimiste non sourcée.
- [ ] Les volets sociaux sont explicitement conditionnés / séquencés par la relance économique ; les mesures sacrifiées ou différées sont listées avec leur raison.
- [ ] `programme/CHANGELOG.md` existe. Tous les liens relatifs et ancres Markdown fonctionnent.
- [ ] Le ton, la langue (français) et la structure des fichiers existants sont préservés ; le contenu ajouté est dense et utile (pas de remplissage).

## Contraintes

- Do not run Playwright, Cypress, or any headless-browser/e2e/UI test runner — they routinely hang or crash this sandbox and kill the session. Verify UI behavior via static/type checks and unit tests only, and describe manual verification steps in the PR description instead.
- Never run destructive git commands (`git reset --hard`, `git checkout -- .` / `git restore .`, `git clean -fd`/`-fdx`, unresolved `git stash`, force-push, history rewrite on pushed commits). Never discard uncommitted changes. Commit work incrementally and frequently so nothing is lost if the session stops early.
- Rester dans le dépôt : contenu Markdown uniquement (un petit script Python/shell de vérification des sommes et des liens est accepté ; le placer dans `programme/outils/`).
- Ne pas modifier le positionnement politique du programme (social-démocrate à la française, travail, pas de hausse du taux global de prélèvements) ; l'arbitrage consiste à dimensionner, séquencer, différer ou abandonner des mesures, pas à changer de projet. Toute mesure retirée ou différée doit être tracée dans l'arbitrage et le CHANGELOG.
- Honnêteté avant tout : ne pas fabriquer de chiffres, d'études ou de citations. En cas de doute, `[À VÉRIFIER]` + hypothèse explicite. Distinguer clairement faits sourcés, estimations et hypothèses.
- Travailler par lots (p. ex. ~5 domaines par commit), dans cet ordre : audit → hypothèses macro → domaines économiques (06, 05, 07, 19, 20, 22, 28, 34, 13, 14-16, 11) → domaines sociaux → domaines régaliens et divers → arbitrage → index et cohérence finale. Mettre à jour l'index et l'arbitrage en dernier, après stabilisation des chiffres des domaines.
- Commits en français ou anglais, messages clairs (`docs(programme): …`).

## Livrables

PR sur GitHub contenant : domaines enrichis, `programme/00-index.md` v3, `programme/arbitrage.md`, `programme/annexes/hypotheses-macro.md`, `programme/audit/audit-chiffres.md`, `programme/CHANGELOG.md`. La description de la PR résume : les 10 corrections de chiffres les plus importantes, les arbitrages majeurs (retenu/différé/abandonné), le budget consolidé final, la trajectoire macro, et la liste des points restant `[À VÉRIFIER]`.
