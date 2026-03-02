# Guía: Configurar Subdominio en Cloud Run con Cloudflare

## Contexto

Esta guía documenta el proceso **correcto** para conectar un subdominio de Cloudflare a un servicio de Google Cloud Run.
Fue escrita después de una sesión de debugging de ~2 horas en la que el enfoque inicial (Cloud Run Domain Mappings) falló por un problema estructural conocido.

---

## Arquitectura Final (la que funciona)

```
Usuario
  │
  ▼ HTTPS
Cloudflare Edge
  │  (SSL terminado por Cloudflare)
  │  (Worker hace proxy de la petición)
  ▼
Cloudflare Worker  ←── mamitas-care-proxy
  │
  ▼ HTTPS
Google Cloud Run
  └── insulina-viz (us-central1)
      URL: https://insulina-viz-xmk24o54ta-uc.a.run.app
```

**Lo que hace Cloudflare:** emite y gestiona el certificado SSL, recibe el tráfico, lo pasa al Worker.
**Lo que hace el Worker:** hace proxy de todas las peticiones hacia la URL interna de Cloud Run.
**Lo que hace Cloud Run:** sirve la aplicación normalmente usando su URL propia.

---

## Por qué falla el enfoque de Cloud Run Domain Mappings

El enfoque nativo de Cloud Run (`gcloud beta run domain-mappings create`) tiene un problema de **ciclo gallina-huevo**:

1. Para emitir un certificado SSL, Google necesita validar el dominio via HTTP-01 ACME challenge en:
   `http://subdominio/.well-known/acme-challenge/<token>`
2. Pero `ghs.googlehosted.com` (el frontend de Google) redirige **todo** el tráfico HTTP → HTTPS con un `302 Found`
3. HTTPS no funciona porque el certificado aún no existe
4. La validación falla → el certificado no se emite → ciclo infinito

**Síntoma:** El estado del domain mapping queda atascado en:
```yaml
reason: CertificatePending
message: Certificate issuance pending.
```

**Verificación del problema:**
```bash
curl -sI http://subdominio.tudominio.com/.well-known/acme-challenge/test
# Respuesta: HTTP/1.1 302 Found  ← esto confirma el ciclo
```

Este problema ocurre **independientemente de**:
- Si el CNAME apunta correctamente a `ghs.googlehosted.com`
- Si el dominio está verificado en Google Search Console
- Si el servicio tiene ingress `all` y acceso `allUsers`
- Si Cloudflare tiene la nube en gris (DNS Only)
- Si se recrea el domain mapping múltiples veces

---

## Solución Correcta: Cloudflare Worker como Proxy

### Prerequisitos

- Dominio en Cloudflare (cualquier plan, incluyendo Free)
- Servicio Cloud Run desplegado y funcionando con su URL propia (`*.run.app`)
- Servicio con acceso público: `allUsers` con rol `roles/run.invoker`

Verificar acceso público:
```bash
gcloud run services get-iam-policy NOMBRE_SERVICIO \
  --project ID_PROYECTO \
  --region REGION
# Debe mostrar: members: [allUsers], role: roles/run.invoker
```

---

### Paso 1: Verificar que el servicio Cloud Run funciona

```bash
curl -sI https://TU_SERVICIO-xxxx-uc.a.run.app
# Debe responder 200 OK
```

---

### Paso 2: Limpiar el DNS en Cloudflare

En Cloudflare Dashboard → **DNS** → **Records**:

- **Eliminar** cualquier CNAME que apunte a `ghs.googlehosted.com` para el subdominio
- **Eliminar** cualquier Cloud Run domain-mapping existente:

```bash
gcloud beta run domain-mappings delete \
  --domain subdominio.tudominio.com \
  --project ID_PROYECTO \
  --region REGION \
  --quiet
```

> **Nota:** Los registros CAA que se agregaron (`pki.goog`, `letsencrypt.org`) pueden quedarse — no hacen daño y son buena práctica.

---

### Paso 3: Agregar registros CAA (buena práctica)

