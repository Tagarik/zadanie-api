# Flask API Demo - System zarządzania użytkownikami
Przykładowy projekt demonstracyjny mający na celu przedstawienie prostego serwera API (REST) stworzonego w Pythonie przy użyciu frameworka Flask. Aplikacja pozwala na zarządzanie użytkownikami poprzez operacje CRUD.

> [!CAUTION]
> Uwaga: Ten projekt jest demonstracją i nie powinien być używany w środowisku produkcyjnym

## Funkcje
- Rejestracja nowego użytkownika
- Pobieranie listy wszystkich użytkowników
- Pobieranie szczegółowych danych pojedynczego użytkownika
- Aktualizacja hasła użytkownika
- Usuwanie konta użytkownika

## Struktura projektu
`server.py` - serwer API z endpointami i backendem
`client.py` - klient konsolowy do testowania API
`users.json` - plik do przechowywania danych o użytkownikach

## Instalacja
> [!NOTE]
> Wymagania:
> - Python 3.7+
> - pip (menedżer pakietów)

**Konfiguracja środowiska wirtualnego**

1. Sklonuj lub pobierz repozytorium
2. Otwórz terminal/wiersz poleceń i wybierz mejsce docelowe projektu
```
cd C://{lokalizacja projektu}
```
3. Stwórz wirtualne środowisko
```
python -m venv env
```
4. Aktywuj wirtualne środowisko
```
env\Scripts\activate
```
5. Zainstaluj wymagane biblioteki
```
pip install -r requirements.txt
<LUB>
py -m pip install -r requirements.txt
```

## Uruchomienie aplikacji
**Serwer**
```
py server.py
```

**Klient**
```
py client.py
```
Po uruchomieniu klienta pojawi się menu z opcjami:

Wyświetlenie listy użytkowników
Rejestracja nowego użytkownika
Pobranie danych pojedynczego użytkownika
Zmiana hasła
Usunięcie konta
## Endpointy API 
|Metoda|Endpoint|Opis|
|---|---|---|
|POST|/register|Rejestracja nowego użytkownika|
|GET|/users|Pobieranie listy wszystkich użytkowników|
|GET|/users/{user_id}|Pobieranie danych pojedynczego użytkownika|
|PUT|/users/{user_id}|Aktualizacja hasła użytkownika|
|DELETE|/users/{user_id}|Usunięcie konta użytkownika|

## Obsługa błędów
API zawiera obsługę błędów z wykorzystaniem niestandardowej klasy ApiError, która zwraca odpowiedzi w formacie JSON:

- Kod statusu HTTP
- Komunikat błędu
- Opcjonalnie dodatkowe szczegóły

## Rozwój projektu
Możliwe poszerzenie projektu o:
- hashowanie haseł
- uwierzytelnianie JWT
- utworzenie bazy danych (SQL lub noSQL)