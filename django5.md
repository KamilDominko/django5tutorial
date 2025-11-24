# Django 5 notatki Kaila

## Komenda `startproject`

`django-admin startproject mysite djangotutorial`

Tworzy projekt django w folderze w którym wywoła się tą komende. Tworzy podstawową strukturę folderów oraz podstawowe pliki.

W wyzej przytoczonym przypadku tworzy projekt mysite w folderze djangotutorial który zostanie utworzony na ścieżce z której została wywołana komenda.

## Komenda `startapp`

`python manage.py startapp polls`

Tworzy aplikacje o nazwie polls. Fodler i podstawowe pliki.

## Komenda `runserver`

Ex: `python manage.py runserver`

UIruchamia serwer django.

## Komenda `migrate`

Przykład: `python manage.py sqlmigrate polls 0001`

Komenda ta nie uruchomi migracji na bazie danych tylko drukuje ją jako kod SQL, który jest wedłóg django wymagany.

## Komenda `check`

Przykład: `python manage.py check`

Sprawdza, czy są jakiekolwiek problemy w projekcie bez robienia migracji lub dotykania bazy danych.

## Komenda `makemigrations`

Słóży do stworzenia migracji do zmian wprowadzonych w modelach.

## Komenda `migrate`

Uruchomi migracje tylko dla aplikacji w INSTALLED_APPS.

## Trzy kroki do tworzenia zmian w modelach:

1. Zmień swoje modele w models.py

2. Uruchom `python manage.py makemigrations` aby stworzyć migracje dla tych zmian

3. Uruchom `python manage.py migrate` aby zastosować te zzmiany na bazie danych

## Komenda `shell`

Aktywuje interakktywnego shella Pythona umożliwiajac działanie na otwartym API django. W porównianiu do podstawowego pytohna ten shell automatycznie pobiera modele z INSTALLED_APPS.
