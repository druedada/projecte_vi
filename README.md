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

```text
Usuari → URL → Vista (views.py) → Model (models.py) → BD MySQL
                    ↓
              Plantilla (templates/)
```

1. **Model** — Defineix l'estructura de dades i la persistència a MySQL.
2. **Vista** — Lògica de negoci: recupera dades dels models, valida formularis i passa el context a les plantilles.
3. **Plantilla** — Renderitza la interfície i els formularis; rep les dades de la vista per mostrar-les a l'usuari final.

### Exemples del flux en el projecte

#### 1. Creació d'un usuari (Registre)
- **Plantilla**: L'usuari accedeix a `/usuaris/registre/` i veu el formulari renderitzat com a HTML per emplenar les dades (correu, contrasenya, adreça) i les envia per mètode `POST`.
- **Vista**: El controlador rep les dades (`request.POST`). Implementa la lògica de negoci: verifica que les contrasenyes coincideixen, que el correu no estigui ja en ús validant correctament el formulari corresponent.
- **Model**: Un cop les dades queden validades en la vista, s'utilitza el model `User` preexistent de Django i la classe nativa per guardar les credencials del nou usuari (tot encriptant la contrasenya). A continuació, utilitza el seu propi model `Adreces` per desar les dades de l'adreça al seu nom dins la relació establerta amb el nou usuari i les fa persistents sobre la BD MySQL.

#### 2. Crear, Modificar i Borrar un Vi (Gestió de Catàleg)
El flux és seguit des de l'app relacionada directament a la gestió pròpia.
- **Crear un vi**:
  - **Plantilla**: L'usuari (Gestor o Staff) accedeix a l'apartat de creació generant un formulari en blanc, llest per adjuntar els texts i la imatge descriptiva. 
  - **Vista**: En rebre el formulari en format de dades `POST` i a la vegada el mateix arxiu d'imatge (`request.FILES`), en valida tots els camps obligatoris i formats adients.
  - **Model**: La vista fa que s'instanciï un objecte del model `Vi` introduint els valor validats i hi executa `save()`. L'ORM finalment ho traduirà per executar la corresponent instrucció de guardat `INSERT` a MySQL i el fitxer quedarà enmagatzemat a `media/vins/`.

- **Modificar un vi**:
  - **Vista i Model**: Mitjançant la ID del vi sol·licitat, la vista inicial farà un `query`, és a dir instanciarà pel propi model en concret (com ara `Vi.objects.get(...)`) extraient un diccionari amb les dades preexistents sobre MySQL previ de cridar i visualitzar a la plantilla.
  - **Plantilla**: Això es tradueix a poder renderitzar al complet el formulari de modificació d'aquesta vista instanciada: el pinta pre-omplert (amb la instància llançada des de la vista com a variables del context des del *backend*), i a més s'hi adjunta la referència desitjada o l'arxiu d'imatge anterior adjunt en previsualització.
  - **Actualització**: El Gestor envia finalitzades totes les modificacions oportunes alterades pel POST; la **Vista** torna a recollir aquells canvis processats per assignar-los sobre el **Model** obtingut inicialment de la base de dates validant novament per acabar amb l'arxiu `save()` utilitzant així instàncies com instruccions utilitàries del model equivalent cap a `UPDATE`.

- **Borrar un vi**:
  - **Plantilla**: Fent click a qualsevol funció principal destructiva pel producte, freqüentment en lloc de realitzar la esborrada o invocar peticions sense mides oportunes es requerirà redirigir a un modal i o a un element o un apartat extra per realitzar confirmació final executant o bé un `POST`.
  - **Vista**: Rep aquesta nova sol·licitud destructiva total amb consentiment llançant l'ordre sobre que el component pertanyent en actiu executi la cerca cap la unitat en gestió particular. 
  - **Model**: Actua per part de la lògica enviada sol·licitant esborrament cridant en aquest model identificador l'assignació procedent com a eina predeterminada d'en Django l'opció funcional tal que `delete()` permetent eliminar sota una `DELETE` base total aquest model en la taula que es trobé en la base de dades esborrar per exemple fitxers inamobibles prèviament creat i el propi element instanciat.

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
