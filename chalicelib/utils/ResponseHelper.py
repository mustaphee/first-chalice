from chalice import Response


class SuccessResponse(Response):
    def __init__(self, message='', data=[], status_code=200, headers= { 'Content-Type': 'application/json'}, status='success'):
        super().__init__({ 'message': message, 'data': data, 'status': status }, headers=headers, status_code=status_code)

class ErrorResponse(Response):
    def __init__(self, message='', error={}, status_code=400, headers= { 'Content-Type': 'application/json'}, status='fail'):
        super().__init__({ 'message': message, 'error': error, 'status': status }, headers=headers, status_code=status_code)
