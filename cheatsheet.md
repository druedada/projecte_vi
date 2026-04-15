# 📋 CHEATSHEET DJANGO 

## 🐍 Entorn virtual
```bash
# Crear carpeta del projecte
mkdir mi_proyecto
cd mi_proyecto

# Crear entorn virtual
python3 -m venv venv

# Activar
source venv/bin/activate

# Desactivar
deactivate
```

## 📦 Instalar Django
```bash
pip install django
pip freeze > requirements.txt
```

## 🚀 Crear projecte i app
```bash
# Crear projecte Django
django-admin startproject config .

# Crear una app
python manage.py startapp core
```

## ⚙️ Servidor i migracions
```bash
# Arrancar servidor
python manage.py runserver

# Altres ports
python manage.py runserver 8001

# Migracions
python manage.py makemigrations
python manage.py makemigrations core
python manage.py migrate

# Veure estat
python manage.py showmigrations
```

## 👑 Superusuari
```bash
python manage.py createsuperuser
```

## 📊 Fixtures JSON
```bash
# Carregar dades JSON
python manage.py loaddata bbdd.json
python manage.py loaddata bd
```

## 🛠️ Base de dades
```bash
# Shell Django
python manage.py shell

# SQL d'una migració
python manage.py sqlmigrate core 0001
```

## 🔐 Usuari i auth
```bash
# Canviar contrasenya
python manage.py changepassword nom_usuari
```

## 📁 Arxius estàtics
```bash
python manage.py collectstatic
```

## 🧪 Tests
```bash
python manage.py test
python manage.py test core
```

## 🔒 django-axes (bloquejos)
```bash
# Reset global
python manage.py axes_reset

# Per IP
python manage.py axes_reset_ip 127.0.0.1

# Per usuari
python manage.py axes_reset_username meu_usuari

# IP + usuari
python manage.py axes_reset_ip_username 127.0.0.1 meu_usuari
```

## 🔄 Flux diari
```bash
cd mi_proyecto
source venv/bin/activate
python manage.py runserver
```

## 📈 Si canvies models
```bash
python manage.py makemigrations
python manage.py migrate
```

## 👨‍💻 Si et bloqueja axes
```bash
python manage.py axes_reset_username meu_usuari
```

## 📋 Extra útil
```bash
# Des de requirements
pip install -r requirements.txt

# Veure paquets
pip freeze
```

---

