#!/bin/bash

# Este script crea un repositorio en GCP y un trigger de despliegue en Cloud Build.
# Requerimiento: Todo dentro de GCP, nada de GitHub.

PROJECT_ID=$(gcloud config get-value project)
echo "El proyecto actual es: $PROJECT_ID"
read -p "¿Es este tu proyecto personal (NO OESKN)? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Cancelando. Por favor, cambia a tu proyecto personal usando: gcloud config set project TU_PROYECTO"
    exit 1
fi

echo "Creando el repositorio en Cloud Source Repositories..."
gcloud source repos create lacamposm-profile || echo "El repositorio probablemente ya existe."

echo "Creando el Trigger en Cloud Build..."
gcloud builds triggers create cloud-source-repositories \
    --name="lacamposm-profile-main-deploy" \
    --repo="lacamposm-profile" \
    --branch-pattern="^main$" \
    --build-config="gcp/cloudbuild.yaml"

echo ""
echo "¡Listo! El repositorio y el trigger de GCP han sido creados."
echo "Para subir tu código por primera vez a GCP, ejecuta:"
echo "git remote add google https://source.developers.google.com/p/$PROJECT_ID/r/lacamposm-profile"
echo "git push --all google"