En Cloudflare DNS → **Add record**:

| Type | Name          | Flag | Tag   | CA domain name   |
|------|---------------|------|-------|------------------|
| CAA  | tudominio.com | 0    | issue | pki.goog         |
| CAA  | tudominio.com | 0    | issue | letsencrypt.org  |

En el dropdown de "Tag", la opción correcta es: **"Only allow specific hostnames"**

---

### Paso 4: Crear el Cloudflare Worker

1. Cloudflare Dashboard → menú izquierdo → **Compute** (bajo "Build") → **Workers & Pages**
2. Clic **Create Application** → **Start with Hello World!**
3. Cambiar el nombre del Worker a algo descriptivo: `mamitas-care-proxy`
4. Clic **Deploy** (con el código Hello World — lo editaremos después)
5. Una vez en el overview del Worker → clic **Edit code**
6. Seleccionar todo (`Ctrl+A`), borrar, y pegar:

```javascript
export default {
  async fetch(request) {
    const url = new URL(request.url);
    url.hostname = "TU_SERVICIO-xxxx-uc.a.run.app"; // URL interna de Cloud Run
    url.protocol = "https:";
    return fetch(url.toString(), request);
  }
};
```

7. Clic **Deploy**

> Puedes verificar que funciona en el preview del editor — debería mostrar la app.

---

### Paso 5: Conectar el dominio al Worker

1. En el Worker → tab **Settings** → sección **Domains & Routes** → **+ Add**
2. Seleccionar **"Custom domain"**
3. Escribir: `subdominio.tudominio.com`
4. Clic **Add domain**

Cloudflare emite el certificado SSL automáticamente en ~1-2 minutos.

> **Error común:** "This domain is already in use" → significa que aún existe un CNAME en DNS. Ir a DNS → eliminar el registro del subdominio → volver a intentar.

---

### Paso 6: Verificar

```bash
# Esperar ~2 minutos y luego:
curl -sI https://subdominio.tudominio.com
# Debe responder 200 OK con headers de Cloudflare (cf-ray, etc.)
```

O simplemente abrir `https://subdominio.tudominio.com` en el navegador.

---

## Configuración SSL/TLS en Cloudflare (Edge Certificates)

Durante el proceso es importante verificar estos ajustes en Cloudflare → **SSL/TLS** → **Edge Certificates**:

| Ajuste | Valor correcto |
|--------|---------------|
| Always Use HTTPS | **OFF** (durante configuración inicial) |
| HSTS | **Deshabilitado** (no clicar "Enable HSTS") |
| Minimum TLS Version | TLS 1.0 (default) |

Con el Worker, el SSL es manejado por Cloudflare automáticamente y estas configuraciones son menos críticas.

---

## Resumen de lo que NO funciona y por qué

| Enfoque | Por qué falla |
|---------|--------------|
| Cloud Run domain-mappings | Ciclo HTTP-01 ACME challenge: Google Frontend redirige el challenge a HTTPS antes de tener certificado |
| Cloudflare proxy (nube naranja) sobre CNAME a ghs.googlehosted.com | Google Frontend cierra la conexión HTTPS sin certificado: `SSL handshake has read 0 bytes` |
| Esperar horas con domain-mapping | Puede funcionar eventualmente (24-48h) pero es poco confiable y no resuelve si ha fallado en intentos previos |

---

## Proyectos de Referencia

| Recurso | Valor |
|---------|-------|
| Dominio raíz | lacamposm.com |
| Proyecto GCP principal | lacamposm-hub |
| Proyecto GCP secundario | celtic-volt-476203-e9 |
| Servicio Cloud Run | insulina-viz (us-central1) |
| URL interna Cloud Run | https://insulina-viz-xmk24o54ta-uc.a.run.app |
| Worker Cloudflare | mamitas-care-proxy |
| Subdominio final | mamitas-care.lacamposm.com |
| Nameservers Cloudflare | adrian.ns.cloudflare.com, clay.ns.cloudflare.com |
