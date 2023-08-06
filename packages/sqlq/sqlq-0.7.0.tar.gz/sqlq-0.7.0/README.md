# Sqlite3 Execution Queue

<badges>[![version](https://img.shields.io/pypi/v/sqlq.svg)](https://pypi.org/project/sqlq/)
[![license](https://img.shields.io/pypi/l/sqlq.svg)](https://pypi.org/project/sqlq/)
[![pyversions](https://img.shields.io/pypi/pyversions/sqlq.svg)](https://pypi.org/project/sqlq/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>A thread safe queue worker that executes SQL for multi-threaded applications.</i>

# Hierarchy

```
sqlqueue
'---- SqlQueue()
    |---- sql()
    |---- _sql()
    |---- commit()
    '---- stop()
```

# Example

## python
```python
from sqlq import *

# specify the db file, relative or absolute path
# set server=True
sqlqueue = SqlQueue(server=True, db="db.db")

# SQL execution modes
# all will return the executed SQL result immediately
SqlQueue(server=True, db="default", timeout_commit=1000).sql("SELECT * FROM table;")
SqlQueue(server=True, db="commit per 1ms", timeout_commit=1).sql("INSERT INTO table VALUES (?);", (0,))
SqlQueue(server=True, db=r"C:\somewhere\db.db").sql("INSERT INTO table VALUES (?);", ((0,),(0,)))
SqlQueue(server=True, db="../../data/db.db").sql('''
CREATE TABLE "tablea" ("a" TEXT);
DELETE TABLE "table";
''')

# stop the worker
# use it at your own risk
# otherwise data will be lost
# always commit before stopping it
sqlqueue.commit()
sqlqueue.stop()

# using sqlq with encryptedsocket
# server
from encryptedsocket import SS
from easyrsa import *
sqlqueueserver = SqlQueue(server=True, db=r"db.db")
threading.Thread(target=SS(EasyRSA(bits=1024).gen_key_pair(), sqlqueueserver.functions).start).start()
# client
sqlqueue = SqlQueue()
for i in range(10):
    # SqlQueue._sql() must not be used in socket mode
    sqlqueue.sql("INSERT INTO test VALUES (?);", (str(i)))
# server
sqlqueueserver.commit()
sqlqueueserver.stop()

# SQL execution speed
# # server mode _sql() without built-in ThreadWrapper() handler
# SqlQueue(server=True, ...)._sql() <
# # server mode sql() with built-in ThreadWrapper() handler
# SqlQueue(server=True, ...).sql() <
# # client mode sql() with two nested ThreadWrapper() handlers
# SqlQueue().sql()

# this example shows how sqlq is used
# SQL should not be executed frequently
r = (1, 5, 10, 50, 100, 200)
r = (50,)
for l in r:
    tw = ThreadWrapper(threading.Semaphore(l))
    starttime = time.time()
    result = {}  # result pool
    for i in range(l):
        def job(i):
            # return SQL execution result to result pool
            return sqlqueue._sql(threading.get_ident(), "INSERT INTO test VALUES (?);", (str(i),))
        tw.add(job, args=args(i), result=result, key=i)  # pass the pool and uid in
    tw.wait()
    # p(result)
    p(l, (time.time()-starttime)/l, time.time()-starttime)
    p(sqlqueue.sql("SELECT * FROM test;"))
    tw = ThreadWrapper(threading.Semaphore(l))
    starttime = time.time()
    for i in range(l):
        def job(i):
            sqlqueue._sql(threading.get_ident(), f"DELETE FROM test WHERE a = ?;", (str(i),))
        tw.add(job, args=args(i))
    tw.wait()
    p(l, (time.time()-starttime)/l, time.time()-starttime)
    # in order to use SqlQueue()._sql(), ThreadWrapper() is
    # recommended to queue threads, check threadwrapper for more info
    # SqlQueue()._sql() will raise execution error
    # it will only report it to the result
    # you should handle the errors separately


    starttime = time.time()
    for i in range(l):
        sqlqueue.sql("INSERT INTO test VALUES (?);", (str(i),))
    p(l, (time.time()-starttime)/l, time.time()-starttime)
    p(sqlqueue.sql("SELECT * FROM test;"))
    starttime = time.time()
    for i in range(l):
        sqlqueue.sql(f"DELETE FROM test WHERE a = ?;", (str(i),))
    p(l, (time.time()-starttime)/l, time.time()-starttime)
    p()
    sqlqueue.commit()  # manual commit
    # both manual and timeout commit always wait until
    # the current SQL execution is completed. 
    # the worker will not raise any error
    # however SqlQueue().sql() will re-raise execution error
```
