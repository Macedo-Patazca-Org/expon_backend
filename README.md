# 📚 Expon Backend API

Este es el backend del proyecto **Expon**, una plataforma construida en Python con **FastAPI** y conectada a una base de datos **PostgreSQL** con el objetivo para apoyar el desarrollo de habilidades de comunicación oral mediante análisis de sentimientos y retroalimentación.

---

## 🚀 Tecnologías

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Uvicorn
- Pydantic
- Passlib (hash de contraseñas)
- Dotenv (variables de entorno)

---

## ✅ Requisitos previos

Asegúrate de tener instalado:

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [PostgreSQL](https://www.postgresql.org/download/) + pgAdmin
- [Visual Studio Code](https://code.visualstudio.com/)
  - Extensión de Python (opcional pero recomendada)

---

## 📥 Clonación del proyecto

```bash
git clone https://github.com/TU_USUARIO/expon_backend.git
cd expon_backend
```

---

## 🛠️ Instalación

1. Crear entorno virtual:

```bash
python -m venv env
```

2. Activar entorno virtual:

- En Windows:
  ```bash
  env\Scripts\activate
  ```

- En macOS/Linux:
  ```bash
  source env/bin/activate
  ```

3. Instalar dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🗄️ Configurar base de datos

1. Crea una base de datos en PostgreSQL:

```sql
CREATE DATABASE expon_db;
```

2. Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA@localhost:5432/expon_db
```

📌 **Nota**: Cambia `TU_CONTRASEÑA` por tu contraseña real de PostgreSQL.

---

## ▶️ Ejecutar el servidor

```bash
uvicorn main:app --reload
```

Abre en tu navegador:
- API: http://localhost:8000
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
