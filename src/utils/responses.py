from errors.detailed_error import DetailedError


# response is what js code in 'ui' folder gets as a result of exposed python function

def create_error_response(error: DetailedError):
    return dict(error=vars(error), data=None)

def create_successful_response(data = None):
    return dict(error=None, data=data)

