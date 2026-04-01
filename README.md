# Projecte Vi 🍷

## Descripció

Aplicació web desenvolupada amb **Django 5.1** per gestionar i vendre vins en línia. El projecte segueix una arquitectura de 3 capes (Model–Vista–Plantilla) i s'organitza en múltiples apps Django per separar responsabilitats.

## Tecnologies

| Tecnologia | Versió / Detalls |
|---|---|
| Python | 3.x |
| Django | 5.1 |
| Base de dades | MySQL 8 (via `django.db.backends.mysql`) |
| Autenticació | Django Auth + `django-axes` (protecció brute-force) |
| CSS | Tailwind CSS (compilat via `input.css`) |
| Hosting estàtics | Django `STATICFILES_DIRS` |
| Idioma / Zona horaria | Català (`ca`) / `Europe/Madrid` |

## Estructura del projecte

```
projecte_vi/
├── core/               # Configuració principal (settings, urls, wsgi, asgi)
├── apps/
│   ├── vins/           # Gestió del catàleg de vins
│   ├── usuaris/        # Registre, login i adreça d'enviament
│   ├── comandes/       # Gestió de comandes
│   └── subscripcions/  # Subscripcions / newsletter
├── templates/          # Plantilles base i components compartits (nav, footer)
├── static/             # CSS (Tailwind), JS i imatges estàtiques
├── media/              # Imatges pujades (vins/)
└── manage.py
```

## Aplicacions

### `apps.vins` — Catàleg de vins
- **Model `Vi`**: nom, origen, tipus (Blanc · Negre · Rosat · Espumos), preu, estoc, any de collita, imatge i descripció.
- Vistes: llistat de vins disponibles (`stock > 0`).
- Imatges desades a `media/vins/`.

### `apps.usuaris` — Gestió d'usuaris
- **Registre** (`UserRegisterForm`): crea un `User` de Django amb correu com a `username`, i una `Adreça` associada (CP, població, carrer, número). Inclou validacions de format i seguretat.
- **Login** (`UserLoginForm`): autenticació per correu i contrasenya amb protecció `django-axes` (bloqueig després de 3 intents fallits, desbloqueix al cap d'1 hora).
- **Logout**: sessió tancada i redirecció a la pàgina principal.
- **Model `Adreces`**: relació `OneToOne` amb `User` (CP, població, carrer, número).

### `apps.comandes` — Comandes
- Estructura bàsica per gestionar comandes dels usuaris.

### `apps.subscripcions` — Subscripcions
- Estructura bàsica per gestionar subscripcions / newsletter.

## Arquitectura de 3 capes

```
Usuari → URL → Vista (views.py) → Model (models.py) → BD MySQL
                    ↓
              Plantilla (templates/)
```

1. **Model** — Defineix l'estructura de dades i la persistència a MySQL.
2. **Vista** — Lògica de negoci: recupera dades dels models, valida formularis i passa el context a les plantilles.
3. **Plantilla** — Renderitza la interfície; usa herència (`base.html`) i components modulars (nav, footer).

## Seguretat

- **`django-axes`**: bloqueig automàtic per `username`, `ip_address`, `user_agent`, `path_info` i `http_accept` després de 3 intents fallits.
- **CSRF**: activat per defecte en tots els formularis.
- **Contrasenyes**: amb hash via `set_password()`; validadors de Django activats (longitud, complexitat, etc.).

## Com executar el projecte

### Prerequisits
- Python 3.x
- MySQL 8 en funcionament amb la base de dades `projecte_vi` creada i l'usuari configurat.

### Configuració

1. **Crea i activa l'entorn virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Instal·la les dependències**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Aplica migracions**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Crea un superusuari** (opcional, per accedir a `/admin`):
   ```bash
   python manage.py createsuperuser
   ```

5. **Compila Tailwind CSS** (en una terminal separada):
   ```bash
   # Compilació única
   venv/bin/tailwindcss -i static/css/input.css -o static/css/output.css

   # Mode watch (recompila automàticament en cada canvi)
   venv/bin/tailwindcss -i static/css/input.css -o static/css/output.css --watch
   ```

6. **Executa el servidor**:
   ```bash
   python manage.py runserver
   ```

### URLs principals

| URL | Descripció |
|---|---|
| `/` | Pàgina principal |
| `/vins/` | Llistat de vins |
| `/usuaris/registre/` | Registre d'usuari |
| `/usuaris/login/` | Inici de sessió |
| `/usuaris/logout/` | Tancar sessió |
| `/admin/` | Panell d'administració de Django |

## Notes addicionals

- Les imatges dels vins es guarden a `media/vins/` i es serveixen via `MEDIA_URL` en mode `DEBUG`.
- Els fitxers estàtics (CSS Tailwind, JS) es troben a `static/` i estan configurats amb `STATICFILES_DIRS`.
- El correu electrònic s'utilitza com a `username` de Django internament.
- La configuració de `django-axes` utilitza múltiples paràmetres de bloqueig per màxima seguretat.
