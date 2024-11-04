from flask import Flask, request, jsonify
from flask_cors import CORS
from evaluator import determine_chatbot_preset, validate_score, get_user_metrics
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running"""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    })

@app.route('/api/process-survey', methods=['POST'])
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
    try:
        # Validate request contains JSON data
        if not request.is_json:
            raise ValueError("Request must contain JSON data")

        user_metrics = request.json
        logger.info(f"Received survey metrics: {user_metrics}")

        # Validate required metrics are present
        required_metrics = ['metric_a', 'metric_b', 'metric_c']
        for metric in required_metrics:
            if metric not in user_metrics:
                raise ValueError(f"Missing required metric: {metric}")
            
            # Validate score ranges
            if not validate_score(user_metrics[metric]):
                raise ValueError(f"Invalid score for {metric}. Must be between 0-100")

        # Process survey and get recommended presets
        chatbot_presets = determine_chatbot_preset(user_metrics)
        logger.info(f"Determined presets: {chatbot_presets}")

        return jsonify({
            'success': True,
            'presets': chatbot_presets,
            'metrics': user_metrics
        })

    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400

    except Exception as e:
        logger.error(f"Error processing survey: {str(e)}")
        return jsonify({
            'success': False,
            'error': "An unexpected error occurred"
        }), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get available metrics and their descriptions"""
    try:
        metrics = get_user_metrics()
        return jsonify({
            'success': True,
            'metrics': metrics
        })
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        return jsonify({
            'success': False,
            'error': "Error retrieving metrics"
        }), 500

if __name__ == '__main__':
    logger.info("Starting Survey Calculator API...")
    app.run(debug=True, host='0.0.0.0', port=5000)