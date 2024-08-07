import os
import json
import pymysql
import pymysql.cursors
from datetime import datetime

def sanitize_response(response_content):
    # json decode
    decoded_content = json.loads(response_content)
    extracted_array = None
    # remove key "transactions" and return only list
    if isinstance(decoded_content, dict):
        for key, value in decoded_content.items():
            if isinstance(value, list):
                extracted_array = value
                break

    if extracted_array is None:
        extracted_array = decoded_content

    required_fields = {'date', 'amount', 'payment_method', 'category', 'note'}

    return [obj for obj in extracted_array if required_fields.issubset(obj.keys())]

# load settings.json file
def load_settings():
    # absolute path
    current_dir = os.path.dirname(__file__)
    # build settings.json path
    settings_path = os.path.join(current_dir, 'config', 'settings.json')
    # load file
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    # return file content
    return settings

# retrieve config param from key (settings.json)
def config(key):
    if '.' in key:
        # return array of splitted keys
        elements = key.split('.')
        # load config file
        settings = load_settings()

        for element in elements:
            # create settings[element1][element2]...
            settings = settings.setdefault(element, {})

        return settings

    return None

# convert dd/mm/yyyy to yyyy-mm-dd
def format_db_date(input_date):
    return datetime.strptime(input_date, '%d/%m/%Y').strftime('%Y-%m-%d')

# connect db
def connect_db():
    conn = pymysql.connect(
        host='mysql',
        user='root',
        password='password',
        db='cash-flow-tracker-bot',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def insert_db(conn, sql, values):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, (values))

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def save_transaction(conn, transaction):
    # create sql script
    sql = "INSERT INTO transactions (category, amount, payment_method, note, paid_at) VALUES (%s, %s, %s, %s, %s)"
    # set values
    values = [
        transaction['category'].lower(),
        transaction['amount'],
        transaction['payment_method'].lower(),
        transaction['note'].lower(),
        format_db_date(transaction['date'])
    ] #
    # save
    insert_db(conn, sql, values)