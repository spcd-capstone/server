from hasapi import NodeConnection

with NodeConnection() as conn:
    conn.log("from script")

