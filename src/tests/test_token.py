from jwt import decode

from services.security import create_access_token

# texte para verificar se o token foi criado com sucesso
def test_jwt():
    data = {'test': 'test'} 
    token = create_access_token(data) 

    decoded = decode(token, 'FSDFSDFSDFSDFSDSDS.ASDASDASDASD', algorithms=['HS256']) 

    assert decoded['test'] == data['test']
    assert 'exp' in decoded 