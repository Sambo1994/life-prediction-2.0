import random
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)

class TrinaryProcessor:
    def __init__(self):
        self.state = None

    def set_state(self, value):
        if value in ['+1', '-0', '+/-10']:
            self.state = value
        else:
            raise ValueError("Invalid state. Allowed states: '+1', '-0', '+/-10'")

    def resolve_state(self):
        if self.state == '+/-10':
            probability = random.uniform(0, 1)
            self.state = '+1' if probability >= 0.6 else '-0'
        return self.state
    
    def process(self):
        return self.resolve_state() if self.state == '+/-10' else self.state

def predict_death_date(age):
    processor = TrinaryProcessor()
    processor.set_state('+/-10')
    resolved_state = processor.process()
    life_expectancy = 100 if resolved_state == '+1' else 60
    years_remaining = random.randint(1, life_expectancy - age)
    death_date = datetime.now() + timedelta(days=years_remaining * 365)
    return death_date.strftime('%Y-%m-%d')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    age = int(data.get('age', 0))
    if age <= 0 or age >= 100:
        return jsonify({"error": "Invalid age. Must be between 1 and 99."}), 400
    death_date = predict_death_date(age)
    return jsonify({"death_date": death_date})

def handler(event, context):
    return app(event, context)
