
class RoleValidator:
    '''
    Validate that the role of a session is appropriate.

    The session must be stored in the request params under 'session'.
    '''

    def __init__(self, role):
        self.role = role

    def __call__(self, req, resp, resource, params):
        print("Checking for role "+self.role)
        if 'session' in params:
            print("GOT SESSION.", params['session'])
