Deux models principaux Siamois et Resnet sur les branches suivantes :  
- main (Siamois) 
- app/method_resnet (Resnet)  

Il faut aussi télécharger les deux models pré-entraînés joints (model_demo.h5  & weigths.h5 ) dans le dossier drive (trop gros pour github) et les mettre dans application/backend/app/model.
Il faut également placer le dossier data contenant les PDF dans application/backend/app.

Pour lancer l'application :

- Pour le front :
'''cd application/front  
npm install (installer les nodes modules)  
npm run start (pour lancer l'application)'''

- Pour le back :
'''cd application/backend
pip install -r app/requirements.txt
uvicorn app.main:app'''