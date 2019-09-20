import gspread
import json
from authlib.client import AssertionSession


def create_assertion_session(conf_file, scopes, subject=None):
    with open(conf_file, 'r') as f:
        try:
            conf = json.load(f)
        except json.decoder.JSONDecodeError:
            print("unable to decode Credential file")
            return None

    token_url = conf["token_uri"]
    issuer = conf["client_email"]
    key = conf["private_key"]
    key_id = conf.get('private_key_id')

    header = {'alg': 'RS256'}
    if key_id:
        header["kid"] = key_id

    # Google puts scope in payload
    claims = {'scope': ' '.join(scopes)}
    return AssertionSession(
        grant_type=AssertionSession.JWT_BEARER_GRANT_TYPE,
        token_url=token_url,
        issuer=issuer,
        audience=token_url,
        claims=claims,
        subject=subject,
        key=key,
        header=header,
    )


def openGsClient(credentials):
    scopes = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]

    try:
        session = create_assertion_session(credentials, scopes)
        if session is None:
            raise ValueError
        gc = gspread.Client(None, session)
        return gc
    except FileNotFoundError:
        print("No such credential file")
        return None
    except ValueError:
        print("Cannot get the session")
        return None
    except Exception as e:
        print("%s during opening Google Spreadsheet client" % e)
        return None
