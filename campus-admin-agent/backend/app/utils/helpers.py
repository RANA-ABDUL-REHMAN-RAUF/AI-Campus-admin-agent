def format_response(data):
    return {"status": "success", "data": data}

def format_error(message):
    return {"status": "error", "message": message}

def paginate_data(data, page: int, page_size: int):
    start = (page - 1) * page_size
    end = start + page_size
    return data[start:end]

def validate_id(id):
    if not isinstance(id, int) or id <= 0:
        raise ValueError("Invalid ID: must be a positive integer.")