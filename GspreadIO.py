import gspread
import json
from authlib.client import AssertionSession

def create_assertion_session(conf_file, scopes, subject=None):
    with open(conf_file, 'r') as f:
        conf = json.load(f)

    token_url = conf['token_uri']
    issuer = conf['client_email']
    key = conf['private_key']
    key_id = conf.get('private_key_id')

    header = {'alg': 'RS256'}
    if key_id:
        header['kid'] = key_id

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
    session = create_assertion_session(credentials, scopes)

    gc = gspread.Client(None, session)

    return gc
    #예외처리 추후 추가


def openGsFile(gsclient, filename):
    file = gsclient.open(filename)

    return file
    #예외처리 추후 추가

if(__name__ == '__main__'):
    client = openGsClient('ScryfallCube-80b58226a864.json')
    file = openGsFile(client, 'ScryfallCubeIO')
    wks = file.worksheet("시트1")
    print(wks.get_all_records())