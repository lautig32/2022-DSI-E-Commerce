# DSI2022-E-Commerce

# System Django 4.1 and Python 3.10

# Usar entorno virtual necesita que le demos acceso en windows...

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Entorno virtual

python -m venv venv

# windows .\venv\Scripts\activate

# source .\venv\bin\activate

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