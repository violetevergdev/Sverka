
class GetFailedAttr(Exception):
    def __init__(self, message="Передача ошибочного значения параметра"):
        self.message = message
        super().__init__(self.message)


class FailedExpectedLen(Exception):
    def __init__(self, message="Неверная ожидаемая длина данных в БД"):
        self.message = message
        super().__init__(self.message)




