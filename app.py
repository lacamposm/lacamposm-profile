from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    skills = [
        {"name": "GCP / Infrastructure", "level": "Expert", "icon": "fa-brands fa-google", "desc": "Designing and deploying highly available, scalable infrastructure on Google Cloud Platform."},
        {"name": "Backend Development", "level": "Expert", "icon": "fa-brands fa-python", "desc": "Building robust, secure, and performant backend services with Python, Flask, and FastAPI."},
        {"name": "Workflow Automation", "level": "Expert", "icon": "fa-solid fa-cogs", "desc": "Automating complex business processes and data pipelines using n8n and Python scripts."},
        {"name": "Database Architecture", "level": "Advanced", "icon": "fa-solid fa-database", "desc": "Modeling data and optimizing query performance using PostgreSQL."},
        {"name": "Containerization", "level": "Advanced", "icon": "fa-brands fa-docker", "desc": "Containerizing applications using Docker and orchestrating them with Docker Compose and Cloud Run."},
        {"name": "AI/Agents", "level": "Advanced", "icon": "fa-solid fa-brain", "desc": "Integrating LLMs and generative AI tools to build intelligent and autonomous agents."}
    ]
    return render_template('index.html', skills=skills)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
