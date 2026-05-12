#!/bin/bash

# ============================================================
#  🍷  projecte_vi — Script d'instal·lació automàtica
# ============================================================
# Aquest script configura el projecte des de zero en qualsevol
# ordinador amb Linux/macOS que tingui Python 3 i MySQL instal·lats.
# ============================================================

set -e  # Atura el script si qualsevol comanda falla

# ---------- Colors per a la terminal ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

ok()   { echo -e "${GREEN}✔ $*${NC}"; }
info() { echo -e "${CYAN}ℹ $*${NC}"; }
warn() { echo -e "${YELLOW}⚠ $*${NC}"; }
err()  { echo -e "${RED}✖ $*${NC}"; exit 1; }
step() { echo -e "\n${BOLD}${CYAN}▶ $*${NC}"; }

echo -e "${BOLD}"
echo "╔══════════════════════════════════════════════╗"
echo "║        🍷  Projecte Vi — Setup Script        ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"

# ─────────────────────────────────────────────
# PAS 1 — Comprovació de dependències del sistema
# ─────────────────────────────────────────────
step "Comprovant dependències del sistema..."

command -v python3 &>/dev/null   || err "Python 3 no trobat. Instal·la'l: sudo apt install python3 python3-venv"
command -v pip3   &>/dev/null    || err "pip3 no trobat. Instal·la'l: sudo apt install python3-pip"
command -v mysql  &>/dev/null    || err "MySQL no trobat. Instal·la'l: sudo apt install mysql-server"
command -v node   &>/dev/null    || warn "Node.js no trobat — el CSS de Tailwind no es compilarà."
command -v npm    &>/dev/null    || warn "npm no trobat — el CSS de Tailwind no es compilarà."

PYTHON=$(command -v python3)
ok "Python: $($PYTHON --version)"
ok "MySQL: $(mysql --version | head -1)"

# ─────────────────────────────────────────────
# PAS 2 — Configuració del fitxer .env
# ─────────────────────────────────────────────
step "Configurant fitxer .env..."

if [ ! -f ".env" ]; then
    info "No s'ha trobat el fitxer .env — en crearem un de nou."
fi

echo ""
echo -e "${BOLD}Introdueix les dades de connexió a MySQL:${NC}"
echo -e "(Prem ENTER per acceptar el valor per defecte entre [ ])\n"

read -rp "  Nom de la base de dades [projecte_vi]:   " DB_NAME
DB_NAME=${DB_NAME:-projecte_vi}

read -rp "  Usuari de MySQL          [projecte_user]: " DB_USER
DB_USER=${DB_USER:-projecte_user}

read -rsp "  Contrasenya de MySQL:                    " DB_PASSWORD
echo ""
[ -z "$DB_PASSWORD" ] && err "La contrasenya no pot estar buida."

read -rp "  Host                     [127.0.0.1]:    " DB_HOST
DB_HOST=${DB_HOST:-127.0.0.1}

read -rp "  Port                     [3306]:         " DB_PORT
DB_PORT=${DB_PORT:-3306}

cat > .env <<EOF
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
EOF

ok "Fitxer .env creat."

# ─────────────────────────────────────────────
# PAS 3 — Creació de la base de dades i usuari MySQL
# ─────────────────────────────────────────────
step "Configurant la base de dades MySQL..."

echo ""
warn "Necessitem credencials de ROOT de MySQL per crear la BBDD i l'usuari."
read -rsp "  Contrasenya root de MySQL: " MYSQL_ROOT_PASS
echo ""
MYSQL_ADMIN_METHOD=""

# Crear la BBDD i l'usuari si no existeixen
if mysql -u root -p"${MYSQL_ROOT_PASS}" <<SQL
CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'${DB_HOST}' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'${DB_HOST}';
FLUSH PRIVILEGES;
SQL
then
    MYSQL_ADMIN_METHOD="password"
    ok "Connexió com a root amb contrasenya correcta."
