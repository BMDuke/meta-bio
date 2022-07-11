from fastapi.testclient import TestClient

from app.main import app

'''
'''

# Instantiate the test client
client = TestClient(app)


# Test restricted http methods
def test_http_methods():
    '''
    '''

    res_post = client.post('/databases')
    res_put = client.put('/databases')
    res_patch = client.patch('/databases')

    assert res_post.status_code == 405
    assert res_put.status_code == 405
    assert res_patch.status_code == 405

# Test error handling of unknown organism
def test_unknown_organism():
    '''
    '''
    
    res_human = client.get('/databases?name=human')
    res_homo_sapiens = client.get('/databases?name=homo%20sapiens')

    assert res_human.status_code == 404
    assert res_homo_sapiens.status_code == 200

# Test error is thrown if no query parameters are provided
def test_no_parameters():
    '''
    '''

    res_no_params = client.get('/databases')

    assert res_no_params.status_code == 400

# Test error is thrown if organism length is less than 3
def test_short_organism_name():
    '''
    '''

    res_short_name = client.get('/databases?name=a')

    assert res_short_name.status_code == 400

# Test type checking on resource parameter
def test_resource_type_check():
    '''
    '''

    res_resource = client.get('/databases?release=ninetyone')

    assert res_resource.status_code == 400    