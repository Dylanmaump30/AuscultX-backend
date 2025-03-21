from flask import  jsonify, request


def already_exists():
    message = {
        'message': 'El usuario ya existe, por favor ingrese uno nuevo.'
    }
    response = jsonify(message)
    print(message)
    response.status_code = 409
    return response

def wrong_content():
    message = {
        'message': 'The content does not correspond to the expected one. ' + request.url,
        'status': 500
    }
    print(message)
    response = jsonify(message)
    response.status_code = 500
    return response
def data_not_match():
    message = {
        'message': 'Data do not match ' + request.url,
        'status': 404
    }
    print(message)
    response = jsonify(message)
    response.status_code = 404
    return response
def not_found():
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    print(message)
    response = jsonify(message)
    response.status_code = 404
    return response