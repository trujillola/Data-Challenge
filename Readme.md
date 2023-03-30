# Modèles

Deux models principaux Siamois et Inception sur les branches suivantes :  
- main (Siamois) 
- app/method_resnet (Inception)  

Il faut aussi télécharger les deux models pré-entraînés joints (model_demo.h5  & weigths.h5 ) dans le dossier drive (trop gros pour github) et les mettre dans <i>application/backend/app/model</i>.  
Il faut également placer le dossier data contenant les PDF dans <i>application/backend/app</i>.

# Application  

Pour lancer l'application :

- Pour le front :  
```
cd application/front  
npm install (installer les nodes modules)  
npm run start (pour lancer l'application)
```

- Pour le back :
```
cd application/backend
pip install -r app/requirements.txt
uvicorn app.main:app
```
