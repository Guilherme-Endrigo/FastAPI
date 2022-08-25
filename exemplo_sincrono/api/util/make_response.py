from datetime import datetime

from fastapi import Request
from fastapi.responses import JSONResponse
import sqlalchemy

def make_response(request: Request, status_code=200, headers={}, body=None, message=None, data=None, error_code=None):
    """
    ja define os headers padrão para evitar problema de CORS, default para CORS_ORIGIN no env.
    """
    
    default_headers = {
        "Access-Control-Allow-Origin": request.headers.get('Origin', 'https://publicacoes.empiricus.com.br'),
        "Content-type": "application/json",
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": "Content-Type, Accept, Accept-Language, Accept-Encoding, Authorization",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
    }

    message_template = {
        'success': True,
        'status_code': status_code,
        'error_message': None,
        'error_code': str(error_code),
        'message': message
    }


    if body:
        message_template = body
    else:
        if status_code > 399:
            message_template['success'] = False
            message_template['message'] = None
            message_template['error_message'] = message
        
        elif message and type(message) is str:
            message_template['message'] = message

    if data:
        if type(data) == sqlalchemy.engine.row.Row:
            data = convert_row_to_dict(data)
        elif type(data) == list:
            data = list(map(convert_row_to_dict, data))
        else:
            rows = data['data']
            data['data'] = list(map(convert_row_to_dict, rows))
        message_template['data'] = data
    
    return JSONResponse(
        content=message_template,
        status_code=status_code,
        headers={**default_headers, **headers}
    )


def convert_row_to_dict(row):
    dictionary = {}

    for column in row.keys():
        row_value = getattr(row, column)
        if isinstance(row_value, datetime):
            row_value = int(row_value.timestamp())
        dictionary[column] = row_value

    return dictionary