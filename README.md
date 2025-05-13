# IronPass - Password Manager

**IronPass** is a secure and user-friendly password management system designed to help you store and manage your passwords safely. It uses strong encryption to protect your data and provides a simple command-line interface (CLI) for ease of use.

---

## Features

- **Master Password Protection**  
  Access to all passwords is secured by a master password.

- **Password Generation**  
  Automatically generates strong, random passwords.

- **Password Storage**  
  Saves passwords for different sites or services.

- **Password Retrieval**  
  Easily retrieve stored passwords.

- **Password Deletion**  
  Remove passwords when no longer needed.

- **Encryption**  
  Uses `argon2` for key derivation and `Fernet` (from the `cryptography` library) for encryption to ensure security.

---

## Requirements

To run IronPass, the following Python libraries are required:

- `argon2-cffi`
- `cryptography`
- `getpass` (built-in)
- `sqlite3` (built-in)
- `secrets` (built-in)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/IronPass.git
   cd IronPass
   ```

2. **Install the required libraries:**

   ```bash
   pip install argon2-cffi cryptography
   ```

---

## Usage

### Run the Program

```bash
python main.py
```

### First-time Setup

You will be prompted to create a **master password**. This password will be used to access all your stored credentials.

### Main Menu

1. **Generate new password**  
   Create a new, secure password for a site.

2. **Retrieve password**  
   View a stored password.

3. **Delete password**  
   Remove a stored password.

4. **Add password**  
   Manually add a password for a site.

5. **Exit**  
   Close the program.

---

## Security Notes

- **Master Password:**  
  Keep your master password secure. If it is lost, access to your stored passwords will be permanently lost.

- **Encryption:**  
  All passwords are encrypted using a key derived from your master password. This encryption key is never stored.

- **Database:**  
  The password database (`Main.db`) is stored locally. It is recommended to back it up securely to prevent data loss.

---