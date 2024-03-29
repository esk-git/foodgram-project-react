from constants import USERNAME_MAX_LENGTH
from django.contrib.auth.validators import UnicodeUsernameValidator


class UsernameRegexValidator(UnicodeUsernameValidator):
    """Валидация имени пользователя."""
    regex = r'^[\w.@+-]+\Z'
    flags = 0
    max_length = USERNAME_MAX_LENGTH
    message = ('Имя пользователя может содержать'
               ' только буквы, цифры и знаки @/./+/-/_.')
    error_messages = {
        'invalid': 'Набор символов не более 150. '
                   'Только буквы, цифры и @/./+/-/_',
        'required': 'Поле не может быть пустым',
    }