elif command -v sudo &>/dev/null; then
    warn "No s'ha pogut accedir amb root i contrasenya. Provant amb 'sudo mysql' (auth_socket)..."
    if sudo mysql <<SQL
CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${DB_USER}'@'${DB_HOST}' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'${DB_HOST}';
FLUSH PRIVILEGES;
SQL
    then
        MYSQL_ADMIN_METHOD="sudo"
        ok "Configuració de MySQL feta amb sudo mysql."
    else
        err "No s'ha pogut configurar MySQL ni amb contrasenya root ni amb sudo mysql. Revisa credencials, permisos o autenticació de root."
    fi
else
    err "No s'ha pogut accedir a MySQL com a root. Revisa la contrasenya o instal·la/configura sudo per usar auth_socket."
fi

ok "Base de dades '${DB_NAME}' i usuari '${DB_USER}' configurats."

# ─────────────────────────────────────────────
# PAS 3.5 — Càrrega de zones horàries MySQL
# ─────────────────────────────────────────────
step "Carregant zones horàries de MySQL (recomanat)..."

if command -v mysql_tzinfo_to_sql &>/dev/null; then
    if [ "${MYSQL_ADMIN_METHOD}" = "password" ]; then
        if mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p"${MYSQL_ROOT_PASS}" mysql; then
            ok "Taules de zones horàries carregades a MySQL."
            mysql -u root -p"${MYSQL_ROOT_PASS}" -e "GRANT SELECT ON mysql.time_zone TO '${DB_USER}'@'${DB_HOST}'; GRANT SELECT ON mysql.time_zone_name TO '${DB_USER}'@'${DB_HOST}'; GRANT SELECT ON mysql.time_zone_transition TO '${DB_USER}'@'${DB_HOST}'; GRANT SELECT ON mysql.time_zone_transition_type TO '${DB_USER}'@'${DB_HOST}'; FLUSH PRIVILEGES;" && \
            ok "Permisos de lectura de zones horàries concedits a '${DB_USER}'@'${DB_HOST}'." || \
            warn "No s'han pogut concedir els permisos de lectura de zones horàries."
        else
            warn "No s'han pogut carregar les zones horàries a MySQL. Si tens errors de datetimes, fes-ho manualment."
        fi
    elif [ "${MYSQL_ADMIN_METHOD}" = "sudo" ]; then
        if sudo sh -c "mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql"; then
            ok "Taules de zones horàries carregades a MySQL amb sudo."
            sudo mysql -u root -e "GRANT SELECT ON mysql.time_zone TO '${DB_USER}'@'${DB_HOST}'; GRANT SELECT ON mysql.time_zone_name TO '${DB_USER}'@'${DB_HOST}'; GRANT SELECT ON mysql.time_zone_transition TO '${DB_USER}'@'${DB_HOST}'; GRANT SELECT ON mysql.time_zone_transition_type TO '${DB_USER}'@'${DB_HOST}'; FLUSH PRIVILEGES;" && \
            ok "Permisos de lectura de zones horàries concedits a '${DB_USER}'@'${DB_HOST}'." || \
            warn "No s'han pogut concedir els permisos de lectura de zones horàries."
        else
            warn "No s'han pogut carregar les zones horàries a MySQL amb sudo."
        fi
    else
        warn "S'omet la càrrega de zones horàries perquè no s'ha detectat mètode d'administració MySQL."
    fi
else
    warn "No s'ha trobat 'mysql_tzinfo_to_sql'. S'omet la càrrega de zones horàries."
fi

# ─────────────────────────────────────────────
# PAS 4 — Entorn virtual de Python
# ─────────────────────────────────────────────
step "Creant l'entorn virtual de Python..."

if [ -d "venv" ]; then
    warn "Ja existeix el directori 'venv'. S'omitirà la creació."
else
    $PYTHON -m venv venv
    ok "Entorn virtual creat."
