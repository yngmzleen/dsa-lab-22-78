from flask import Flask, request, jsonify
import random
import requests

app = Flask(__name__)

# 1. Работа с GET эндпоинтами
@app.route('/number/', methods=['GET'])
def get_number():
    param = request.args.get('param', type=int)
    random_number = random.randint(1, 100)
    result = random_number * param
    return jsonify({"param": param, "random_number": random_number, "result": result, "operation": "mul"})

# 2. Работа с POST эндпоинтами
@app.route('/number/', methods=['POST'])
def post_number():
    data = request.get_json()
    json_param = data['jsonParam']
    random_number = random.randint(1, 100)
    result = random_number * json_param
    operation = random.choice(["sum", "sub", "mul", "div"])
    return jsonify({"jsonParam": json_param, "random_number": random_number, "result": result, "operation": operation})

# 3. Работа с DELETE эндпоинтами
@app.route('/number/', methods=['DELETE'])
def delete_number():
    random_number = random.randint(1, 100)
    operation = random.choice(["sum", "sub", "mul", "div"])
    return jsonify({"result": random_number, "operation": operation})

def send_get_request():
    param_value = random.randint(1, 10)
    response = requests.get(f'http://localhost:5000/number/?param={param_value}')
    data = response.json()
    print(f"GET Request - Param: {param_value}, Random Number: {data['random_number']}, Result: {data['result']}, Operation: {data['operation']}")
    return data

def send_post_request():
    json_param = random.randint(1, 10)
    response = requests.post('http://localhost:5000/number/', json={"jsonParam": json_param})
    data = response.json()
    print(f"POST Request - JSON Param: {json_param}, Random Number: {data['random_number']}, Result: {data['result']}, Operation: {data['operation']}")
    return data

def send_delete_request():
    response = requests.delete('http://localhost:5000/number/')
    data = response.json()
    print(f"DELETE Request - Random Number: {data['result']}, Operation: {data['operation']}")
    return data

def calculate_expression(get_data, post_data, delete_data):
    result = get_data['result']
    if post_data['operation'] == 'sum':
        result += post_data['result']
    elif post_data['operation'] == 'sub':
        result -= post_data['result']
    elif post_data['operation'] == 'mul':
        result *= post_data['result']
    elif post_data['operation'] == 'div':
        result /= post_data['result']

    if delete_data['operation'] == 'sum':
        result += delete_data['result']
    elif delete_data['operation'] == 'sub':
        result -= delete_data['result']
    elif delete_data['operation'] == 'mul':
        result *= delete_data['result']
    elif delete_data['operation'] == 'div':
        result /= delete_data['result']

    print(f"Final Result: {int(result)}")
    return int(result)

if __name__ == '__main__':
    app.run(debug=True)
    get_data = send_get_request()
    post_data = send_post_request()
    delete_data = send_delete_request()
    calculate_expression(get_data, post_data, delete_data)
