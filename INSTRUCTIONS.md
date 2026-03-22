# Directrices de Desarrollo - Proyecto Productor de Vi

## 1. Framework y Stack Tecnológico

### Backend
- **Framework**: Django 5.x utilizando el patrón **MVT** (Model-View-Template)
- **Base de Datos**: MySQL 8.0
- **ORM**: Django ORM (nunca SQL puro)
- **Versión Python**: 3.10+
- **Entorno Virtual**: venv (ubicado en `/venv/bin/activate`)

### Frontend
- **HTML**: HTML5 semántico y accesible
- **CSS**: Tailwind CSS 3.4
- **Accesibilidad**: WCAG 2.1 Nivel AA (mínimo)
- **JavaScript**: Vanilla JS o mínimo necesario de librerías

## 2. Patrones de Arquitectura

### MVT (Model-View-Template)
- **Models** (`vins/models.py`): Definir entidades de negocio usando Django ORM
- **Views** (`vins/views.py`): Lógica de negocio y control de flujo
- **Templates** (`templates/`): Presentación HTML, reutilizando `base.html`

### POO (Programación Orientada a Objetos)
- Usar clases para encapsular comportamiento relacionado
- Respetar principios SOLID
- Evitar código procedural innecesario

### DAO (Data Access Object)
- Crear una capa DAO para abstraer acceso a datos
- Separar consultas complejas en métodos reutilizables
- Ubicación: `vins/dao.py` (crear si no existe)
- Ejemplo:
  ```python
  class VinDAO:
      @staticmethod
      def get_all_vins():
          return Vin.objects.all()
      
      @staticmethod
      def get_vin_by_id(vin_id):
          return Vin.objects.get(id=vin_id)
  ```

### Factory Pattern
- Usar factories para crear objetos complejos o con lógica de inicialización
- Ubicación: `vins/factories.py`
- Ejemplo:
  ```python
  class VinFactory:
      @staticmethod
      def create_vin_from_form(form_data):
          return Vin(**form_data)
  ```

## 3. Estructura de Carpetas

```
projecte_vi/
├── manage.py
├── INSTRUCTIONS.md          # Este archivo
├── core/                    # Configuración de Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── vins/                    # App principal
│   ├── models.py           # Modelos Django
│   ├── views.py            # Vistas
│   ├── urls.py             # URLs de la app
│   ├── dao.py              # Capa de acceso a datos
│   ├── factories.py        # Factories para creación de objetos
│   ├── forms.py            # Formularios Django (crear si no existe)
│   ├── admin.py            # Admin de Django
│   └── migrations/         # Migraciones de BD
├── templates/              # Templates HTML
│   ├── base.html           # Template base
│   ├── home.html
│   └── includes/           # Components reutilizables
│       ├── nav.html
│       └── footer.html
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── media/                  # Archivos subidos por usuarios
└── venv/                   # Entorno virtual
```

## 4. Seguridad

### Autenticación
- Usar sistema nativo de Django: `django.contrib.auth`
- Decoradores: `@login_required` para proteger vistas
- Template tag: `{% if user.is_authenticated %}` en templates

### Protección de Datos
- Usar Django ORM para evitar SQL injections
- Habilitar CSRF tokens en formularios: `{% csrf_token %}`
- Validar input en forms de Django
- Never trust user input

### HTTPS
- En producción, forzar HTTPS con `SECURE_SSL_REDIRECT = True`

## 5. Gestión del Carrito de Compras

### Arquitectura: Cliente (localStorage)
- **Ubicación**: `static/js/cart.js`
- **Almacenamiento**: localStorage del navegador
- **Objetivo**: Minimizar peticiones a BBD antes del checkout
- **Datos almacenados**: Array de objetos con `{ vin_id, cantidad, precio }`

### Flujo
1. Usuario agrega vino al carrito → se guarda en localStorage
2. Carrito visible en cliente sin peticiones backend
3. Solo en checkout → POST al servidor para validar y crear orden
4. Backend valida inventario, precios, etc. antes de procesar

### Implementación
```javascript
// cart.js ejemplo
class Cart {
    static addToCart(vinId, cantidad) {
        let cart = this.getCart();
        const item = cart.find(i => i.vin_id === vinId);
        if (item) {
            item.cantidad += cantidad;
        } else {
            cart.push({ vin_id: vinId, cantidad });
        }
        this.saveCart(cart);
    }

    static getCart() {
        return JSON.parse(localStorage.getItem('cart')) || [];
    }

    static saveCart(cart) {
        localStorage.setItem('cart', JSON.stringify(cart));
    }
}
```

## 6. Convenciones de Código

### Naming
- Variables/funciones: `snake_case`
- Clases: `PascalCase`
- Constantes: `UPPER_SNAKE_CASE`
- Templates: `kebab-case-name.html`

### Django Models
```python
class Vin(models.Model):
    nom = models.CharField(max_length=200)
    descripcio = models.TextField()
    prec = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Vins"

    def __str__(self):
        return self.nom
```

### Views
- Usar Class-Based Views (CBV) cuando sea posible
- Mantener lógica clara y separada
- Usar DAO para acceso a datos

### Templates
- Usar `{% extends "base.html" %}` en todos los templates
- Usar template tags de Django: `{% if %}`, `{% for %}`, `{% url %}`
- Priorizar legibilidad: indentación coherente
- Incluir componentes con `{% include %}`

## 7. Frontend - Accesibilidad WCAG 2.1 AA

### Checklist
- [ ] Todos los `<img>` tienen atributos `alt` descriptivos
- [ ] Colores con ratio de contraste mínimo 4.5:1 (texto)
- [ ] Formularios con `<label>` asociadas a inputs
- [ ] Navegación por teclado funcional en todo el sitio
- [ ] ARIA labels donde sea necesario
- [ ] Headings (`<h1>`, `<h2>`, etc.) en orden jerárquico
- [ ] Mensajes de error claros y vinculados a inputs

### Tailwind CSS
- Usar utilities de Tailwind para responsive design
- Breakpoints: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`
- No escribir CSS custom a menos que sea imprescindible

## 8. Base de Datos - MySQL 8.0

### Convenciones
- Nombres de tablas: `plural` en inglés (según Django)
- Campos en Catalan cuando sea lógico (nom, descripcio, etc.)
- Usar tipos apropiados: VARCHAR para strings cortos, TEXT para largos, DECIMAL para dinero
- Siempre incluir timestamps: `created_at`, `updated_at`

### Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## 9. Workflow de Desarrollo

### Iniciar sesión de trabajo
```bash
source venv/bin/activate
python manage.py runserver
```

### Realizar cambios en modelo
```bash
python manage.py makemigrations
python manage.py migrate
```

### Testing
```bash
python manage.py test vins
```

### Verificación
```bash
python manage.py check
```

## 10. Notas Importantes

- **No cambiar el patrón MVT**: Cualquier extensión debe integrarse respetando esta arquitectura
- **DAO y Factory son opcionales en consultas simples**, pero obligatorios en lógica compleja
- **Siempre usar formatos Catalan/Español en la interfaz** pero mantener lógica en inglés en backend
- **Seguridad primero**: Revisar permisos en cada view antes de pasar a producción
- **Comentar lógica compleja**: Especialmente en DAO y Factories

---

*Última actualización: 21 de marzo de 2026*
