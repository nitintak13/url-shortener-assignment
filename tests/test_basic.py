import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Health Check
def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

# API Health
def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['message'] == 'URL Shortener API is running'

# Valid URL Shortening
def test_shorten_url_success(client):
    url_data = {"url": "https://example.com"}
    response = client.post('/api/shorten', json=url_data)
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data

# Invalid URL
def test_shorten_url_invalid(client):
    url_data = {"url": "invalid-url"}
    response = client.post('/api/shorten', json=url_data)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

# Missing URL in body
def test_shorten_url_missing_field(client):
    response = client.post('/api/shorten', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

# Redirection and Click Tracking
def test_redirection_and_stats(client):
    # Shorten a valid URL
    original_url = "https://google.com"
    shorten_res = client.post('/api/shorten', json={"url": original_url})
    short_code = shorten_res.get_json()["short_code"]

    # Access the short URL (redirect)
    redirect_res = client.get(f'/{short_code}')
    assert redirect_res.status_code == 302  # Redirect
    assert redirect_res.location == original_url

    # Check analytics
    stats_res = client.get(f'/api/stats/{short_code}')
    assert stats_res.status_code == 200
    stats = stats_res.get_json()
    assert stats["url"] == original_url
    assert stats["clicks"] >= 1
    assert "created_at" in stats

# Invalid short code stats
def test_stats_not_found(client):
    response = client.get('/api/stats/notarealcode')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
