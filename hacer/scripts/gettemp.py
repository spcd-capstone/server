from hasapi import NodeConnection

with NodeConnection() as conn:
    temp = conn.getVal("temperature")
    conn.log(temp)
    print(temp)

