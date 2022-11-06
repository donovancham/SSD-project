import os

def test_base_route(flask_app):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = flask_app.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Add your credentials" in response.data
    assert b"Clinic Management System-Team 10" in response.data
    

def test_login_route(flask_app):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check the response is valid
    """
    response = flask_app.get('/login', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Add your credentials" in response.data
    assert b"Remember password" in response.data
    

def test_register_route(flask_app):
    """
    GIVEN a Flask application
    WHEN the '/register' page is requested (GET)
    THEN check the response is valid
    """
    response = flask_app.get('/register', follow_redirects=True)
    assert response.status_code == 200
    assert b"Register" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_password_reset_route(flask_app):
    """
    GIVEN a Flask application
    WHEN the '/password_reset' page is requested (GET)
    THEN check the response is valid
    """
    response = flask_app.get('/password_reset', follow_redirects=True)
    assert response.status_code == 200
    assert b"Password Recovery" in response.data
    assert b"Enter your account's email address and we will send you a link to reset your password." in response.data
    assert b"Send" in response.data
    
    
def test_all_forbidden_routes(flask_app):
    """
    GIVEN a Flask application
    WHEN the a page that requires authorization is requested (GET)
    THEN check the response should be forbidden
    """
    forbidden_routes = []
    path = os.path.abspath("cmsapp/templates")
    for subpath in os.listdir(path):
        forbidden_routes.extend(os.listdir(path))
    
    for route in forbidden_routes:
        response = flask_app.get('/' + route, follow_redirects=True)
        assert response.status_code == 403