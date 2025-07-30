KNI 2024/2025 

# Dokumentacja projetu: zgubionypupil.pl

## Opis projektu
Zgubionypupil.pl będzie platformą internetową stworzoną w Django, która umożliwi użytkownikom zgłaszanie oraz wyszukiwanie zagubionych psów. Głównym celem projektu będzie pomoc w odnalezieniu zwierząt poprzez umożliwienie dodawania zgłoszeń zawierających zdjęcie psa, opis oraz miejsce, w którym zwierzę zostanie zauważone.

![Screenshot 1](https://github.com/UR-INF/pwjp-ontn/blob/f5809a289b5fa50b79a5c0e8a80cb70a387fcf79/docs/screen1.png)
![Screenshot 2](https://github.com/UR-INF/pwjp-ontn/blob/f5809a289b5fa50b79a5c0e8a80cb70a387fcf79/docs/screen2.png)

## Instrukcja uruchomienia aplikacji

Nalezy mieć zainstalowane środowisko Docker.
Nastepne nalezy wpisac komendy:
```
docker-compose build
docker-compose run web sh -c "python manage.py migrate"
docker-compose run web sh -c "python manage.py seed_cities"
docker-compose up
```

## Zakres projektu i opis funkcjonalności:
- Dodawanie zgłoszeń – użytkownicy będą mogli dodawać posty ze zdjęciem, opisem psa oraz lokalizacją, gdzie go zauważono.
- Mapa zgłoszeń – zostanie wdrożona interaktywna mapa, na której będą oznaczane zgłoszenia zagubionych psów.
- Wyszukiwanie i filtrowanie – będzie możliwość przeszukiwania zgłoszeń według daty, lokalizacji, rasy czy innych parametrów.
- Rejestracja i logowanie – użytkownicy będą mogli tworzyć konta, aby zarządzać swoimi zgłoszeniami oraz śledzić posty.
- Powiadomienia e-mail – zostaną zaimplementowane automatyczne powiadomienia dla użytkowników w przypadku nowych zgłoszeń w ich okolicy.
- Komentarze i aktualizacje – użytkownicy będą mogli dodawać komentarze i oznaczać odnalezione zwierzęta.


## Panele / zakładki aplikacji 
- Panel logowania / rejestracji – umożliwi tworzenie konta i zarządzanie danymi.
- Strona główna – będzie zawierać listę najnowszych zgłoszeń oraz mapę.
- Dodawanie zgłoszenia – zostanie stworzony formularz do wprowadzania informacji o zagubionym psie.
- Lista zgłoszeń – będzie można przeglądać i filtrować dostępne zgłoszenia.
- Profil użytkownika – umożliwi zarządzanie kontem i przeglądanie historii zgłoszeń.

## Baza danych
###### Diagram ERD

![ERD of database](https://github.com/UR-INF/pwjp-ontn/blob/576ab298dd50cc0117209e92a920568223bc3412/docs/dbERD.png)

## Wykorzystane biblioteki:
- asgiref           3.8.1
- attrs             25.3.0
- autobahn          24.4.2
- Automat           25.4.16
- cffi              1.17.1
- channels          4.2.2
- channels_redis    4.2.1
- constantly        23.10.4
- cryptography      44.0.3
- daphne            4.1.2
- Django            5.2
- hyperlink         21.0.0
- idna              3.10
- incremental       24.7.2
- msgpack           1.1.0
- pillow            11.1.0
- pip               25.1.1
- psycopg2-binary   2.9.10
- pyasn1            0.6.1
- pyasn1_modules    0.4.2
- pycparser         2.22
- pyOpenSSL         25.0.0
- redis             6.0.0
- service-identity  24.2.0
- setuptools        80.3.1
- sqlparse          0.5.3
- Twisted           24.11.0
- txaio             23.1.1
- typing_extensions 4.13.1
- whitenoise        6.9.0
- zope.interface    7.2


