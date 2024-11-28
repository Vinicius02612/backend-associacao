from jwt import decode
from services.security import create_access_token, SECRETY_KEY,ALGORITHM


def test_create_access_token():
    data = {'test': 'test'}
    token = create_access_token(data)
    decoded = decode(token, SECRETY_KEY, algorithms=[ALGORITHM])
    assert decoded['test'] == 'test'
    assert decoded['exp']
