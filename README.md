
# SOFTDESK API


## Description du projet

SoftDesk, une société d'édition de logiciels de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques. Cette solution, SoftDesk Support, s’adresse à des entreprises en B2B (Business to Business). 

## Mise en place et exécution en local de l'application

1. Téléchargez le projet depuis Github en clonant le projet en utilisant la commande suivante:  
```
git clone https://github.com/Antinii/Projet_10_SoftDeskApi.git
```
2. Déplacez vous dans le répertoire du projet avec la commande:
```
cd Projet_9_SoftDeskApi
```
3. Installez les dépendances à l'aide de la commande:
```
pipenv install
```
Puis, activez votre environnement virtuel avec la commande suivante:
```
pipenv shell
```
4. Effectuez les migrations:
```
pipenv run python manage.py migrate
```
5. Vous pouvez maintenant exécuter l'application en local à l'aide de la commande suivante :
```		
pipenv run python manage.py runserver
```
6. L'application est prête, accédez-y à l'addresse suivante:
```
http://127.0.0.1:8000/
```
7. Dans la base de donnée communiquée, 3 comptes ont été créés. Les noms d'utilisateurs sont les suivants :
```		
antini (superuser)
```
```		
jules
```
```
toto
```
Le mot de passe est le même pour les comptes :
```		
S3cret!!
```

Afin de générer un nouveau rapport flake8:
```		
flake8 --format=html --htmldir=rapport
```
