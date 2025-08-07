
# 🧠 Social Media Feed Backend – ProDev BE

## 🚀 Overview

This project is a full-stack social media backend built with Django and GraphQL, featuring real-time chat, notifications, and user interactions (likes, comments). It also includes a simple Bootstrap frontend for both user and admin interfaces. The backend is optimized for scalability and advanced querying.

---

## 🎯 Project Goals

- Build a scalable GraphQL-based social media backend.
- Enable flexible querying for posts and user interactions.
- Integrate real-time features like notifications and chat.
- Design a responsive Bootstrap frontend for users and admins.

---

## 🛠️ Technologies Used

| Component         | Technology             |
|------------------|------------------------|
| Backend           | Django, GraphQL (Graphene) |
| Database          | PostgreSQL             |
| Realtime Layer    | Django Channels + Redis |
| Auth              | JWT (django-graphql-jwt) |
| Frontend (UI)     | HTML/CSS + Bootstrap   |
| Testing & API     | GraphQL Playground     |
| Deployment        | Render / Railway / etc. |

---

## 📁 Project Structure

```bash
socialmedia/
├── feed/              # Main app (posts, comments, likes, notifications)
├── users/             # Custom user model
├── chat/              # Real-time messaging
├── templates/         # HTML templates (Bootstrap)
├── static/            # CSS/JS files
├── socialmedia/       # Project settings and routing
├── schema.py          # GraphQL root schema
├── routing.py         # WebSocket routing
├── asgi.py            # ASGI server setup for Channels
├── requirements.txt   # Python dependencies
```

---

## 📦 Features

### ✅ Post Management
- Create, update, and delete posts
- Like and comment on posts
- View all posts with full interaction data

### 🔁 Interactions & Notifications
- Real-time likes/comments generate notifications
- Notifications are marked read/unread
- Notifications are received instantly via WebSocket

### 💬 Chat System (Real-Time)
- Send/receive messages instantly
- One-to-one messaging via WebSockets
- Stores full chat history

### 👥 User System
- Register/Login via JWT
- Admin and regular user roles
- Admin dashboard to manage content

### 🧪 GraphQL API
- Queries: fetch posts, comments, notifications, messages
- Mutations: createPost, addComment, likePost, sendMessage
- Authenticated endpoints using JWT

---

## 🔨 Setup & Installation

1. **Clone the repo:**
```bash
git clone https://github.com/yourname/socialmedia-backend.git
cd socialmedia-backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure PostgreSQL in `settings.py`**

5. **Run migrations and create superuser:**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Start development server:**
```bash
python manage.py runserver
```

---

## 🌐 WebSocket Setup (Chat & Notifications)

1. **Install Redis server locally:**
```bash
sudo apt install redis
redis-server
```

2. **Install Channels & configure:**
```bash
pip install channels channels-redis
```

3. **Add to `settings.py`:**
```python
ASGI_APPLICATION = "socialmedia.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

---

## 🧪 API Testing

- Access GraphQL Playground at:
```
http://localhost:8000/graphql/
```

- Use headers:
```json
{
  "Authorization": "JWT <your_token>"
}
```

---

## 📌 Key GraphQL Operations

### Queries
- `allPosts`
- `post(id)`
- `comments(postId)`
- `notifications`
- `messages(userId)`

### Mutations
- `createPost(title, content)`
- `addComment(postId, content)`
- `likePost(postId)`
- `sendMessage(toUserId, content)`
- `markNotificationAsRead(id)`

---

## 🧰 Admin Panel

- URL: `http://localhost:8000/admin/`
- Manage users, posts, comments, and site data

---

## 👨‍🎨 Frontend Pages (Bootstrap)

| Page | Description |
|------|-------------|
| Home | Feed with posts, like/comment buttons |
| Post Detail | View post + comments |
| Notifications | List unread notifications |
| Chat | Real-time chat interface |
| Admin Dashboard | Manage content, view stats |

---

## 📌 Git Commit Workflow

| Type | Description |
|------|-------------|
| `feat:` | New feature (e.g., `feat: add comment mutation`) |
| `fix:` | Bug fix |
| `perf:` | Performance improvement |
| `docs:` | Documentation update |
| `refactor:` | Code refactor |
| `test:` | Adding or updating tests |

---

## ✅ To Do List

- [x] Setup Django + PostgreSQL + GraphQL
- [x] Build Post, Like, Comment models
- [x] Implement GraphQL API with queries/mutations
- [x] Add real-time notifications using Channels
- [x] Integrate one-to-one real-time chat
- [x] Create basic Bootstrap frontend
- [ ] Add deployment scripts & environment configs
- [ ] Write unit tests and finalize docs

---

## 📬 Contact

For questions or collaboration, contact [achraf.kassimi.1995@gmail.com](mailto:achraf.kassimi.1995@gmail.com)

---

## in CMD (Command) or Powershell run this code, it works fine:
- validation
⦁	python -m django --help
- start a new project
⦁	python -m django startproject socialmedia

⦁   python -m venv venv 
⦁   cd venv
⦁   .\Scripts\activate
pip install django
python.exe -m pip install --upgrade pip
⦁   pip freeze > requirements.txt
python manage.py startapp feed == >  But: Regrouper les modèles des posts, likes, commentaires, etc


