import time, sqlite3
from modules.config import Env

class DB:
    @staticmethod
    def sql_execute(query: str, *, placeholders={} ,args=()):
        placeholders['%timestamp%'] = str(time.time())

        for placeholder in placeholders:
            query = query.replace('%' + placeholder + '%', str(placeholders[placeholder]))
        
        with sqlite3.connect(Env.DB_PATH) as conn:
            c = conn.cursor()
            try:
                c.execute(query, args)
                return c.lastrowid

            except EnvironmentError as e:
                print(e)
                return False
        
    @classmethod
    def sql_execute_many(cls, queries, *, args=()):
        result = []
        for query in queries:
            result.append(cls.sql_execute(query, args=args))
        return result

    @staticmethod
    def sql_fetch(query, last=False):
        with sqlite3.connect(Env.DB_PATH) as conn:
            conn.row_factory = sqlite3.Row

            c = conn.cursor()

            c.execute(query)

            result = [dict(row) for row in c.fetchall()]

            if last:
                if len(result) > 0:
                    return result[0]
                else:
                    return None
            else:
                return result

    @staticmethod
    def sql_fetch_value(query):
        with sqlite3.connect(Env.DB_PATH) as conn:
            c = conn.cursor()

            c.execute(query)

            fetched = c.fetchone()
            
            return fetched[0] if fetched != None else None

    # -------------
    #  Decorators
    # -------------

    @classmethod
    def execute(cls, func):
        def decorator(*args, **kwargs):
            res = func(*args,**kwargs)
            return cls.sql_execute(res) if type(res) == str else cls.sql_execute_many(res)
        decorator.query = func
        return decorator

    @classmethod
    def fetch(cls, func):
        def decorator(*args, **kwargs):
            return cls.sql_fetch(func(*args, **kwargs))
        return decorator

    @classmethod
    def fetch_last(cls, func):
        def decorator(*args, **kwargs):
            return cls.sql_fetch(func(*args, **kwargs), last=True)
        return decorator

    @classmethod
    def fetch_value(cls, func):
        def decorator(*args, **kwargs):
            return cls.sql_fetch_value(func(*args, **kwargs))
        return decorator

    @classmethod
    def exist(cls, func):
        def decorator(*args, **kwargs):
            result = cls.sql_fetch(func(*args, **kwargs))

            return False if len(result) == 0 else True
        return decorator