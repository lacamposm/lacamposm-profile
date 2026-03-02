# Guía Definitiva de Despliegue en GCP (Cloud Run) con Cloudflare

Esta guía documenta todo el proceso técnico paso a paso para desplegar proyectos (como la página de perfil en FastAPI) en Google Cloud Platform (GCP) utilizando **Cloud Run** como infraestructura sin servidor (serverless), integrado con un flujo de **CI/CD vía Cloud Build** y gestionando el dominio con **Cloudflare**.

Está pensada para ser tu referencia maestra cada vez que desees lanzar un nuevo microservicio o proyecto bajo tu dominio principal (`lacamposm.com`) o en subdominios futuros (`api.lacamposm.com`, etc).

---

## 1. Preparación Local y Contenedor (Docker)

Todo el código que subas a Cloud Run debe estar encapsulado en una imagen de Docker.

1. **Elegir el Framework y Servidor:**
   Migramos de Flask+Gunicorn a **FastAPI+Uvicorn** para tener una base asíncrona y robusta. 
   *(Importante: En los archivos HTML, siempre llamar las rutas estáticas de forma relativa, ej. `href="/static/style.css"`, para evitar que Cloud Run genere URLs erróneas con el SSL de los proxies de GCP).*
2. **Definir el `Dockerfile`:**
   Debe instalar dependencias y levantar la aplicación mapeando el puerto `8080` (es la costumbre de Cloud Run).
   ```dockerfile
   FROM python:3.12-slim
   ENV PYTHONUNBUFFERED=True
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . ./
   CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
   ```

---

## 2. Configuración de CI/CD (Cloud Build)

El archivo `cloudbuild.yaml` coordina la automatización cada vez que hacemos un `git push` a `main`.

1. **Crear `gcp/cloudbuild.yaml`** en el repositorio.
2. Definir los tres pasos principales:
   - **Build:** Construye la imagen de Docker usando el registro `us-central1-docker.pkg.dev` (Artifact Registry).
   - **Push:** Envía la imagen compilada al Artifact Registry de tu proyecto (`lacamposm-hub`).
   - **Deploy:** Despliega esa imagen hacia el servicio de **Cloud Run**. Aquí debes usar banderas como `--allow-unauthenticated` para que sea público.

> **Tip de Logging:** Se añadió `options: logging: CLOUD_LOGGING_ONLY` para que la salida de la consola de Cloud Build se guarde ordenadamente en caso de errores.

---

## 3. Configuración en Google Cloud Platform (La Primera Vez)

Para el proyecto de GCP (`lacamposm-hub`):
1. **Facturación:** Asegúrate de vincular tu cuenta de Billing (Facturación).
2. **APIs Habilitadas:** Se requirieron las siguientes APIs:
   - Cloud Run API
   - Cloud Build API
   - Artifact Registry API
3. **Artifact Registry:** Se crea un repositorio Docker dentro de la región correspondiente (ej. `us-central1`).
4. **Triggers (Activadores):** 
   - Se va a "Cloud Build > Activadores" y se crea uno enlazado a tu repositorio de GitHub. 
   - Evento: Insertar en una rama (Push to branch).
   - Rama: `^main$`.
   - Archivo de configuración: Buscar ruta a `gcp/cloudbuild.yaml`.

---

## 4. El Triage del Flujo de Trabajo (Git Workflow)

Para evitar romper producción, la regla de oro para GCP es usar **Pull Requests (PR)**. El flujo para un nuevo despliegue es:
1. Siempre trabajar en una rama aparte: `git checkout -b feature/lo-que-sea` o `fix/lo-que-sea`.
2. Una vez que estés satisfecho en tu ambiente local, haces `git push origin feature/lo-que-sea`.
3. Revisas los cambios y abres un **Pull Request (PR)** hacia la rama `main` en GitHub.
4. **Merge**: Al momento de aceptar el PR, GitHub avisa a Cloud Build. Ese **merge es el gatillo** que acciona el despliegue automático hacia GCP.

*(Si hay un error en Cloud Run como acceso denegado (Forbidden), puedes forzar el permiso público con: `gcloud run services add-iam-policy-binding NOMBRE_SERVICIO --member="allUsers" --role="roles/run.invoker"`. )*

---

## 5. El Desafío Final: Dominio Personalizado & Cloudflare

Una vez que la aplicación existe en `.run.app`, el mundo no la verá en tu dominio sin un enlazamiento correcto por DNS.

### A. Verificación en Central Webmaster
Google te obliga a probar que el dominio es tuyo en cada nuevo Proyecto:
1. Desde Google Cloud Console, ve a **Cloud Run > Mapeo de Dominios (Domain mappings)**.
2. Añades el servicio y pones que quieres enlazar tu URL (`lacamposm.com`).
3. Te pedirá **Verificar en Search Console / Webmaster Central**.
4. Te dará un código TXT: `google-site-verification=...`.
5. Ese código debes llevarlo tú o Cloudflare mismo automáticamente (a través del flujo guiado conectando ambos servicios) a tu administrador DNS. En caso manual, creas un registro tipo `TXT` en Cloudflare con Nombre `@` y como valor ese gran código. Tras ello, Google te aprueba como dueño absoluto de esa URL.

### B. Enlazar hacia GCP a través de Cloudflare
Ya verificado, Cloud Run te pedirá colocar una lista de 4 registros IPv4 y 4 registros IPv6:
1. En **Cloudflare** eliminas todos los antiguos registros A o CNAME de hosts del pasado.
2. Agregas 4 registros tipo `A` (ej. IP `216.239.32.21`, etc). 
3. Agregas 4 registros tipo `AAAA` (IPv6).
4. **Vital:** En Cloudflare, todos estos 8 registros vinculados a Cloud Run deben encenderse en estado **DNS Only (Nubecita Gris)**. Esto desactiva el firewall proxy de Cloudflare momentáneamente para que Google lance el candado **SSL (HTTPS)** en su propia nube hacia tu página, un proceso que toma menos de 15 minutos en propagarse. 

---

## 6. Siguientes Servicios (Futuro)

Cuando decidas instalar un nuevo sistema (como las analíticas, backends o agentes):
- Creas el servicio nuevo en Cloud Run.
- Cuando vayas a "Dominios Personalizados", GCP ya sabrá que la URL es tuya, así que **NO te pedirá Webmaster Verification de nuevo**.
- Simplemente seleccionarás un subdominio: `api.lacamposm.com`.
- Cloud Run te dará un nuevo registro (seguramente un CNAME hacia `ghs.googlehosted.com`). 
- Vas a Cloudflare, agregas ese nuevo CNAME y listo. 

> ¡El trabajo duro de infraestructura arquitectónica a nivel fundacional de lacamposm.com ya ha sido superado con éxito!
