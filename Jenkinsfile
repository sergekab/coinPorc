pipeline {
  agent any

  stages {
    stage('Préparation') {
      steps {
        echo "Étape 1 : Préparation du dossier de déploiement"
      }
    }

    stage('Clonage du dépôt') {
      steps {
        echo "Étape 2 : Clonage du dépôt Git"
      }
    }

    stage('Création de l’environnement virtuel') {
      steps {
        echo "Étape 3 : Création et activation de l'environnement Python (venv)"
      }
    }

    stage('Installation des dépendances') {
      steps {
        echo "Étape 4 : Installation des dépendances via pip"
      }
    }

    stage('Migration de la base de données') {
      steps {
        echo "Étape 5 : Exécution des migrations Django"
      }
    }

    stage('Collecte des fichiers statiques') {
      steps {
        echo "Étape 6 : Collecte des fichiers statiques Django"
      }
    }

    stage('Redémarrage de l’application') {
      steps {
        echo "Étape 7 : Redémarrage de Gunicorn (ou autre serveur)"
      }
    }

    stage('Fin du pipeline') {
      steps {
        echo "Pipeline terminé avec succès"
      }
    }
  }
}
