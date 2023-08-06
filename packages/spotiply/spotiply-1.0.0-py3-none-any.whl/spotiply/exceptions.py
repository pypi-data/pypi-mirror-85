class SpotifyException(Exception):
    def __init__(self, http_status_code, message, reason=None):
        self.http_status_code = http_status_code
        self.message = message
        self.reason = reason

    def __str__(self):
        return f'http.status_code: {self.http_status_code},\
 message: {self.message} reason: {self.reason}'
