from werkzeug.security import safe_str_cmp
from db_handler import Db

db = Db()

class User(object):
    def __init__(self, user_name, user_id):
        self.id = user_id
        self.user_name = user_name


def authenticate(user_name, password):
    sql = f'''
        select *
        from app_users
        where user_name = '{user_name}'
        '''
    df = db.query(sql)
    if len(df) > 0:
        df = df.query(f"user_name == '{user_name}'")
        user_data = df.iloc[0]
        if safe_str_cmp(user_data['user_password'].encode('utf-8'), password.encode('utf-8')):
            return User(str(user_data['user_id']),
                        str(user_data['user_name'])
                        )


def identity(payload):
    user_name = payload['identity']
    user_id = db.query(f"select * from app_users where user_name = '{user_name}'").iloc[0]['user_id']
    return {'user_name': user_name , 'user_id' : user_id}
