# **Projet Data Engineer :**

# **Analyse des Relations Startups - Investisseurs**

**Données brutes :** Lien vers la Google Sheet

## I - Consigne et Objectif du projet


### 1. Consigne :

En tant que data engineering, vous êtes missionné pour construire un pipeline de données permettant

&nbsp;d'analyser les mises en relation entre startups et investisseurs.

### 2\. Objectifs :

L'objectif est de mieux comprendre :

* Identifiez les points de blocage dans le processus de matchmaking
* Recommandez des actions à mener pour chaque typologie d'investisseur
* Proposez des critères de priorisation pour les relances
* La qualité et la progression des contacts,
* Les typologies d'investisseurs les plus engagés
* Les startups les plus sollicitées ou en situation de blocage.

## II - Étapes techniques à réaliser

### 1\. Collecte et ingestion des données

* Utilisez Python et sa librairie adéquates pour télécharger le fichier, effectuer le nettoyage
  et la transformation des données.
* Stockez les données dans une bdd SQLite pour exploration et traitement
* 

### 2\. Nettoyage et transformation

* Gérez les valeurs manquantes (emails, contacts)
* Uniformisez les champs (typologie d'investisseur, statut de match, etc.)
* Créez des champs dérivés utiles (ex. : nom complet du contact, jour du RDV, statut simplifié, etc.)

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

* **Python**
* **SQL**
* **Power BI**
