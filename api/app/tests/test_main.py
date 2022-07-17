from fastapi.testclient import TestClient

from app.main import app

'''
This file contains the tests which we will run against our API
to ensure that the business logic works as intended.

This does not include unittests to test the correctness of the 
code base at the function level. 
'''

# Instantiate the test client
client = TestClient(app)


# Test restricted http methods
def test_http_methods():
    '''
    '''
    
    res_get = client.post('/databases?release=106')
    res_post = client.post('/databases')
    res_put = client.put('/databases')
    res_patch = client.patch('/databases')

    assert res_get.status_code == 200
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

# Test error handling of unknown db_type
def test_unknown_db_type():
    '''
    '''
    
    res_bad_db_type = client.get('/databases?db_type=unknown')
    res_good_db_type = client.get('/databases?db_type=cdna&name=homo%20sapiens')

    assert res_bad_db_type.json() == []
    assert len(res_good_db_type.json()) > 0

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
    res_long_name = client.get('/databases?name=homo%20sapiens')

    assert res_short_name.status_code == 400
    assert res_long_name.status_code == 200

# Test type checking on resource parameter
def test_resource_type_check():
    '''
    '''

    res_resource_str = client.get('/databases?release=ninetyone')
    res_resource_int = client.get('/databases?release=91')

    assert res_resource_str.status_code == 400    
    assert res_resource_int.status_code == 200    
