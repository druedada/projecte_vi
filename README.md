# Projecte Vi

## Descripció

Aquest projecte és una aplicació web desenvolupada amb Django per gestionar i mostrar vins. Inclou funcionalitats per afegir nous vins, gestionar imatges i mostrar-los a través d'una interfície web modularitzada. El projecte segueix una arquitectura de 3 capes (models, vistes, plantilles) per garantir una separació clara de responsabilitats.

## Estructura del projecte

- **core/**: Configuració principal del projecte i rutes globals.
- **vins/**: App dedicada a la gestió de vins (models, vistes, plantilles, admin).
- **media/**: Directori on es guarden les imatges pujades dels vins.
- **static/**: Recursos estàtics (CSS, JS, imatges no gestionades per models).
- **templates/**: Plantilles base i compartides.

## Arquitectura de 3 capes

### 1. Model (models.py)
- Defineix l'estructura de dades del vi (`Vi`), incloent camps com nom, tipus (enum), preu, estoc i imatge.
- Gestiona la lògica de persistència a la base de dades.
- Exemple: Quan es crea un nou vi, es fa una instància del model `Vi` i es desa a la base de dades.

### 2. Vista (views.py)
- Gestiona la lògica de negoci i la interacció entre models i plantilles.
- Exemple: La vista `home` de l'app vins recupera tots els vins disponibles (amb estoc > 0) i els passa a la plantilla per mostrar-los.
- També pot gestionar la creació d'un nou vi (formulari, validació, desar a la base de dades).

### 3. Plantilla (templates/)
- S'encarrega de la presentació i renderització de la informació.
- Exemple: La plantilla `llista_vins.html` mostra la llista de vins amb les seves dades i imatge.
- Utilitza herència de plantilles (`base.html`) i inclou components modulars (nav, footer).

## Flux de creació d'un nou vi
1. **Usuari** accedeix a un formulari per afegir un nou vi (no implementat per defecte, però es faria amb una vista basada en formularis).
2. **Vista** rep les dades del formulari, valida i crea una nova instància de `Vi`.
3. **Model** desa el nou vi a la base de dades i guarda la imatge a `media/vins/`.
4. **Vista** redirigeix o mostra un missatge de confirmació.

## Flux de visualització d'un vi
1. **Vista** recupera els vins disponibles de la base de dades (models).
2. **Vista** passa la llista de vins a la plantilla corresponent.
3. **Plantilla** renderitza la informació de cada vi (nom, tipus, preu, imatge, estoc).

## Com executar el projecte

1. **Instal·la dependències**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Aplica migracions**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Crea un superusuari (opcional)**:
   ```bash
   python manage.py createsuperuser
   ```
4. **Executa el servidor**:
   ```bash
   python manage.py runserver
   ```
5. **Accedeix a l'aplicació**:
   - Navega a `http://localhost:8000/` per veure la pàgina principal.
   - Navega a `http://localhost:800/admin`per a afegir/modificar vins.
   - Navega a `http://localhost:8000/vins/` per veure la llista de vins.

## Notes addicionals
- Les imatges dels vins es guarden a `media/vins/` i es serveixen via `MEDIA_URL` en mode DEBUG.
- L'administració de vins es fa des del panell d'admin de Django (`/admin`).
- El projecte segueix bones pràctiques de modularització i separació de responsabilitats.
