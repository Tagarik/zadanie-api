import requests as re, pprint

def load_users():
    try:
        resp = re.get('http://localhost:8080/users')
        pprint.pprint(resp.json())
    except Exception as e:
        pprint.pprint(e)
    
def register(email, password):
    try:
        data = {"email": email, "password": password}
        resp = re.post('http://localhost:8080/register', json=data)
        pprint.pprint(resp.json())
    except Exception as e:
        pprint.pprint(e)
    
def load_user(user_id):
    try:
        resp = re.get(f'http://localhost:8080/users/{user_id}')
        pprint.pprint(resp.json())
    except Exception as e:
        pprint.pprint(e)
    
def update_password(user_id, old_password, new_password):
    try:
        data = {"old_password": old_password,
                "new_password": new_password}
        resp = re.put(f'http://localhost:8080/users/{user_id}', json=data)
        pprint.pprint(resp.json())
    except Exception as e:
        pprint.pprint(e)
    
def delete_user(user_id, password):
    try:
        data = {"password": password}
        resp = re.delete(f'http://localhost:8080/users/{user_id}', json=data)
        pprint.pprint(resp.json())
    except Exception as e:
        pprint.pprint(e)
        

def menu():
    print("1. Uzytkownicy")
    print("2. Zarejestruj")
    print("3. Zaladuj dane uzytkownika")
    print("4. Zmien haslo")
    print("5. Usun konto")
    choice = input("Wybierz opcje: ")
    if choice == '1':
        load_users()
    elif choice == '2':
        email = input("Podaj email: ")
        password = input("Podaj haslo: ")
        register(email, password)
    elif choice == '3':
        user_id = input("Podaj ID uzytkownika: ")
        load_user(user_id)
    elif choice == '4':
        user_id = input("Podaj ID uzytkownika: ")
        old_password = input("Podaj stare haslo: ")
        new_password = input("Podaj nowe haslo: ")
        update_password(user_id, old_password, new_password)
    elif choice == '5':
        user_id = input("Podaj ID uzytkownika: ")
        password = input("Podaj haslo: ")
        delete_user(user_id, password)
    else:
        print("Niepoprawny wybor")


if __name__ == '__main__':
    menu()