import datetime
import sqlite3

con = sqlite3.connect(r"C:\Users\Kanchan Verma\AppData\Local\Google\Chrome\User Data\Profile 14\Network\Cookies")
cur = con.cursor()
print("total rows:", cur.execute("select count(*) from cookies").fetchone()[0])
for pat in ("pinterest", "google"):
    n = cur.execute("select count(*) from cookies where host_key like ?", ("%" + pat + "%",)).fetchone()[0]
    print(pat, "->", n)
names = ("SID", "HSID", "SSID", "APISID", "SAPISID", "__Secure-1PAPISID", "__Secure-3PAPISID", "_pinterest_sess", "_auth")
q = ("select host_key, name, expires_utc from cookies where name in "
     + "(" + ",".join("?" * len(names)) + ")")
rows = cur.execute(q, names).fetchall()
now = datetime.datetime.now()
print("auth cookie rows:", len(rows))
for host, name, exp in rows:
    exp_dt = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=exp)
    print(f"  {host:24s} {name:18s} {exp_dt:%Y-%m-%d} {'EXPIRED' if exp_dt < now else 'valid'}")
