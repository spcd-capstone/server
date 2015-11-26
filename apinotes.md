API Spec
========

All urls shown here should be prefixed with "/api/" either by server container,
or with Flask's routing.

Note: This is a design doc to help with the development of the server, client,
and database. It is subject to change.


Nodes
-----

### Object Description

A node is represented by the following values:

```json
{
    "id": 4,
    "name": "NodeName",
    "type": "toggle",
    "ip": "192.168.1.80",
    "last_updated": "2015-11-01T23:14:00.00"
}
```

The "type" property specifies the type of node. The following types are valid:

* toggle
* light_rgb
* sensor_temp
* thermostat
* other


### API Calls

#### Reading

Need to be able to get nodes, both as a list and individually. The URLs for
retrieving node data are as follows:

    GET /nodes

retrieves list of nodes in following form:

```json
{
    "node_list":
        [
            { "id": 1, "name": "outlet1", ... },
            { "id": 2, ... },
            ...
        ]
}
```

This allows additional metadata to be delivered along with the payload, if
necessary.

To get a specific node, use the following urls:

    GET /nodes/id/<id:int>
    GET /nodes/name/<name:string>

These API calls will return the specified node data nested in a "node" value

```json
{
    "node": {"id": 1, ... }
}
```


#### Writing

The only property which can be written is the "name" property. The node being
updated must be identified with it's id:

    POST /nodes/id/<id:int>

    { "name": "newName", ... }

The server should only check for the "name" field, and then update the database
entry accordingly. All other values should be ignored.

The update should fail if a node with the "newName" already exists, or if the
ID refers to an invalid node.


Scripts
-------

Scripts to run should be located in the 'scripts' directory. The list of
available scripts is generated dynamically from the contents of the directory.
When a script is run, the name of the node (as stored in database) is passed as
the first parameter. Additional user defined parameters may be specified,
depending on the script.

When spawning a process to run the script, the ScriptingAPI expects that a
"HADB_PATH" environment variable be set containing the sqlite database path, as
well as a "HA_LOG_THREAD_ID" be set to some unique identifier. The log thread
ID will be used as an identifier in the log DB table to keep track of the
progress of the script.


### Object Description

The JSON representation for a script is shown below:

```json
{
    "id": 1,
    "name": "turnon",
}

```

The "name" field is apended with ".py" when executing the script. The "id"
can just be some sort of hash of the script name?


### API Calls

#### Reading

To get a list of the scripts on the server, use the following URL:

    GET /scripts/list

The server should return a list of scripts like this:

```json
{
    "script_list": [ { "id": 1, "name": "turnon" }, ... ]
}

```

#### Writing

To run a script, use the following URL with the params as a payload

    POST /scripts/exec/id/<id:int>
        - or -
    POST /scripts/exec/name/<name:string>

```json
    {
        "params": [ "outet1", "0" ]
    }
```

The params should be added to the script command in order.

If the script exists, and the server was able to dispatch a process, the
response should be success, regardless of the script's result.

When the server responds with a "200 OK", it will also contain the following
payload:

```json
{
    "status": "ok",
    "log_thread_id": 9181
}
```

The "log_thread_id" is a unique identifier that can be used to query the
status/result of the script execution. See Logs section for specifics.


Schedules
---------

*NOT DESIGNED YET*

### Object Description

### API Calls

#### Reading

#### Writing


Logs
----

*NOT FULLY DESIGNED YET*

### Object Description

There will be a few different log tables that are queryable. Each log table
will contain slightly different data.

A script  log entry will have the following data

```json
{
    "id": 1,
    "timestamp": "2015-11-02T23:14:00.00",
    "thread_id": 1,
    "script_name": "script",
    "params": ["outlet1", "-v"],
    "entry_type": "output",
    "data": "This is output from script running"
}
```

The "script_name" and "params" fields may only be set for the first item in the
log thread.

The valid "entry_type"s are as follows:

* "launch"
    * When a script is launched, this entry is added.
    * Only entry type where it is requried to have the "script_name" and
      "params" fields set.
    * "data" field will be blank

* "output"
    * If a script outputs anything (with log() API call), it should be stored
      as this type.
    * The output is stored in the "data" field.

* "sent_set"
    * records when set() api function is called
    * data is parameters to set() call

* "sent_get"
    * records when get() api function is called

* "result"
    * after command is executed on node, node will respond with a status code
      and payload, these are recorded here

* "exception"
    * If the script throws an exception, it should be logged here.
    * The Exception name and message will be stored in the "data" field.

* "exit_status"
    * The return status code of a script.
    * Must be included or else it is assumed that the script is still running.
    * The "data" field contains return code.


*Other log types not yet defined*


### API Calls

#### Reading

Querying a list of script log entries

    GET /logs/script/

Querying all entries with a specific thread_id

    GET /logs/script/thread_id/<thread_id:int>

Querying all entries with a specific "thread_id". useful for monitoring the
status of a specific script execution.

*optional:* Querying the script log table can be done like so:

    POST /logs/script/search

    { some query syntax here }


#### Writing

Logs cannot be written to externally.


Dashboard
---------

*NOT DESIGNED YET*


### Object Description

### API Calls

#### Reading

#### Writing


