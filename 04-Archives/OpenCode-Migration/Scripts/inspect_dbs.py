import sqlite3, os

LOCALAPPDATA = os.environ.get("LOCALAPPDATA", "")
DBS = [
    ("state.db", os.path.join(LOCALAPPDATA, "hermes", "state.db")),
    ("projects.db", os.path.join(LOCALAPPDATA, "hermes", "projects.db")),
    ("shared-state.db", os.path.join(LOCALAPPDATA, "hermes", "shared-state.db")),
]

for label, path in DBS:
    print("=== " + label)
    if not os.path.exists(path):
        print("  missing")
        continue
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        tables = [r[0] for r in con.execute(
            "select name from sqlite_master where type='table' order by name").fetchall()]
        print("  tables:", tables)
        for t in tables:
            try:
                cnt = con.execute(f"select count(*) from [{t}]").fetchone()[0]
                print(f"    {t}: {cnt} rows")
                cols = [c[1] for c in con.execute(f"pragma table_info([{t}])").fetchall()]
                print(f"      cols: {cols}")
            except Exception as e:
                print(f"    {t}: ERR {e}")
    finally:
        con.close()
