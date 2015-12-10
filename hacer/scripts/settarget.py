from hasapi import NodeConnection

with NodeConnection() as conn:
    conn.setVal("target", conn.params[0])

