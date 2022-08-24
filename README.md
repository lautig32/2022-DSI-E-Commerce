# DSI2022-E-Commerce

# System Django 4.1 and Python 3.10

# Entorno virtual

python -m venv venv

# windows .\venv\Scripts\activate

## Instalación y configuración

1. Instalación de dependencias
```console
(venv) pip install -r requirements.txt
```

2. Aplicar las migraciones de la base de datos:
```console
(venv) python manage.py migrate
```

3. Creamos el superusuario
```console
(venv) python manage.py createsuperuser
```

## Utilidades
* Salida de paquetes instalados en formato de requisitos.
```console
(venv) pip freeze > requirements.txt
```

* [Django Admin Interface](https://pypi.org/project/django-admin-interface/) 

##### [Django](https://www.djangoproject.com/) theme (default):
```console
(venv) python manage.py loaddata admin_interface_theme_django.json
```

##### [Bootstrap](http://getbootstrap.com/) theme:
```console
(venv) python manage.py loaddata admin_interface_theme_bootstrap.json
```

##### [Foundation](http://foundation.zurb.com/) theme:
```console
(venv) python manage.py loaddata admin_interface_theme_foundation.json
```

##### [U.S. Web Design Standards](https://standards.usa.gov/) theme:
```console
(venv) python manage.py loaddata admin_interface_theme_uswds.json
```
