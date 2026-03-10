from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

translations = {
    "en": {
        "title": "Andres Campos | Data Scientist & ML Engineer",
        "description": "I extract actionable insights from data and build intelligent AI systems, backed by scalable cloud infrastructure.",
        "nav_expertise": "Expertise",
        "nav_work": "History",
        "nav_connect": "Connect",
        "badge_available": "Available for new projects",
        "section_background": "Professional History",
        "experience": [
            {"role": "AI Engineer", "company": "oeskn", "period": "Present", "desc": "Building AI-driven skincare solutions in a fast-paced startup environment."},
            {"role": "Data Scientist", "company": "Instituto Geográfico Agustín Codazzi (IGAC)", "period": "3 years", "desc": "Designed and implemented ML models for geographic, cadastral, and spatial datasets."}
        ],
        "education": [
            {"degree": "Magister en Ciencias - Matemáticas", "institution": "Universidad Nacional de Colombia", "year": "2014"},
            {"degree": "Matemático", "institution": "Universidad Nacional de Colombia", "year": "2010"}
        ],
        "hero_greeting": "Hi, I'm Andres Campos",
        "hero_title_1": "Extracting Value from Data",
        "hero_title_2": "& Building ML / AI Systems.",
        "hero_tagline": "I help organizations train robust machine learning models, analyze complex datasets, and deploy intelligent AI agents, supercharged by efficient cloud architectures.",
        "btn_discuss": "Discuss a Project",
        "btn_code": "Explore Code",
        "social_proof": "Trusted by clients for delivering accurate models and scalable data solutions.",
        "expertise_title": "Technical",
        "expertise_subtitle": "Expertise",
        "expertise_desc": "Focused on the intersection of data science, machine learning, and autonomous agents.",
        "cta_title": "Ready to unlock your data's potential?",
        "cta_desc": "Let's build models that drive business value and intelligent systems that automate effectively.",
        "cta_btn": "Connect on LinkedIn",
        "footer_tagline": "Engineering the future, one node at a time.",
        "footer_rights": "© 2026 Andres Campos. Building from Bogotá.",
        "form_title": "Start a Conversation",
        "form_name": "Name",
        "form_email": "Email",
        "form_message": "Project Details",
        "form_send": "Send Message",
        "form_close": "Close",
        "form_success_title": "Message Received",
        "form_success_desc": "I'll be in touch soon. Keep building and pushing boundaries!",
        "skills": [
            {"name": "Data Science & ML", "level": "Expert", "icon": "fa-solid fa-chart-network", "desc": "Applying advanced machine learning algorithms to extract actionable insights from complex datasets."},
            {"name": "AI & Autonomous Agents", "level": "Expert", "icon": "fa-solid fa-brain", "desc": "Building robust, stateful multi-agent applications and cognitive architectures using LangGraph and its ecosystem."},
            {"name": "Workflow Automation", "level": "Expert", "icon": "fa-solid fa-cogs", "desc": "Automating business processes and data pipelines using n8n and Python scripting."},
            {"name": "Data Architecture", "level": "Advanced", "icon": "fa-solid fa-database", "desc": "Designing Data Lakes and managing data governance and analytics platforms with Databricks Unity Catalog."},
            {"name": "Backend Development", "level": "Advanced", "icon": "fa-brands fa-python", "desc": "Building robust, secure, and performant backend services and APIs with Python and FastAPI."},
            {"name": "GCP / Infrastructure", "level": "Intermediate", "icon": "fa-brands fa-google", "desc": "Designing and deploying highly available, scalable infrastructure on Google Cloud Platform to support AI/ML workloads."},
            {"name": "Academic Instruction", "level": "Master's Professor", "icon": "fa-solid fa-graduation-cap", "desc": "Teaching advanced concepts in Data Science, Machine Learning, and AI at the postgraduate level."},
        ]
    },
    "es": {
        "title": "Andrés Campos | Data Scientist & Machine Learning",
        "description": "Extraigo valor de los datos y construyo sistemas de IA inteligentes, respaldados por infraestructura en la nube escalable.",
        "nav_expertise": "Habilidades",
        "nav_work": "Trayectoria",
        "nav_connect": "Conectar",
        "badge_available": "Disponible para nuevos proyectos",
        "section_background": "Trayectoria Profesional",
        "experience": [
            {"role": "AI Engineer", "company": "oeskn", "period": "Actualmente", "desc": "Construyendo soluciones de skincare impulsadas por IA en un entorno de startup ágil."},
            {"role": "Data Scientist", "company": "Instituto Geográfico Agustín Codazzi (IGAC)", "period": "3 years", "desc": "Diseño e implementación de modelos de ML para datos geográficos, catastrales y espaciales."}
        ],
        "education": [
            {"degree": "Magíster en Ciencias - Matemáticas", "institution": "Universidad Nacional de Colombia", "year": "2014"},
            {"degree": "Matemático", "institution": "Universidad Nacional de Colombia", "year": "2010"}
        ],
        "hero_greeting": "Hola, soy Andrés Campos",
        "hero_title_1": "Extrayendo Valor de los Datos",
        "hero_title_2": "y Construyendo Sistemas ML / IA.",
        "hero_tagline": "Ayudo a las organizaciones a entrenar modelos de IA robustos, analizar datasets complejos y desplegar agentes autónomos, potenciados por arquitecturas en la nube.",
        "btn_discuss": "Discutir un Proyecto",
        "btn_code": "Explorar Código",
        "social_proof": "Confianza de clientes por entregar modelos precisos y arquitecturas sólidas.",
        "expertise_title": "Dominios",
        "expertise_subtitle": "Técnicos",
        "expertise_desc": "Centrado en la intersección de la ciencia de datos, machine learning y agentes autónomos.",
        "cta_title": "¿Listo para potenciar tus datos?",
        "cta_desc": "Construyamos modelos que generen valor para el negocio y sistemas que automaticen inteligentemente.",
        "cta_btn": "Conecta en LinkedIn",
        "footer_tagline": "Ingeniando el futuro, un nodo a la vez.",
        "footer_rights": "© 2026 Andrés Campos. Construyendo desde Bogotá.",
        "form_title": "Iniciar una Conversación",
        "form_name": "Nombre",
        "form_email": "Correo",
        "form_message": "Detalles del Proyecto",
        "form_send": "Enviar Mensaje",
        "form_close": "Cerrar",
        "form_success_title": "Mensaje Recibido",
        "form_success_desc": "Me pondré en contacto pronto. ¡Sigue construyendo y rompiendo límites!",
        "skills": [
            {"name": "Ciencia de Datos y ML", "level": "Experto", "icon": "fa-solid fa-chart-network", "desc": "Aplicación de algoritmos avanzados de machine learning para extraer insights de datasets complejos."},
            {"name": "IA y Agentes Autónomos", "level": "Experto", "icon": "fa-solid fa-brain", "desc": "Construcción de aplicaciones multi-agente robustas y arquitecturas cognitivas utilizando LangGraph y su ecosistema."},
            {"name": "Automatización de Flujos", "level": "Experto", "icon": "fa-solid fa-cogs", "desc": "Automatización de procesos y pipelines de datos utilizando n8n y scripts en Python."},
            {"name": "Arquitectura de Datos", "level": "Avanzado", "icon": "fa-solid fa-database", "desc": "Diseño de Data Lakes y gobernanza/analítica de datos mediante Databricks Unity Catalog."},
            {"name": "Desarrollo Backend", "level": "Avanzado", "icon": "fa-brands fa-python", "desc": "Construcción de servicios backend robustos, APIs y arquitecturas escalables usando Python y FastAPI."},
            {"name": "GCP / Infraestructura", "level": "Intermedio", "icon": "fa-brands fa-google", "desc": "Diseño y despliegue de infraestructura altamente disponible en Google Cloud para soportar cargas de IA/ML."},
            {"name": "Docencia Académica", "level": "Docente de Maestría", "icon": "fa-solid fa-graduation-cap", "desc": "Enseñanza de conceptos avanzados en Ciencia de Datos, Machine Learning e IA a nivel posgrado."},
        ]
    }
}

@app.get('/', response_class=HTMLResponse)
async def index(request: Request, lang: str = 'es'):
    if lang not in ['en', 'es']:
        lang = 'es'
    
    content = translations[lang].copy()
    content['current_lang'] = lang
    content['request'] = request
    return templates.TemplateResponse("index.html", content)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
