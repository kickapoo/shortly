import json

# Note:
# Working with axios lib. By default the response schema
# has structure https://github.com/axios/axios#response-schema
# this why the ugly data={'data': {}} exists


def test_short_me_empty_client_request(client):

    headers = {'content-type': 'application/json'}
    data = json.dumps({'data': {}})
    r = client.post('/api/short-me', headers=headers, data=data)

    response_data = json.loads(r.data)
    assert r.status_code == 400
    assert response_data['errors'] == ['Empty request']


def test_short_me_invalid_client_request(client):

    headers = {'content-type': 'application/json'}
    data = json.dumps({'data': {'raw_lng_url': 'Iam Batman'}})
    r = client.post('/api/short-me', headers=headers, data=data)

    response_data = json.loads(r.data)
    assert r.status_code == 400
    assert response_data['errors'] == ['Invalid url syntax']


def test_short_me_valid_client_request(client, db):

    headers = {'content-type': 'application/json'}
    data = json.dumps({
        'data': {'raw_lng_url': 'https://github.com/kickapoo/'}
    })
    r = client.post('/api/short-me', headers=headers, data=data)

    response_data = json.loads(r.data)
    assert r.status_code == 200
    assert 'srt_url' in response_data['data'].keys()
