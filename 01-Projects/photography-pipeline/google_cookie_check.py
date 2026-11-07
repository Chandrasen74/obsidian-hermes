import sqlite3

con = sqlite3.connect(r"C:\Users\Kanchan Verma\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies")
cur = con.cursor()
names = ("SID", "HSID", "SSID", "APISID", "SAPISID", "__Secure-1PAPISID", "__Secure-3PAPISID", "LSID", "OSID", "__Secure-OSID", "LSOLH")
q = ("select host_key, name, expires_utc, is_persistent, source_scheme from cookies where name in "
     + "(" + ",".join("?" * len(names)) + ") order by name")
now = cur.execute("select max(expires_utc) from cookies").fetchone()[0]
rows = cur.execute(q, names).fetchall()
print("edge default: matching auth cookies:", len(rows))
import datetime
for host, name, exp, pers, sch in rows:
    # WebKit timestamps are microseconds since 1601-01-01
    exp_dt = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=exp)
    print(f"  {host:28s} {name:20s} expires {exp_dt:%Y-%m-%d %H:%M} {'EXPIRED' if exp_dt < datetime.datetime.now() else 'valid'}")
print("(now = %s)" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
