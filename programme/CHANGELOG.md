# Journal des corrections — Version 3

[← Index](00-index.md)

Version 3 du programme « Réunir la France » (18 octobre 2026). Ce journal trace les corrections de chiffres et d'arbitrage issues de l'audit, des six lots de sourçage (`lots/lot-N.md`) et de la consolidation.

## Corrections de structure et de cohérence budgétaire

| Sujet | Avant | Après | Raison |
|---|---|---|---|
| Recettes du fichier 06 | ≈ 81 Md€ | ≈ 77 Md€ (rendement visé), ≈ 51 Md€ (prudent) | −3 Md€ de niches fossiles (comptées au 17) ; −1 Md€ de taxes comportementales (déduites des 12 et 13) ; décote de prudence ajoutée. |
| Domaine 05 (finance) | −5,5 Md€ « d'excédent » | +0,5 Md€ | Les recettes de la finance étaient comptées dans le 05 **et** dans le 06 (double compte). |
| Domaine 07 (travail) | 9 Md€, puis 6,5 Md€ | 7,5 Md€ | Somme des lignes fausse dans la passe précédente (4 + 4 − 0,5 = 7,5) ; économie « baisse du chômage » déjà comptée dans les effets retour. |
| Domaine 12 (santé) | 7,8 Md€ | 7,1 Md€ | 0,7 Md€ de taxes comportementales comptées ici, retirées du 06. |
| Domaine 13 (logement) | 5,5 Md€ | 4,9 Md€ | 0,6 Md€ de vacance et meublés comptés ici, retirés du 06. |
| Domaine 16 (routes) | −0,5 Md€ | +1,0 Md€ | La redevance autoroutière (1,5 Md€) était comptée au 14 et au 16. |
| Domaine 11 (recherche) | 11 Md€ | 11,2 Md€ | Somme des lignes du fichier. |
| Domaines 14, 15, 18, 19, 28, 44 | 3,3 ; −0,5 ; 1,4 ; 0,8 ; 1,5 ; 0,4 | 3,25 ; −0,05 ; 1,2 ; 0,2 ; 1,4 ; 0,35 | Chiffrages détaillés des lots 2, 6 et 1 (voir `lots/`). |
| Mesures nouvelles nettes | ≈ 121 Md€ | ≈ 117 Md€ | Somme des changements ci-dessus. |
| Socle / seconde vague | 81 / 40 Md€ | 64 / 53 Md€ | Ventilation par mesure issue des lots ; le socle n'était pas détaillé. |
| Trajectoire de déficit 2032 | −2,5 % (sans modèle) | ≈ 3,4 % (central) | Modèle explicite ajouté (arbitrage §4). Le chiffre précédent n'était pas défendable. |

## Arbitrages majeurs (économie d'abord)

- Socle : 48 % économie, 17 % régalien, 34 % social. Seconde vague : 53 % social.
- Seconde vague scindée en **tranche A** (≈ 14 Md€, investissement et régalien, déclenchée par seuils) et **tranche B** (≈ 39 Md€, social, différée tant que le déficit n'est pas ≤ 3 %).
- **Clause de sauvegarde** : gel du socle social si le déficit dérape de plus de 0,5 point deux années de suite.
- Aucune mesure abandonnée ; trois grandes mesures différées (APD à 0,55 %, point d'indice, allocation d'autonomie étudiante).

## Principales corrections de chiffres factuels (voir les rapports de lot)

- Dette : ≈ 3 460 Md€ fin 2025, 115,6 % du PIB (lot 1). Charge de la dette : ≈ 74-77 Md€ en 2026 (lot 1).
- Dividendes et rachats du CAC 40 : 97,1 Md€ en 2023 (lot 1).
- Mises en chantier de logements : ≈ 260 000 en 2024 ; coût des 6 EPR2 : 67-80 Md€ (lot 2).
- Rail dans le fret : ≈ 10 % (lot 2). Morts sur les routes : ≈ 3 400 (lot 2).
- Surprime CatNat : 12 % → 20 % (lot 6).

## Finalisation de la Version 3 (18 octobre 2026)

- **Harmonisation structurelle intégrale des 45 domaines** :
  - Standardisation stricte des 9 sections canoniques dans chaque fichier : `## Constat chiffré`, `## Ce qui marche ailleurs`, `## Mesures`, `## Coût et financement`, `## Indicateurs de réussite en 2032`, `## Chiffrage détaillé`, `## Justification et Faisabilité`, `## Arbitrage et Relance`, `## Sources`.
  - Harmonisation des statuts budgétaires avec emojis standardisés dans chaque section Arbitrage : 🟢 Socle (45 fichiers), 🟡 Tranche A (11 fichiers), 🔵 Différé (11 fichiers).
- **Ventilation granulaire des recettes et économies sensibles** :
  - **Fichier 06 (Fiscalité et finances)** : revue des aides aux entreprises (20 Md€) décomposée en 5 piliers documentés (allègements > 2,5 SMIC et niches sectorielles 6 Md€, CIR recentré 3 Md€, doublons guichets État-Régions 5 Md€, subventions fossiles et clause de remboursement 4 Md€, primes d'apprentissage 2 Md€). Sanctuarisation explicite des allègements généraux sur 1,0 à 1,6 SMIC pour préserver l'emploi peu qualifié.
  - **Fichier 12 (Santé)** : pertinence des soins (5 Md€) décomposée en 4 leviers issus des rapports CNAM/Cour des comptes (prescriptions et biologie -1,5 Md€, imagerie et DMP -1,2 Md€, chirurgie ambulatoire et HAD -1,3 Md€, transports sanitaires et arrêts fictifs -1,0 Md€).
- **Vérification et sourçage primaire du Lot 3 (Social, Santé, Autonomie)** :
  - Vérification et mise à jour de l'ensemble des données d'origine avec URLs officielles et rapports primaires (DREES 2024, CNAM 2024-2025, INSEE 2024-2025, DARES 2024, CNSA 2024, SSMSI 2024) sur les domaines 12, 29, 30, 31, 32, 08, 09.
  - Clôture du rapport de lot `programme/lots/lot-3.md`.
- **Rédaction de la Synthèse Exécutive officielle Version 3 (`programme-v3.md`)** :
  - Document de référence complet articulé en 8 sections : diagnostic et paradoxe français, 6 principes du contrat républicain, doctrine « L'économie d'abord » et architecture à 3 étages (Socle 64,1 Md€, Tranche A 14,3 Md€, Tranche B 39,0 Md€, clause de sauvegarde), équilibre macro-budgétaire et trajectoire 2027-2032 (3 scénarios), synthèse des 45 chantiers par grand bloc, calendrier d'action gouvernementale, matrice récapitulative exhaustive des 45 domaines et engagements de méthode.

## Ce qui reste à faire

- Poursuivre le réalignement avec URLs des sources secondaires restantes pour les lots 1, 2, 4, 5 et 6 lors des phases ultérieures.
- Remplacer le modèle macroéconomique simplifié et les décotes de prudence par des modélisations officielles approfondies (Trésor, DLF, OFCE).
- Programmer les concertations préalables avec les partenaires sociaux et les exécutifs régionaux (flexisécurité, codétermination, clarification des compétences territoriales).
