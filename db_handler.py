import psycopg2
import pandas as pd
from config import conn_string


class Db:
    def __init__(self):
        self.con_string = conn_string

    def query(self, sql):
        with psycopg2.connect(self.con_string) as con:
            df = pd.read_sql(sql, con)
        return df

    def commit_to_db(self, sql):
        with psycopg2.connect(self.con_string) as con:
            cur = con.cursor()
            cur.execute(sql)
            con.commit()

    def get_all_messages_for_user(self, user_id: int, only_unread: bool, last_message=False):
        sql = f'''
        select messages_id,
               messages_content,
               messages_subject,
               send_date,
               is_read,
               au_sender.user_name as sender,
               au_receiver.user_name as receiver
        from messages ms
        join app_users au_sender
        on ms.sender_id = au_sender.user_id
        join app_users au_receiver
        on ms.receiver_id = au_receiver.user_id
        where receiver_id = {user_id}
        '''
        sql += ' and is_read = false' if only_unread else ''
        df = self.query(sql)
        if len(df) > 0:
            if last_message:
                df = df.sort_values('send_date', ascending=True)
                df = df.head(1)
        return df
