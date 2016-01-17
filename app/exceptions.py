class AppError(Exception):
    status_code = 200
    message = 'An exception occured.'

    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        if message is not None:
            self.message = message

    @property
    def serialize(self):
        return {
            'success': False,
            'errors': [self.message]
        }


class NotFoundError(AppError):
    def __init__(self, model):
        AppError.__init__(self, 'Specified ' + model.__tablename__ +
                           ' does not exist.')


class IdError(AppError):
    def __init__(self, key):
        AppError.__init__(self, 'Key `' + key + '` must be an integer.')
