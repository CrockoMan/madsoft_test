JWT_LIFITIME_SECONDS = 3600
PASSWORD_MIN_LEN = 3

DONATE_DISTRIBUTION_ATTEMPTS = 100

NAME_MAX_LEN = 100

TEXT_LIMIT = 30
EMPTY_FIELD = 'Поле не может быть пустым!'

MEME_EMPTY = 'Пустое значение!'
MEME_EXISTS = 'Мем уже существует!'
MEME_NOT_FOUND = 'Мем не существует!'

FILE_NOT_FOUND = 'Файл отсутствует в хранилище'

USER_REMOVE_EXCEPTION = 'Удаление запрещено'


PASSWORD_LENGTH_ERROR = ('Пароль должен быть не меньше '
                         f'{PASSWORD_MIN_LEN} символов')
PASSWORD_CONTAIN_EMAIL_ERROR = 'Пароль не может содержать e-mal'
PASSWORD_ALREADY_REGISTERED = 'Пользователь зарегистрирован.'