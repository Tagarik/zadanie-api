import flask, json, os, uuid, datetime

app = flask.Flask(__name__)

class ApiError(Exception):
    # Obsluga bledow API
    def __init__(self, message, status_code=500, payload=None):
        self.message = message
        self.status_code = status_code
        self.payload = payload
        super().__init__(self.message)

@app.errorhandler(ApiError)
def handle_api_error(error):
    response = {
        "status": "error",
        "message": error.message
    }
    if error.payload:
        response["details"] = error.payload
    return flask.jsonify(response), error.status_code

USERS_FILE = "users.json"

# Ladowanie uzytkownikow
def load_users():
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        return []
    
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


# Zapis uzytkownikow
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


# Rejestracja uzytkownika
@app.route('/register', methods=['POST'])
def register():

    data = flask.request.get_json() 

    # walidacja danych
    if not data:
        raise ApiError("Brak danych", status_code=400)
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        raise ApiError("Brak emaila lub hasla", status_code=400)

    # test czy uzytkownik juz istnieje
    users = load_users()
    if any(user['email'] == email for user in users):
        raise ApiError("Uzytkownik o tym emailu juz istnieje", status_code=400)

    # dodanie nowego uzytkownika
    new_user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password": password, # oczywiscie haslo powinno byc zahashowane
        "created_at": datetime.datetime.now().isoformat()
    }
    users.append(new_user)
    save_users(users)
    user_data = {k: v for k, v in new_user.items() if k != 'password'}
    resp_message = {
        "status": "success",
        "message": "Uzytkownik zarejestrowany pomyslnie",
        'user': user_data
    }
    return flask.jsonify(resp_message), 201



# Pobieranie wszystkich uzytkownikow
@app.route('/users', methods=['GET'])
def get_users():

    users = load_users()
    users_no_pass = []

    # tworzenie listy uzytkownikow bez hasel
    for user in users:
        user_no_pass = {k: v for k, v in user.items() if k != 'password'}
        users_no_pass.append(user_no_pass)

    resp_message = {
        "status": "success",
        "users": users_no_pass
    }
    return flask.jsonify(resp_message), 200



# Pobieranie danych uzytkownika po ID
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):

    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)

    if not user:
        raise ApiError("Nie znaleziono uzytkownika", status_code=404)

    user_data = {k: v for k, v in user.items() if k != 'password'}
    resp_message = {"status": "success",
                    'user': user_data}
    return flask.jsonify(resp_message), 200



# Aktualizacja hasla uzytkownika
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):

    data = flask.request.get_json()
    if not data:
        raise ApiError("Brak danych", status_code=400)

    old_password = data.get('old_password')
    # Sprawdzenie czy stare haslo zostalo podane
    if not old_password:
        raise ApiError("Prosze podac stare haslo", status_code=400)

    new_password = data.get('new_password')
    # Sprawdzenie czy haslo zostalo podane
    if not new_password:
        raise ApiError("Prosze podac nowe haslo", status_code=400)

    users = load_users()
    user_index = next((i for i, u in enumerate(users) if u['id'] == user_id), None)
    if user_index is None:
        raise ApiError("Nie znaleziono uzytkownika", status_code=404)

    # Weryfikacja starego hasla
    if users[user_index]['password'] != old_password:
        raise ApiError("Niepoprawne haslo", status_code=401)

    users[user_index]['password'] = new_password

    save_users(users)
    user_data = {k: v for k, v in users[user_index].items() if k != 'password'}
    resp_message = {
        "status": "success",
        "message": "Haslo zmienione pomyslnie",
        'user': user_data
    }
    return flask.jsonify(resp_message), 200



# Usuwanie uzytkownika
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):

    data = flask.request.get_json()
        
    # Sprawdzenie czy podano dane
    if not data or not data.get('password'):
        flask.abort(400, description="Wymagane podanie hasla")
        
    password = data.get('password')
    users = load_users()
        
    # Wyszukanie uzytkownika
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        raise ApiError("Nie znaleziono uzytkownika", status_code=404)
        
    # Sprawdzenie hasla
    if user['password'] != password:
        raise ApiError("Niepoprawne haslo", status_code=401)
        
    # Usuniecie uzytkownika
    users = [u for u in users if u['id'] != user_id]
    save_users(users)
        
    resp_message = {
        "status": "success",
        "message": "Uzytkownik usuniety pomyslnie"
    }
    return flask.jsonify(resp_message), 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)