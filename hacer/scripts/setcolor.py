from hasapi import NodeConnection

with NodeConnection() as conn:
    colorInt = int(conn.params[0], 16)
    conn.setVal("color", "colorInt")

