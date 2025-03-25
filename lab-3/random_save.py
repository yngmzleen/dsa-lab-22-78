from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# ранение результатов запросов
results = {
    "get": None,
    "post": None,
    "delete": None
}

@app.route('/number', methods=['GET'])
def process_get():
    # Генерируем случайное число от 1 до 10 для param
    param_value = random.randint(1, 10)
    operation = random.choice(["sum", "sub", "mul", "div"])
    results["get"] = {"param": param_value, "operation": operation}
    return jsonify(results["get"])

@app.route('/number', methods=['POST'])
def process_post():
    # Генерируем случайное число от 1 до 10
    json_param = random.randint(1, 10)
    operation = random.choice(["sum", "sub", "mul", "div"])
    results["post"] = {"number": json_param, "operation": operation}
    return jsonify(results["post"])

@app.route('/number', methods=['DELETE'])
def process_delete():
    number = random.randint(1, 10)
    operation = random.choice(["sum", "sub", "mul", "div"])
    results["delete"] = {"number": number, "operation": operation}
    return jsonify(results["delete"])

# эндпоинт для вычисления выражения
@app.route('/calculate', methods=['GET'])
def calculate_expression():

    # Получаем числа и операции из сохраненных результатов
    get_data = results["get"]
    post_data = results["post"]
    delete_data = results["delete"]

    # Начинаем с первого числа
    result = get_data['param']  # Используем param из GET запроса

    # Применяем операцию из POST запроса
    if post_data['operation'] == 'sum':
        result += post_data['number']
    elif post_data['operation'] == 'sub':
        result -= post_data['number']
    elif post_data['operation'] == 'mul':
        result *= post_data['number']
    elif post_data['operation'] == 'div':
        result /= post_data['number']

    # Применяем операцию из DELETE запроса
    if delete_data['operation'] == 'sum':
        result += delete_data['number']
    elif delete_data['operation'] == 'sub':
        result -= delete_data['number']
    elif delete_data['operation'] == 'mul':
        result *= delete_data['number']
    elif delete_data['operation'] == 'div':
        result /= delete_data['number']

    final_result = int(result)
    return jsonify({
        "get_operation": f"{get_data['param']} {get_data['operation']}",
        "post_operation": f"{post_data['number']} {post_data['operation']}",
        "delete_operation": f"{delete_data['number']} {delete_data['operation']}",
        "final_result": final_result
    })

if __name__ == '__main__':
    app.run(debug=True) 