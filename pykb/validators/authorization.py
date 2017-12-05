import re
import pykbdb
import falcon
import datetime

class AuthorizationValidator:
    '''
    Validate the authorization header token.

    This will look up the user record for the session and put it in the parameters under "session".
    '''

    authorization_header_re = re.compile('^\s*bearer\s+(.*)$', re.IGNORECASE)

    def __init__(self):
        pass

    def __call__(self, req, resp, resource, params):
        authorization = req.get_header('Authorization', False, '')
        m = AuthorizationValidator.authorization_header_re.match(authorization)
        if m:
            session = pykbdb.Session()
            websessions = session.query(pykbdb.WebSession).filter(pykbdb.WebSession.authorization == m[1])
            if websessions.count() > 0:
                now = datetime.datetime.now()
                if websessions[0].expiration < now:
                    session.query(pykbdb.WebSession).filter(pykbdb.WebSession.expiration < now).delete()
                    session.commit()
                    session.close()
                    raise falcon.HTTPUnauthorized(description = "Session expired.")
                else:
                    params['session'] = websessions[0]
                    session.close()

            else:
                session.close()
                raise falcon.HTTPUnauthorized(description = "Session not found.")
