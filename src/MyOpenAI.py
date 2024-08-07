import json
from datetime import datetime
from openai import OpenAI, OpenAIError

class MyOpenAI:

    def __init__(self):
        self.client = OpenAI()

    def get_response(self, message):
        # set current date
        date = datetime.today().strftime('%d/%m/%Y')
        # set available categories
        categories = ['Stipendio MS', 'Mancia', 'Betting in', 'Altro in', 'Rata famiglia', 'Rata auto / Assicurazione', 'Benzina', 'Trasporti', 'Svago', 'Cibo', 'Bar', 'Vestiti', 'Ricarica', 'Abbonamenti', 'Medicine', 'Regali', 'Betting out', 'Altro out']
        payment_methods = ['Intesa SanPaolo', 'Buddybank', 'Contanti']
        # categories = {
        #     'income': [ 'Stipendio MS', 'Mancia', 'Betting in', 'Altro in'],
        #     'expenses': [ 'Rata famiglia', 'Rata auto / Assicurazione', 'Benzina', 'Trasporti', 'Svago', 'Cibo', 'Bar', 'Vestiti', 'Ricarica', 'Abbonamenti', 'Medicine', 'Regali', 'Betting out', 'Altro out']
        # }
        # define messages
        messages = [
            {
                'role': 'system',
                'content': f'Ritorna un json con le transazioni, ognuna con: date(dd/mm/yyyy, oggi: {date}), payment_method (one, [{payment_methods}], default: "Contanti"), category (one, [{categories}]), amount, note (max 10 caratteri)'
            },
            {
                'role': 'user',
                'content': message
            }
        ]
        try:
            # get response
            # response_format={ "type": "json_object" }
            # response = self.client.chat.completions.create(model='gpt-4', messages=messages, max_tokens=200, temperature=0.5)
            response = self.client.chat.completions.create(model='gpt-4o-mini', messages=messages, max_tokens=200, temperature=0.5, response_format={ "type": "json_object" })
            print(response)
            # return message content response
            return response.choices[0].message.content

        except OpenAIError as e:
            # handle all OpenAI API errors
            print(f"Error: {e}")