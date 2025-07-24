# **Projet Data : Analyse des Relations Startups - Investisseurs**





## I - Consigne et Objectif du projet

### 1. Consigne :

En tant que data engineering, vous êtes missionné pour construire un pipeline à partir d’un fichier brut de données.
Permettant aini d'analyser les mises en relation entre startups et investisseurs. 
Chaque ligne représente une interaction ou un rendez-vous entre une start-up et un investisseur, avec des informations variées (typologie, statut, contact, etc.).

### 2\. Objectifs :

L'objectif est normaliser les données pour une meilleure analyse des interactions:

* D'identifiez les points de blocage dans le processus de matchmaking
* Recommandez des actions à mener pour chaque typologie d'investisseur
* Proposez des critères de priorisation pour les relances
* La qualité et la progression des contacts,
* Les typologies d'investisseurs les plus engagés
* Les startups les plus sollicitées ou en situation de blocage.

    **Note** : [Lien de téléchargement](https://docs.google.com/spreadsheets/d/1-ozQDxIBwo-XhgNrfqDZaPwlN9j88c8E/export?format=xlsx&id=1-ozQDxIBwo-XhgNrfqDZaPwlN9j88c8E "lien google Sheetsheat") des données brutes.

### **3. Description des données** :

|        Nom de colonne        | Description                                                               |
| :---------------------------: | :------------------------------------------------------------------------ |
|     **Id. unique**     | Identifiant unique de chaque ligne d’enregistrement                      |
|      **Id.Match**      | Identifiant du match entre la start-up et l’investisseur                 |
|      **Start-up**      | Nom de la start-up                                                        |
|     **Id.Startup**     | Identifiant numérique attribué à chaque start-up                       |
|   **Contact client**   | Nom du contact côté client (start-up)                                   |
|    **Investisseur**    | Nom de l’investisseur                                                    |
|   **Id.Investisseur**   | Identifiant de l’investisseur                                            |
|       **Prénom**       | Prénom du contact principal chez l’investisseur                         |
|       **Nom CP**       | Nom du contact principal (CP = Contact Principal)                         |
| **Investisseur.statut** | Statut de l’investisseur dans la relation (ex : prospect, engagé, etc.) |
|  **Client Principal**  | Le contact de l'Investisseur                                             |
|      **Typologie**      | Catégorie de l’investisseur (exemples détaillés ci-dessous)           |
|    **Statut match**    | État de l’interaction (match confirmé, en cours, rejeté, etc.)        |
|       **Dépôt**       | Canal de prise de contact avec l'investisseur                             |
|   **Montant estimé**   | Montant estimé de l’investissement (souvent numérique ou texte libre)  |
|       **RDV le**       | Date prévue du rendez-vous avec l’investisseur                          |
|     **Unnamed: 16**     | Colonne vide                                                              |
|     **Commentaire**     | Notes ou remarques libres sur le match ou l’interaction                  |
|    **Adresse email**    | Adresse e-mail du contact principal (investisseur ou client               |

**Focus Colonne `Typologie` :**

|            Valeur            | Interprétation                                     |
| :--------------------------: | --------------------------------------------------- |
|          `1.3 VC`          | Venture Capital classique                           |
|         `1.4 CVC`         | Corporate Venture Capital                           |
|          `1.0 BA`          | Business Angel                                      |
|        `2.1 Banque`        | Organisme bancaire                                  |
|          `1.2 FO`          | Family Office                                       |
| `1.5 Prestataire (Equity)` | Prestataire de services avec prise de participation |
|    `2.2 Accélérateur`    | Structure d’accélération de start-ups            |
|     `4.0 Entrepreneur`     | Investissement provenant d’un entrepreneur         |
|           `nan`           | Non renseignée                                     |

**Focus Colonne `Investisseur.statut`**

|         Valeur         | Signification                                               |
| :---------------------: | ----------------------------------------------------------- |
|    `0.0 Associé`    | Membre de l’équipe ou associé interne à la structure    |
|     `0.1 Client`     | Client de l'organisation                                    |
|   `0.2 Partenaire`   | Partenaire identifié, non client                           |
|  `2.0 Itera Friend`  | Contact connu de manière informelle (ami/partenaire Itera) |
| `2.1 Contact établi` | Lien confirmé, contact existant avec échange              |
| `2.2 Co-investisseur` | A déjà investi ou peut co-investir dans un projet         |
|    `3.1 Contacté`    | A été contacté (par email, téléphone, etc.)            |
|   `3.2 A contacter`   | Doit encore être contacté (en attente d’action)          |
|  `3.3 Email rebond`  | Adresse email invalide ou message retourné                 |
| `3.5 Trouver contact` | Aucun contact identifié, recherche en cours                |
|   `4.1 A étudier`   | Profil à analyser ou à prioriser plus tard                |
|     `4.2 Vivier`     | Gardé en base comme prospect potentiel                     |
|   `4.3 Hors-Scope`   | Investisseur non adapté au profil recherché               |
| `6.0 Leveur de fonds` | Professionnel agissant comme intermédiaire (leveur)        |
|    `9.0 KO Itera`    | Rejeté par l’équipe Itera                                |
| `9.1 KO Unsubscribe` | Contact s’est désinscrit / ne veut plus être contacté   |
|   `9.5 A supprimer`   | À retirer de la base pour nettoyage                        |
|    `9.8 KO Arret`    | Processus abandonné ou investisseur s’est retiré         |
|         `nan`         | Non renseignée                                             |

**Focus Colonne : `Statut match`**

|          Valeur          | Signification                                       |
| :----------------------: | :-------------------------------------------------- |
|       `0.0 Deal`       | Match réussi, accord signé ou deal finalisé      |
|    `1.0 Potentiel`    | L’investisseur est considéré comme intéressant  |
| `2.0 Trouver contact` | Il manque un point de contact pour avancer          |
|   `2.1 A présenter`   | Start-up à présenter à l’investisseur           |
| `2.2 Dossier envoyé` | Dossier de la start-up déjà transmis              |
|      `2.3 En RDV`      | Rendez-vous planifié ou réalisé                  |
|     `2.6 relancer`     | Nécessite une relance (pas encore de retour)       |
|     `2.7 Stand by`     | Mis en pause, temporairement sans suite             |
|    `3.0 Intérêt`    | L’investisseur a manifesté un intérêt           |
|    `3.1 Intention`    | Intention d’aller plus loin (investir, échanger)  |
|    `7.1 Hors Scope`    | Ne correspond pas aux critères de l’investisseur  |
| `7.2 NoGo - Deal Flow` | Rejet au niveau du pipeline de projets              |
|    `7.3 NoGo - RDV`    | Rejet après un rendez-vous                         |
| `7.4 Deal concurrent` | Un autre deal est passé en priorité (concurrence) |

## II - Étapes techniques à réaliser

### 1\. Collecte, nettoyage et transformation des données :

* Utilisez Python et les librairies adéquates pour télécharger le fichier, effectuer le nettoyage
  et la transformation des données.
* Gérez les valeurs manquantes
* Uniformisez les champs
* Créez des champs dérivés utiles

### 2\. Stockage des données :

- Stockez les données dans une bdd SQLite pour exploration et traitement

### 3\. Analyse des données

* Combien de matchs ont atteint le statut "2.1 Contact établi" ou "0.0 Deal" ?
* Quelle est la répartition des investisseurs par typologie (VC, BA, CVC, etc.) ?
* Quels sont les investisseurs avec le plus de contacts "à relancer" ?
* Classez les startups par nombre de mises en relation et par statut de match
* Repérez les investisseurs qui n'ont jamais répondu (statut "KO" ou vide)

### 4\. Visualisation sous Power BI

* Connecter Power BI à la base SQLite
* Construisez des visualisations utiles pour les équipes opérationnelles :

  * Histogramme du nombre de relations par startup
  * Camembert des typologies d'investisseurs engagés
  * Carte de chaleur : statut du match par typologie
  * Tableau des investisseurs à relancer

## III - Technologies à utiliser

* Python
* SQL
* Power BI
