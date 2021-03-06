"""Create default Hug routers for each HTTP method
The default routers can be used to set common functionality such as headers
or error behavior.
"""
import hug
import falcon


@hug.format.content_type('application/json')
def default_response(data, request, response, **kwargs):
    """Generates the default JSON response for all endpoints.
    This is probably not needed, but it might be nice if we decide to do some custom formatting for
    json responses (which we might not even use anyways
    Parameters:
        data: the data to serialize (injected by Hug)
        request: an instance of falcon.request (injected by Hug)
        response: an instance of falcon.response (injected by Hug)
    Returns:
        string: encoded JSON string for output
    """
    # either errors or data, not both
    formatted_response = {}
    if isinstance(data, dict) and 'errors' in data:
        formatted_response['errors'] = data['errors']
    else:
        formatted_response['data'] = data

    kwargs['sort_keys'] = True
    r = hug.output_format.json(formatted_response, **kwargs)

    return r


def validation_errors(hug_errors):
    """Formats a list of validation errors generated by Hug. Each validation
    error is transformed into the standard error format.
    Parameters:
        hug_errors: a key-value pairs dict which contains all validation
        errors trapped when parsing the request input.
    Returns:
        dict: the list of validation errors formatted for output
    """
    assert 'errors' in hug_errors
    errors_in = hug_errors['errors']
    errors_out = []
    for (field, validation_error) in errors_in.items():
        status = falcon.HTTP_BAD_REQUEST
        description = "Input validation failed for field '{0}': {1}.".\
            format(field, validation_error)

        code = 500
        elem = {'status': status, 'description': description, 'code': code}
        errors_out.append(elem)

    return {'errors': errors_out}


requires_list = []

# default GET routes
get = hug.object.get(
    output=default_response,
    on_invalid=validation_errors,
    requires=requires_list
)

get_html = hug.object.get(
    output=hug.output_format.html,
    on_invalid=validation_errors,
    requires=requires_list
)

# default POST routes
post = hug.object.post(
    output=default_response,
    on_invalid=validation_errors,
    requires=requires_list
)

# default PUT routes
put = hug.object.put(
    output=default_response,
    on_invalid=validation_errors,
    requires=requires_list
)

# default PATCH routes
patch = hug.object.patch(
    output=default_response,
    on_invalid=validation_errors,
    requires=requires_list
)

# default DELETE routes
delete = hug.object.delete(
    output=default_response,
    on_invalid=validation_errors,
    requires=requires_list
)
