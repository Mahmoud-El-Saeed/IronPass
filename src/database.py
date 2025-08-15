import sqlite3

def Create_Database(hashedPassword: str) -> None:
    conn = sqlite3.connect(".Main.db")
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                date_created TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(site_name, username)
                )
                """)
    cur.execute("CREATE TABLE IF NOT EXISTS auth (token TEXT NOT NULL)")

    cur.execute("SELECT token FROM auth")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO auth (token) VALUES (?)", (hashedPassword,))

    conn.commit()
    conn.close()

def GetTokin() -> str:
    conn = sqlite3.connect(".Main.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT token FROM auth")
    res = cur.fetchone()
    conn.close()
    return res[0] if res else None


def Store_Password(site_name: str, username: str, password: bytes) -> bool:
    try:
        conn = sqlite3.connect(".Main.db")
        cur = conn.cursor()
        cur.execute("""
                INSERT INTO passwords (site_name, username, encrypted_password) VALUES (?,?,?)     
        """, (site_name.lower(), username.lower(), password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally: 
        conn.close()

def Showing_Password(site_name: str, username: str): 
    conn = sqlite3.connect(".Main.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT encrypted_password FROM passwords WHERE LOWER(site_name) = LOWER(?) AND LOWER(username) = LOWER(?)",
        (site_name, username)
    )
    res = cur.fetchone()
    conn.close()
    return res

def Deleting_Password(site_name: str, username: str) -> bool: 
    try:
        conn = sqlite3.connect(".Main.db")
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM passwords WHERE LOWER(site_name) = LOWER(?) AND LOWER(username) = LOWER(?)",
            (site_name, username)
        )
        conn.commit()
        return cur.rowcount > 0
    except:
        return False
    finally:
        conn.close()    
    
def GetAllPasswords():
    conn = sqlite3.connect(".Main.db")
    cur = conn.cursor()
    cur.execute("SELECT  site_name, username, encrypted_password FROM passwords")
    results = cur.fetchall()
    conn.close()
    return results