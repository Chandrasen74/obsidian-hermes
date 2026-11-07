import sqlite3

con = sqlite3.connect(r"C:\Users\Kanchan Verma\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies")
cur = con.cursor()
print("total rows:", cur.execute("select count(*) from cookies").fetchone()[0])
for pat in ("pinterest", "google", "accounts.google", "drive.google"):
    n = cur.execute(
        "select count(*) from cookies where host_key like ?", ("%" + pat + "%",)
    ).fetchone()[0]
    print(pat, "->", n)
rows = cur.execute(
    "select host_key, name, length(encrypted_value), is_httponly from cookies where host_key like '%pinterest%'"
).fetchall()
print("pinterest rows detail:", len(rows))
for r in rows[:20]:
    print("  ", r)
rows = cur.execute(
    "select host_key, name from cookies where host_key like '%accounts.google%' or host_key like '%drive.google%'"
).fetchall()
print("google auth rows detail:", len(rows))
for r in rows[:20]:
    print("  ", r)
