"""
Flask application for Voice Chatbot India - Maternal Health Support
Main API endpoints for testing and voice integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Add project root to path for imports
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.use_cases.test_screening import TestScreeningUseCase

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize use cases
test_screening = TestScreeningUseCase()

# In-memory context storage (for demo - use database in production)
user_contexts = {}


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'voice_chatbot_india',
        'version': '1.0.0'
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint for testing.
    
    Request body:
    {
        "message": "What tests do I need?",
        "pregnancy_week": 20,
        "language": "english",  # optional
        "user_id": "user123",   # optional
        "name": "Priya"         # optional
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing required field: message'
            }), 400
        
        user_message = data['message']
        user_id = data.get('user_id', 'default_user')
        
        # Get or create user context
        if user_id not in user_contexts:
            user_contexts[user_id] = {
                'pregnancy_week': data.get('pregnancy_week'),
                'language': data.get('language', 'english'),
                'name': data.get('name', 'there')
            }
        else:
            # Update context with any new info
            if 'pregnancy_week' in data:
                user_contexts[user_id]['pregnancy_week'] = data['pregnancy_week']
            if 'language' in data:
                user_contexts[user_id]['language'] = data['language']
            if 'name' in data:
                user_contexts[user_id]['name'] = data['name']
        
        context = user_contexts[user_id]
        
        # Determine which use case to handle (for now just test_screening)
        # TODO: Add intent classification
        use_case = test_screening
        
        # Get response
        response = use_case.handle(user_message, context)
        
        return jsonify({
            'response': response,
            'context': context,
            'user_id': user_id
        })
        
    except Exception as e:
        app.logger.error(f"Error in /api/chat: {str(e)}")
        return jsonify({
            'error': 'An error occurred processing your request',
            'details': str(e)
        }), 500


@app.route('/api/context', methods=['GET', 'POST'])
def manage_context():
    """
    Get or update user context.
    
    GET: Returns current context for user_id
    POST: Updates context for user_id
    """
    user_id = request.args.get('user_id', 'default_user')
    
    if request.method == 'GET':
        context = user_contexts.get(user_id, {})
        return jsonify({
            'user_id': user_id,
            'context': context
        })
    
    elif request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update or create context
        if user_id not in user_contexts:
            user_contexts[user_id] = {}
        
        user_contexts[user_id].update(data)
        
        return jsonify({
            'user_id': user_id,
            'context': user_contexts[user_id],
            'message': 'Context updated'
        })


@app.route('/api/context/reset', methods=['POST'])
def reset_context():
    """Reset context for a user."""
    user_id = request.args.get('user_id', 'default_user')
    
    if user_id in user_contexts:
        del user_contexts[user_id]
    
    return jsonify({
        'message': f'Context reset for user {user_id}'
    })


@app.route('/voice/incoming', methods=['POST'])
def incoming_call():
    """
    Handle incoming Twilio voice calls.
    This is a placeholder for voice integration.
    """
    # TODO: Implement Twilio voice handling
    from twilio.twiml.voice_response import VoiceResponse
    
    response = VoiceResponse()
    response.say(
        "Welcome to maternal health support. This feature is coming soon.",
        language='en-IN'
    )
    
    return str(response), 200, {'Content-Type': 'text/xml'}


@app.route('/voice/gather', methods=['POST'])
def gather_input():
    """
    Handle user voice input from Twilio.
    This is a placeholder for voice integration.
    """
    # TODO: Implement speech gathering
    from twilio.twiml.voice_response import VoiceResponse
    
    response = VoiceResponse()
    response.say("Voice input handling coming soon.", language='en-IN')
    
    return str(response), 200, {'Content-Type': 'text/xml'}


# Development helper endpoints
@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Quick test endpoint to verify API is working."""
    return jsonify({
        'message': 'API is working!',
        'endpoints': {
            'health': '/health',
            'chat': '/api/chat (POST)',
            'context': '/api/context (GET/POST)',
            'test': '/api/test (GET)'
        }
    })


@app.route('/api/examples', methods=['GET'])
def examples():
    """Return example API requests for testing."""
    return jsonify({
        'examples': [
            {
                'description': 'Ask about tests at 20 weeks',
                'endpoint': '/api/chat',
                'method': 'POST',
                'body': {
                    'message': 'What tests do I need?',
                    'pregnancy_week': 20,
                    'language': 'english',
                    'name': 'Priya'
                }
            },
            {
                'description': 'Ask about ultrasound timing',
                'endpoint': '/api/chat',
                'method': 'POST',
                'body': {
                    'message': 'When should I get my ultrasound?',
                    'pregnancy_week': 18,
                    'language': 'english'
                }
            },
            {
                'description': 'Ask in Hindi',
                'endpoint': '/api/chat',
                'method': 'POST',
                'body': {
                    'message': 'मुझे कौन से टेस्ट करवाने चाहिए?',
                    'pregnancy_week': 30,
                    'language': 'hindi',
                    'name': 'प्रिया'
                }
            },
            {
                'description': 'Get user context',
                'endpoint': '/api/context?user_id=user123',
                'method': 'GET'
            },
            {
                'description': 'Update user context',
                'endpoint': '/api/context?user_id=user123',
                'method': 'POST',
                'body': {
                    'pregnancy_week': 25,
                    'language': 'hindi'
                }
            }
        ]
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"""
    ╔════════════════════════════════════════════════════════╗
    ║   Voice Chatbot India - Maternal Health Support       ║
    ║                                                        ║
    ║   Server starting on http://localhost:{port}            ║
    ║                                                        ║
    ║   Endpoints:                                           ║
    ║   • GET  /health           - Health check              ║
    ║   • POST /api/chat         - Main chat endpoint        ║
    ║   • GET  /api/examples     - See example requests      ║
    ║   • GET  /api/test         - Quick API test            ║
    ║                                                        ║
    ║   Try: curl http://localhost:{port}/api/test            ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)