# 🚀 Social Network

A Django-based social network project.

## 📦 Installation

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/Sayidboy7/Social_Network.git
```

### 2. Navigate to the project directory

```bash
cd Social_Network
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 5. Install project dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the development server

```bash
uvicorn config.asgi:application --reload
```

The application will be available at:

```
http://127.0.0.1:8000
```

### 7. Database setup

Make sure all database tables are created before running the project.

Run the migrations:

```bash
python manage.py migrate
```

If needed, create a superuser:

```bash
python manage.py createsuperuser
```

---

## 🛠 Tech Stack

- Python
- Django
- Django Channels
- Redis
- Uvicorn
- WebSockets
- SQLite

---

## 📂 Project Structure

```
Social_Network/
│── auth_network/
│── chat/
│── config/
│── Social_Network/
│── media/
│── static/
│── templates/
│── manage.py
│── requirements.txt
└── README.md
```

---

## 🚀 Features

- 👤 User Authentication
- 📝 Posts
- 💬 Real-time Chat (WebSocket)
- ❤️ Social Features
- 📱 Responsive UI

---

## 📄 License

This project is available for educational and personal use.
