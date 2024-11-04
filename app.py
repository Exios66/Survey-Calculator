from flask import Flask, request, jsonify
from flask_cors import CORS
from evaluator import determine_chatbot_preset
import logging

app = Flask(__name__)
CORS(app)

@app.route('/api/process-survey', methods=['POST'])
def process_survey():
    try:
        user_metrics = request.json
        chatbot_presets = determine_chatbot_preset(user_metrics)
        return jsonify({
            'success': True,
            'presets': chatbot_presets
        })
    except Exception as e:
        logging.error(f"Error processing survey: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 