python manage.py makemigrations
python manage.py migrate


----
Server [localhost]: localhost
Database [postgres]: socialdb
Port [5432]: 5432
Username [postgres]: postgres
1234
----
socialdb=# \dt liste of table li kaynin f la base

socialdb=# \d+ users_customuser description ta3 table les Colonnes 

Common psql Meta-commands:
\l or \list: Lists all available databases. Use \l+ for more details.
\c <database_name> or \connect <database_name>: Connects to a different database.
\dt: Lists all tables in the current database. Other similar commands include \di (indexes), \dv (views), \ds (sequences), \df (functions), \du (users).
\d <table_name>: Describes the structure of a specific table, including columns, types, and indexes.
\dn: Lists all schemas.
\s: Displays command history.
\o <file_name>: Redirects query output to a file.
\i <file_name>: Executes commands from a specified file.
\timing: Toggles the display of query execution time.
\q: Exits the psql shell.
\?: Displays a list of all psql meta-commands.
\h <SQL_command>: Provides syntax help for a specific SQL command (e.g., \h SELECT).
----
pip install graphene-django django-graphql-jwt channels channels-redis
graphene-django: pour GraphQL
django-graphql-jwt: auth via JWT
channels & channels-redis: WebSocket pour le chat/notifications

python manage.py startapp users
python manage.py startapp social

project/
│
├── users/
│   └── models.py → CustomUser
│
├── social/
│   └── models.py → Post, Comment, Like, Message, Notification
│
└── settings.py → AUTH_USER_MODEL = 'users.CustomUser'

Username: achraf
Email address: achraf@gmail.com
Password: 1234
Password (again): 1234

-----------------------
✅ 🗓 Jour 1 – Initialisation du Projet
🎯 Objectifs :
Créer et configurer le projet Django avec PostgreSQL

Créer l'app user avec modèle CustomUser

Définir les bases du projet (venv, git, config)

📌 Étapes réalisées :
django-admin startproject socialmedia_backend

Création du virtualenv et installation de Django + psycopg2

Configuration PostgreSQL dans settings.py

Création de l'app user

Définition du modèle CustomUser (is_admin, hérite de AbstractUser)

Ajout de AUTH_USER_MODEL = 'user.CustomUser' dans settings.py

Enregistrement de l'app user dans INSTALLED_APPS

Migrations et création du superuser

Initialisation de Git et 1er commit feat: setup project with custom user

✅ 🗓 Jour 2 – Modélisation des données sociales
🎯 Objectifs :
Créer l'app feed et modéliser :

Post

Comment

Like

Message

Notification

Préparer le schéma de base pour interactions sociales

📌 Étapes réalisées :
Création de l’app feed

Suppression de l’ancienne app social (si existante)

Création des modèles dans feed/models.py

Importation depuis user.models.CustomUser

Création du schéma UML (SocialMediaFeed_UML.png)

Lancement des migrations

Ajout du modèle au admin.py si besoin

Commit Git : feat: add post, comment, like, message, notification models
-----------------------

username 'test17'
email	 'hhhhh@gmail.com'
password1	 'Achraf12-'
password2	 'Achraf12-'


username	 'tras'
email	 'tras@gmail.com'
password1	 'Achraf12-'
password2	 'Achraf12-'


username	 'koko'
email	 'koko@gmail.com'
password1	 'Achraf12-'
password2	 'Achraf12-'

User momo registered successfully with password: Achraf12-


--> nzido 
jwt
page admin en global = liste user ... statistic
session
cokise
verification ta3 user wach connecte wla la
page 404

 ----------------
For Windows:
Command Prompt (CMD).
Code

    your_venv_name\Scripts\activate.bat
PowerShell.
Code

    your_venv_name\Scripts\Activate.ps1
Git Bash or other Unix-like shells:
Code

    source your_venv_name/Scripts/activate
For macOS and Linux:
Bash, Zsh, or other Unix-like shells:
Code

    source your_venv_name/bin/activate
 ----------------


 # 1.Users
user1 = CustomUser.objects.create_user(username="kassimi", email="kassimi@example.com", password="testpass123")
user2 = CustomUser.objects.create_user(username="fatima", email="fatima@example.com", password="pass456")

Post.objects.create(author=user1, content="Salam 3likom! Hadhi awel post dyali 😊")
Post.objects.create(author=user2, content="J'aime ce projet Django ❤️")
Post.objects.create(author=user1, content="Kanbni la recherche tatmchi mzyan! 👀")
----------------------------------------

❌ شنو مازال خاصنا:
🔄 Like System (بشكل فعّال):
⏳ Backend implementation (toggle like/unlike)

⏳ Show total likes per post

⏳ Ajax (optional) for real-time like without reload

📡 Real-time Chat (WebSocket or Basic):
❌ Chat app (views, urls, templates)

❌ List of users to chat with

❌ Message sending interface (form)

❌ Save & render chat messages

✨ Extra Features (اختياري):
⏳ Pagination for posts

⏳ Profile image (avatar)

⏳ User bio/edit profile

⏳ Notification for likes/comments

⏳ Responsive/mobile-friendly polish

