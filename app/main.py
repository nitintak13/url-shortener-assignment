from flask import Flask, request, jsonify, redirect
from app.models import store
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)

# Health Check Endpoint
@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    original_url = data['url']

    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL format"}), 400

   
    short_code = generate_short_code()
    while store.get(short_code):
        short_code = generate_short_code()

    
    store.save(short_code, original_url)

    return jsonify({
        "short_code": short_code,
        "short_url": request.host_url + short_code
    }), 201


@app.route('/<short_code>', methods=['GET'])
def redirect_to_original(short_code):
    record = store.get(short_code)

    if not record:
        return jsonify({"error": "Short URL not found"}), 404

    store.increment_clicks(short_code)
    return redirect(record['original_url'])


@app.route('/api/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    record = store.get(short_code)

    if not record:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "url": record['original_url'],
        "clicks": record['clicks'],
        "created_at": record['created_at'].isoformat() + 'Z'
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