fi

# Activar l'entorn virtual
# shellcheck disable=SC1091
source venv/bin/activate
ok "Entorn virtual activat."

# ─────────────────────────────────────────────
# PAS 5 — Instal·lació de dependències Python
# ─────────────────────────────────────────────
step "Instal·lant dependències Python (requirements.txt)..."

# mysqlclient requereix les capçaleres de MySQL
if ! python -c "import MySQLdb" &>/dev/null; then
    info "Instal·lant paquets del sistema per mysqlclient..."
    if command -v apt &>/dev/null; then
        sudo apt-get install -y libmysqlclient-dev default-libmysqlclient-dev pkg-config python3-dev &>/dev/null || \
        warn "No s'han pogut instal·lar els paquets del sistema automàticament. Si falla, executa:\n  sudo apt install libmysqlclient-dev python3-dev"
    fi
fi

pip install --upgrade pip -q
pip install -r requirements.txt
ok "Dependències Python instal·lades."

# ─────────────────────────────────────────────
# PAS 6 — Migracions de Django
# ─────────────────────────────────────────────
step "Aplicant migracions de Django..."

python manage.py migrate
ok "Migracions completades."

# ─────────────────────────────────────────────
# PAS 7 — Carregar dades inicials (bbdd.json)
# ─────────────────────────────────────────────
step "Carregant dades inicials des de bbdd.json..."

if [ -f "bbdd.json" ]; then
    python manage.py loaddata bbdd.json
    ok "Dades carregades correctament."
else
    warn "No s'ha trobat el fitxer bbdd.json. Les dades inicials no s'han carregat."
fi

# ─────────────────────────────────────────────
# PAS 8 — Arxius estàtics
# ─────────────────────────────────────────────
step "Recopilant fitxers estàtics..."

python manage.py collectstatic --noinput 2>/dev/null || warn "collectstatic ha fallat (potser no tens STATIC_ROOT configurat — és normal en dev)."
ok "Fitxers estàtics processats."

# ─────────────────────────────────────────────
# PAS 9 — Crear superusuari (opcional)
# ─────────────────────────────────────────────
step "Configuració de superusuari Django (opcional)..."

read -rp "  Vols crear un superusuari ara? [s/N]: " CREATE_SUPERUSER
if [[ "${CREATE_SUPERUSER}" =~ ^([sS]|[sS][iI]|[yY][eE][sS]|[yY])$ ]]; then
    info "S'obrirà l'assistent de Django per crear el superusuari."
    python manage.py createsuperuser
    ok "Superusuari creat."
else
    info "S'omet la creació de superusuari."
fi

# ─────────────────────────────────────────────
# PAS 10 — Compilar CSS (Tailwind) — opcional
# ─────────────────────────────────────────────
if command -v npm &>/dev/null; then
    step "Instal·lant dependències Node.js i compilant Tailwind CSS..."
    npm install --silent
    npm run build:css
    ok "CSS compilat."
else
    warn "npm no disponible — assegura't que el fitxer static/css/output.css ja existeix."
fi

# ─────────────────────────────────────────────
# RESUM FINAL
# ─────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}╔══════════════════════════════════════════════╗"
echo "║     ✅  Instal·lació completada amb èxit!    ║"
echo "╚══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BOLD}Per iniciar el servidor de desenvolupament:${NC}"
echo -e "  ${CYAN}source venv/bin/activate${NC}"
echo -e "  ${CYAN}python manage.py runserver${NC}"
echo ""
echo -e "  ${BOLD}Usuari admin per defecte (carregat des de bbdd.json):${NC}"
echo -e "  ${YELLOW}Usuari:     admin${NC}"
echo -e "  ${YELLOW}Contrasenya: (la del fitxer bbdd.json — hash pbkdf2)${NC}"
echo -e "  ${YELLOW}→ Si has omès el pas de superusuari: python manage.py createsuperuser${NC}"
echo ""
