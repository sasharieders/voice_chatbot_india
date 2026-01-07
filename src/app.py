"""
Flask application for Voice Chatbot India - Maternal Health Support
Main API endpoints for testing and voice integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.use_cases.test_screening import TestScreeningUseCase
from src.voice.twilio_handler import TwilioVoiceHandler
from twilio.twiml.voice_response import VoiceResponse

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize use cases and handlers
test_screening = TestScreeningUseCase()
twilio_voice = TwilioVoiceHandler()

# In-memory context storage (for demo - use database in production)
user_contexts = {}
call_contexts = {}  # Track context per call


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


# ============================================================================
# VOICE ENDPOINTS (Twilio Webhooks)
# ============================================================================

@app.route('/voice/incoming', methods=['POST', 'GET'])
def voice_incoming():
    """
    Handle incoming Twilio voice calls.
    This is the entry point when someone calls your Twilio number.
    """
    try:
        language = request.values.get('language', 'english')
        call_sid = request.values.get('CallSid', 'unknown')
        
        # Initialize context for this call
        call_contexts[call_sid] = {
            'pregnancy_week': None,  # Will ask user or default to 20
            'language': language,
            'name': 'there',
            'messages': []
        }
        
        app.logger.info(f"Incoming call: {call_sid}, language: {language}")
        
        return twilio_voice.welcome_message(language), 200, {'Content-Type': 'text/xml'}
        
    except Exception as e:
        app.logger.error(f"Error in /voice/incoming: {str(e)}")
        return twilio_voice.handle_error(str(e)), 200, {'Content-Type': 'text/xml'}


@app.route('/voice/process', methods=['POST'])
def voice_process():
    """
    Process speech input from user.
    Called after user speaks in response to prompts.
    """
    try:
        speech_result = request.values.get('SpeechResult', '')
        confidence = float(request.values.get('Confidence', 0))
        call_sid = request.values.get('CallSid', 'unknown')
        
        app.logger.info(f"Speech received: '{speech_result}' (confidence: {confidence})")
        
        # Get or create context for this call
        if call_sid not in call_contexts:
            call_contexts[call_sid] = {
                'pregnancy_week': 20,  # Default
                'language': 'english',
                'name': 'there',
                'messages': []
            }
        
        context = call_contexts[call_sid]
        language = context['language']
        
        if not speech_result or confidence < 0.5:
            # Low confidence or no speech
            return twilio_voice._ask_to_repeat(language), 200, {'Content-Type': 'text/xml'}
        
        # Add to conversation history
        context['messages'].append({
            'role': 'user',
            'content': speech_result
        })
        
        # Get chatbot response using test screening use case
        chatbot_response = test_screening.handle(speech_result, context)
        
        # Add to conversation history
        context['messages'].append({
            'role': 'assistant',
            'content': chatbot_response
        })
        
        app.logger.info(f"Chatbot response: {chatbot_response[:100]}...")
        
        return twilio_voice.generate_response(chatbot_response, language), 200, {'Content-Type': 'text/xml'}
        
    except Exception as e:
        app.logger.error(f"Error in /voice/process: {str(e)}")
        language = call_contexts.get(call_sid, {}).get('language', 'english')
        return twilio_voice.handle_error(str(e), language), 200, {'Content-Type': 'text/xml'}


@app.route('/voice/language', methods=['POST', 'GET'])
def voice_language():
    """
    Language selection menu.
    Allows user to choose between English and Hindi.
    """
    try:
        return twilio_voice.language_selection(), 200, {'Content-Type': 'text/xml'}
    except Exception as e:
        app.logger.error(f"Error in /voice/language: {str(e)}")
        return twilio_voice.handle_error(str(e)), 200, {'Content-Type': 'text/xml'}


@app.route('/voice/set-language', methods=['POST'])
def voice_set_language():
    """
    Set language based on keypad input.
    Called after user presses 1 (English) or 2 (Hindi).
    """
    try:
        digits = request.values.get('Digits', '1')
        call_sid = request.values.get('CallSid', 'unknown')
        language = 'hindi' if digits == '2' else 'english'
        
        # Update call context
        if call_sid in call_contexts:
            call_contexts[call_sid]['language'] = language
        
        app.logger.info(f"Language set to: {language} for call {call_sid}")
        
        response = VoiceResponse()
        response.redirect(f'/voice/incoming?language={language}')
        return str(response), 200, {'Content-Type': 'text/xml'}
        
    except Exception as e:
        app.logger.error(f"Error in /voice/set-language: {str(e)}")
        return twilio_voice.handle_error(str(e)), 200, {'Content-Type': 'text/xml'}


@app.route('/voice/continue', methods=['POST'])
def voice_continue():
    """
    Continue conversation flow.
    """
    try:
        call_sid = request.values.get('CallSid', 'unknown')
        context = call_contexts.get(call_sid, {'language': 'english'})
        language = context['language']
        
        # For now, just end the call gracefully
        response = VoiceResponse()
        if language == 'hindi':
            response.say("धन्यवाद। अलविदा।", language='hi-IN')
        else:
            response.say("Thank you for calling. Goodbye!", language='en-IN')
        response.hangup()
        
        return str(response), 200, {'Content-Type': 'text/xml'}
        
    except Exception as e:
        app.logger.error(f"Error in /voice/continue: {str(e)}")
        return twilio_voice.handle_error(str(e)), 200, {'Content-Type': 'text/xml'}


# ============================================================================
# CONTEXT MANAGEMENT ENDPOINTS
# ============================================================================

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


# ============================================================================
# DEVELOPMENT HELPER ENDPOINTS
# ============================================================================

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Quick test endpoint to verify API is working."""
    return jsonify({
        'message': 'API is working!',
        'endpoints': {
            'health': '/health',
            'chat': '/api/chat (POST)',
            'context': '/api/context (GET/POST)',
            'voice_incoming': '/voice/incoming (POST)',
            'voice_process': '/voice/process (POST)',
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
    ║   API Endpoints:                                       ║
    ║   • GET  /health           - Health check              ║
    ║   • POST /api/chat         - Text chat                 ║
    ║   • GET  /api/examples     - Example requests          ║
    ║                                                        ║
    ║   Voice Endpoints (Twilio):                            ║
    ║   • POST /voice/incoming   - Incoming calls            ║
    ║   • POST /voice/process    - Process speech            ║
    ║   • POST /voice/language   - Language selection        ║
    ║                                                        ║
    ║   Next: Set up ngrok and configure Twilio webhook     ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)