import sqlite3
def Create_Database(hashedPassword: str) -> None:
    conn = sqlite3.connect("Main.db")
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_name TEXT UNIQUE NOT NULL,
                encrypted_password TEXT NOT NULL,
                date_created TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS auth (token TEXT NOT NULL)
                """)
    cur.execute("""
                INSERT INTO auth (token) VALUES (?)
                """,(hashedPassword,))
    conn.commit()
    conn.close()
def GetTokin() -> str:
    conn = sqlite3.connect("Main.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT token FROM auth")
    res = cur.fetchone()
    conn.close()
    return res[0] if res else None
def Store_Password(site_name: str,password: bytes ):
    try :
        conn = sqlite3.connect("Main.db")
        cur = conn.cursor()
        cur.execute("""
                INSERT INTO passwords (site_name,encrypted_password) VALUES (?,?)     
        """,(site_name.lower(),password))
        conn.commit()
        return 1
    except sqlite3.IntegrityError as e:
        return 0
    finally: 
        conn.close()
def Showing_Password(site_name: str):
    conn = sqlite3.connect("Main.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT encrypted_password FROM passwords WHERE LOWER(site_name) = LOWER(?)",(site_name,))
    res = cur.fetchone()
    conn.close()
    return res
def Deleting_Password(site_name):
    conn = sqlite3.connect("Main.db")
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM passwords WHERE LOWER(site_name) = LOWER(?)",(site_name,))
    if cur.rowcount == 0:
        print(f"[✕] There is no password for '{site_name}'.")
        conn.close()
        return
    conn.commit()
    print(f"[✓] Password for '{site_name}' Deleted successfully.")
    conn.close()