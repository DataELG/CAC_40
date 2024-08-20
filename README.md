# SOLUTION RPA POUR CRÉÉR UNE BASE DE DONNÉES D’ENTRAINEMENT D’ALGORITMES DE TRADING HAUTE FREQUENCE

## Description
Ce projet vise à automatiser la collecte des données de transactions des entreprises du CAC 40 en utilisant des Azure Functions pour collecter, analyser, et rapporter les données de trading en temps réel. Le système vérifie les nouvelles entreprises, collecte les données toutes les 10 minutes pendant les heures d'ouverture du marché, et génère un rapport en fin de journée. Les données sont stockées dans une base de données Azure SQL, avec les secrets et les accès gérés de manière sécurisée. 

## Fonctionnalités Principales
- **Vérification quotidienne des entreprises** : Mise à jour automatique de la base de données des entreprises du CAC 40.
- **Collecte de données en temps réel** : Récupération des données de trading toutes les 10 minutes.
- **Rapports quotidiens** : Génération et envoi d'un rapport de fin de journée.

## Prérequis
- Compte Azure avec accès aux services Azure Functions, Azure SQL Database
- Python 3.9 pour les scripts.

## Installation et Configuration
1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/votre-repo/cac40-surveillance.git
   cd cac40-surveillance
2. **Déployez les Azure Functions**
3. **Initialisez la base de données en utilisant les scripts SQL fournis.**

## Surveillance et Maintenance
1. **Monitoring** : 
   Utilisez Azure Monitor et Application Insights pour suivre les performances et les erreurs.
2. **Alertes** : 
   Configurez des alertes pour recevoir des notifications en temps réel en cas d'erreurs critiques.