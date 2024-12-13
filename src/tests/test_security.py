from http import HTTPStatus

""" def test_create_access_token():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)
    decoded = decode(token, Settings.SECRETY_KEY, algorithms=[Settings.ALGORITHM])
    assert decoded['sub'] == data['sub']
    assert decoded['exp'] """


""" def test_get_token(client, user):
    response = client.post("/token", data={'username': user.email, 'password': user.senha})
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert  'access_token' in token
 """