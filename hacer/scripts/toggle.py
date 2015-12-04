from hasapi import NodeConnection

with NodeConnection() as conn:
    conn.setVal("on", conn.params[0])

