from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from evaluator import determine_chatbot_preset, validate_score, get_user_metrics
import logging
import sys
import time
from functools import wraps
from datetime import datetime

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'api_{datetime.now().strftime("%Y%m%d")}.log')  # Daily log file
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app with additional security headers
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Request logging middleware
def log_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_start = time.time()
        response = f(*args, **kwargs)
        request_duration = time.time() - request_start
        logger.info(f"Request to {request.path} completed in {request_duration:.2f}s")
        return response
    return decorated_function

# Error handling decorator
def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as ve:
            logger.error(f"Validation error: {str(ve)}")
            return jsonify({
                'success': False,
                'error': str(ve),
                'error_type': 'ValidationError'
            }), 400
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return jsonify({
                'success': False,
                'error': "An unexpected error occurred",
                'error_type': 'ServerError'
            }), 500
    return decorated_function

@app.before_request
def before_request():
    """Log incoming request details"""
    logger.debug(f"Incoming {request.method} request to {request.path}")
    logger.debug(f"Request headers: {dict(request.headers)}")
    if request.data:
        logger.debug(f"Request payload: {request.get_json(silent=True)}")

@app.after_request
def after_request(response):
    """Add security headers and log response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    logger.debug(f"Response status: {response.status}")
    return response

@app.route('/health', methods=['GET'])
@log_request
def health_check():
    """Health check endpoint to verify API is running"""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/process-survey', methods=['POST'])
@log_request
@handle_errors
def process_survey():
    """
    Process survey results and return recommended chatbot presets
    
    Expected request body:
    {
        "metric_a": score (0-100),
        "metric_b": score (0-100),
        "metric_c": score (0-100)
    }
    """
    if not request.is_json:
        raise ValueError("Request must contain JSON data")

    user_metrics = request.json
    logger.info(f"Received survey metrics: {user_metrics}")

    # Validate required metrics are present and their types
    required_metrics = ['metric_a', 'metric_b', 'metric_c']
    for metric in required_metrics:
        if metric not in user_metrics:
            raise ValueError(f"Missing required metric: {metric}")
        
        if not isinstance(user_metrics[metric], (int, float)):
            raise ValueError(f"Invalid type for {metric}. Must be numeric")
            
        # Validate score ranges
        if not validate_score(user_metrics[metric]):
            raise ValueError(f"Invalid score for {metric}. Must be between 0-100")

    # Process survey and get recommended presets
    chatbot_presets = determine_chatbot_preset(user_metrics)
    logger.info(f"Determined presets: {chatbot_presets}")

    response_data = {
        'success': True,
        'presets': chatbot_presets,
        'metrics': user_metrics,
        'timestamp': datetime.now().isoformat()
    }

    return jsonify(response_data)

@app.route('/api/metrics', methods=['GET'])
@log_request
@handle_errors
def get_metrics():
    """Get available metrics and their descriptions"""
    metrics = get_user_metrics()
    return jsonify({
        'success': True,
        'metrics': metrics,
        'timestamp': datetime.now().isoformat()
    })

# Add rate limiting
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'success': False,
        'error': 'Rate limit exceeded',
        'error_type': 'RateLimitError'
    }), 429

# Add 404 handler
@app.errorhandler(404)
def not_found_error(e):
    return jsonify({
        'success': False,
        'error': 'Resource not found',
        'error_type': 'NotFoundError'
    }), 404

if __name__ == '__main__':
    logger.info("Starting Survey Calculator API...")
    logger.info(f"Debug mode: {app.debug}")
    logger.info(f"CORS enabled for /api/* endpoints")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)