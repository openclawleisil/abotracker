import pytest
from app import app, db, Subscription

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_add_subscription(client):
    resp = client.post('/add', data={'name':'Test','amount':'5.0','interval':'monthly'})
    assert resp.status_code == 302
    with app.app_context():
        subs = Subscription.query.all()
        assert len(subs) == 1
        assert subs[0].name == 'Test'

def test_monthly_total(client):
    client.post('/add', data={'name':'A','amount':'10.0','interval':'monthly'})
    client.post('/add', data={'name':'B','amount':'120.0','interval':'yearly'})
    # yearly should not count as monthly in current simple logic
    resp = client.get('/')
    assert b'Gesamt monatlich' in resp.data
