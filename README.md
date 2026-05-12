# Projecte Vi 🍷

[![Python 3.x](https://img.shields.io/badge/Python-3.x-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![Django 5.1](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MySQL 8](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-Visualizations-FF6384?logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-ES6+-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![npm](https://img.shields.io/badge/npm-Package%20Manager-CB3837?logo=npm&logoColor=white)](https://www.npmjs.com/)

## Descripció

Aplicació web desenvolupada amb **Django 5.1** per gestionar i vendre vins en línia. El projecte segueix una arquitectura de 3 capes (Model–Vista–Plantilla) i s'organitza en múltiples apps Django per separar responsabilitats.



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

### Configuració rápida (recomanat) ⚡

La manera més ràpida és usar l'script d'instal·lació automàtica:

```bash
cd ./projecte_vi
chmod +x setup.sh
./setup.sh
```

L'script farà automàticament:
- Comprovació de dependències del sistema
- Configuració interactiva del `.env`
- Creació de la base de dades MySQL i usuari
- Càrrega de zones horàries MySQL
- Creació de l'entorn virtual Python
- Instal·lació de dependències Python
- Aplicació de migracions
- Càrrega de dades inicials (`bbdd.json`)
- Opció d'crear superusuari
- Compilació de Tailwind CSS

Una vegada completat:
```bash
source venv/bin/activate
python manage.py runserver
```

---

### Configuració manual

Si prefereixes fer-ho pas a pas, segueix aquests passos:

#### 1. **Instal·la les dependències del sistema**
```bash
sudo apt update
sudo apt install -y python3 python3-venv nodejs npm mysql-server
```

#### 2. **Configura MySQL i crea la base de dades**
```bash
# Accedeix a MySQL com a root
sudo mysql -u root

# Dins de MySQL, executa (substitueix contrasenya_a_escollir per una contrasenya forta):
```sql
CREATE DATABASE projecte_vi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'projecte_user'@'localhost' IDENTIFIED BY 'contrasenya_a_escollir';
GRANT ALL PRIVILEGES ON projecte_vi.* TO 'projecte_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```
```

#### 3. **Carrega les zones horàries a MySQL**
```bash
# Com a root, carrega les zones horàries del sistema en la BD mysql
sudo mysql_tzinfo_to_sql /usr/share/zoneinfo | sudo mysql -u root mysql

# Otorga permisos de lectura a l'usuari de la BD
sudo mysql -u root -e "GRANT SELECT ON mysql.time_zone TO 'projecte_user'@'localhost'; \
  GRANT SELECT ON mysql.time_zone_name TO 'projecte_user'@'localhost'; \
  GRANT SELECT ON mysql.time_zone_transition TO 'projecte_user'@'localhost'; \
  GRANT SELECT ON mysql.time_zone_transition_type TO 'projecte_user'@'localhost';"
```

#### 4. **Crea i activa l'entorn virtual**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 5. **Crea el fitxer `.env`**
A l'arrel del projecte, crea un fitxer `.env` amb aquest contingut (adaptant la contrasenya):
```
DB_NAME=projecte_vi
DB_USER=projecte_user
DB_PASSWORD=contrasenya_a_escollir
DB_HOST=127.0.0.1
DB_PORT=3306
```

#### 6. **Instal·la les dependències del sistema per mysqlclient**
```bash
sudo apt update
sudo apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config
```

#### 7. **Instal·la les dependències de Python**
```bash
pip install -r requirements.txt
```

#### 8. **Aplica les migracions**
```bash
python manage.py migrate
```

#### 9. **Carrega les dades inicials**
```bash
python manage.py loaddata bbdd.json
```

#### 10. **Crea un superusuari** (opcional, per accedir a `/admin`)
```bash
python manage.py createsuperuser
```

#### 11. **Compila Tailwind CSS** (en una terminal separada)
```bash
npm install

# Compilació única
npm run build:css

# O mode watch (recompila automàticament en cada canvi)
npm run watch:css
```

#### 12. **Executa el servidor**
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
