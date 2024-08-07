import json
import helper
from datetime import datetime
from openai import OpenAI, OpenAIError
import pymysql
import pymysql.cursors

class MyOpenAI:

    def __init__(self):
        self.client = OpenAI()
        # connect db
        # self.conn = helper.connect_db()

    def get_response(self, message):
        # set current date
        date = datetime.today().strftime('%d/%m/%Y')
        # set vars
        categories = helper.config('google_sheet.categories')
        payment_methods = helper.config('google_sheet.payment_methods')
        # define messages
        messages = [
            {
                'role': 'system',
                'content': f'Ritorna un json con le transazioni, ognuna con: date(dd/mm/yyyy, oggi: {date}), payment_method (one, [{payment_methods}], default: "Contanti"), category (one, [{categories}]), amount, note (max 10 caratteri, not null or set "-")'
            },
            {
                'role': 'user',
                'content': message
            }
        ]
        try:
            # get response
            response = self.client.chat.completions.create(
                model=helper.config('openai.model'),
                messages=messages,
                max_tokens=helper.config('openai.max_tokens'),
                temperature=helper.config('openai.temperature'),
                response_format=helper.config('openai.response_format'),
            )
            print(response)
            # return message content response
            return response.choices[0].message.content

        except OpenAIError as e:
            # handle all OpenAI API errors
            print(f"Error: {e}")