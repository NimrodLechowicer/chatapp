from flask import Flask, jsonify, request
from config import *
from db_handler import Db
from aouth import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
app_init(app)
db = Db()
jwt = JWT(app, authenticate, identity)


@app.route('/write_message', methods=['POST'])
@jwt_required()
def write_message():
    """
    this route get a post request with a message parameters :
    - receiver
    - content
    - subject
    the function inserts the message into the messages database.
    :return:
    status : <ok/error>
    details : <if error occurred>
    """
    js = request.json
    if js and all(headers in ['receiver', 'content', 'subject'] for headers in js):
        receiver_data = db.query(f"select * from app_users where user_name = '{js['receiver']}'")
        if len(receiver_data) > 0:
            receiver_data = receiver_data.iloc[0]
            db.commit_to_db(
                f'''
                insert into messages (messages_content,messages_subject,receiver_id,sender_id,is_read) 
                values ('{js['content'].replace("'", "''")}',
                        '{js['subject'].replace("'", "''")}',
                        {receiver_data['user_id']},
                        {current_identity['user_id']},
                        false);
                '''
            )
            return jsonify({'status': 'ok'}), 201
        else:
            error_details = 'receiver user dose not exist'
    else:
        error_details = 'problem with headers'

    return jsonify({'status': 'error',
                    'details': error_details
                    }), 400


@app.route('/get_all_messages', methods=['GET'])
@jwt_required()
def get_all_messages():
    """
    this route return all the messages for user
    """
    only_unread = request.args.get('only_unread')  # if the endpoint wants to get only the unread messages
    df = db.get_all_messages_for_user(current_identity['user_id'], only_unread)
    if len(df) > 0:
        return jsonify({'data': df.to_dict('records')})
    else:
        return jsonify({'data': []})


@app.route('/read_message', methods=['GET'])
@jwt_required()
def read_message():
    """
    this route return the firs message that the user received
    and update the db that the user read the message
    :return:
    the message if exists
    if not exists return empty list
    """
    df = db.get_all_messages_for_user(current_identity['user_id'], only_unread=True, last_message=True)
    if len(df) > 0:
        db.commit_to_db(f'''
        update messages set is_read = true where messages_id = {df.iloc[0]['messages_id']}
        ''')
    data = df.to_dict('records')
    return jsonify({'data': data[0] if data else data})


@app.route('/delete_message/<message_id>',  methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    df = db.query(f'''
    select *
    from messages
    where messages_id = {message_id}
    and (sender_id = {current_identity['user_id']} or receiver_id = {current_identity['user_id']})
    ''')
    if len(df) > 0:
        db.commit_to_db(f'delete from messages where messages_id = {message_id}')
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'no permissions'}), 403


if __name__ == '__main__':
    app.run(debug=True)
