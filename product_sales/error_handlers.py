from flask import jsonify

from . import app


class InvalidAPIUsage(Exception):
    # Если статус-код для ответа API не указан, вернётся код 400:
    status_code = 400

    # Конструктор класса InvalidAPIUsage принимает на вход
    # текст сообщения и статус-код ошибки (необязательно).
    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code
