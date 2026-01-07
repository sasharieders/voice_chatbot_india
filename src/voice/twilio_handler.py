"""
Twilio voice call handler for maternal health chatbot.
Uses Twilio's built-in speech recognition and TTS.
"""

from twilio.twiml.voice_response import VoiceResponse, Gather
import os


class TwilioVoiceHandler:
    def __init__(self):
        self.default_language = 'en-IN'  # English (India)
        self.hindi_language = 'hi-IN'     # Hindi (India)
        
    def welcome_message(self, language='english'):
        """Generate welcome message for incoming call."""
        response = VoiceResponse()
        
        if language == 'hindi':
            message = """
            स्वागत है। मैं आपकी गर्भावस्था स्वास्थ्य सहायक हूं। 
            मैं आपको एएनसी परीक्षणों और स्वास्थ्य जानकारी के बारे में बता सकती हूं।
            कृपया अपना सवाल पूछें।
            """
            voice_lang = self.hindi_language
        else:
            message = """
            Welcome to Maternal Health Support. 
            I can help you with information about pregnancy tests and antenatal care.
            Please ask your question after the beep.
            """
            voice_lang = self.default_language
        
        # Gather user's speech input
        gather = Gather(
            input='speech',
            action='/voice/process',
            method='POST',
            language=voice_lang,
            speech_timeout='auto',
            hints='pregnancy, tests, ultrasound, blood test, ANC, antenatal'
        )
        
        gather.say(message, language=voice_lang)
        response.append(gather)
        
        # If no input, repeat
        response.say("I didn't hear anything. Please call back.", language=voice_lang)
        
        return str(response)
    
    def process_speech(self, speech_result, confidence, language='english'):
        """
        Process speech input from user.
        
        Args:
            speech_result (str): Transcribed speech from Twilio
            confidence (float): Confidence score from Twilio
            language (str): 'english' or 'hindi'
        
        Returns:
            str: TwiML response
        """
        response = VoiceResponse()
        
        if not speech_result or confidence < 0.5:
            # Low confidence or no speech
            return self._ask_to_repeat(language)
        
        # TODO: This will be replaced with actual chatbot logic
        # For now, just acknowledge
        voice_lang = self.hindi_language if language == 'hindi' else self.default_language
        
        response.say(
            f"I heard: {speech_result}. Processing your question...",
            language=voice_lang
        )
        
        # Redirect to continue conversation
        response.redirect('/voice/continue')
        
        return str(response)
    
    def generate_response(self, chatbot_response, language='english'):
        """
        Convert chatbot text response to speech.
        
        Args:
            chatbot_response (str): Text response from chatbot
            language (str): 'english' or 'hindi'
        
        Returns:
            str: TwiML response
        """
        response = VoiceResponse()
        voice_lang = self.hindi_language if language == 'hindi' else self.default_language
        
        # Say the response
        response.say(chatbot_response, language=voice_lang, voice='Polly.Aditi')
        
        # Ask if they want to continue
        gather = Gather(
            input='speech',
            action='/voice/process',
            method='POST',
            language=voice_lang,
            speech_timeout='auto',
            num_digits=1
        )
        
        if language == 'hindi':
            gather.say("क्या आपका कोई और सवाल है?", language=voice_lang)
        else:
            gather.say("Do you have another question?", language=voice_lang)
        
        response.append(gather)
        
        # End call if no response
        if language == 'hindi':
            response.say("धन्यवाद। अलविदा।", language=voice_lang)
        else:
            response.say("Thank you for calling. Goodbye!", language=voice_lang)
        
        response.hangup()
        
        return str(response)
    
    def _ask_to_repeat(self, language='english'):
        """Ask user to repeat their question."""
        response = VoiceResponse()
        voice_lang = self.hindi_language if language == 'hindi' else self.default_language
        
        gather = Gather(
            input='speech',
            action='/voice/process',
            method='POST',
            language=voice_lang,
            speech_timeout='auto'
        )
        
        if language == 'hindi':
            gather.say("मुझे सुनाई नहीं दिया। कृपया दोबारा कहें।", language=voice_lang)
        else:
            gather.say("I'm sorry, I didn't catch that. Please repeat your question.", language=voice_lang)
        
        response.append(gather)
        response.say("Goodbye.", language=voice_lang)
        response.hangup()
        
        return str(response)
    
    def handle_error(self, error_message, language='english'):
        """Handle errors during call."""
        response = VoiceResponse()
        voice_lang = self.hindi_language if language == 'hindi' else self.default_language
        
        if language == 'hindi':
            message = "क्षमा करें, कुछ गलत हो गया। कृपया बाद में फिर से कॉल करें।"
        else:
            message = "I'm sorry, something went wrong. Please try calling again later."
        
        response.say(message, language=voice_lang)
        response.hangup()
        
        return str(response)
    
    def language_selection(self):
        """Let user select their language preference."""
        response = VoiceResponse()
        
        gather = Gather(
            input='dtmf',  # Use keypad
            action='/voice/set-language',
            method='POST',
            num_digits=1,
            timeout=5
        )
        
        gather.say(
            "Press 1 for English. Press 2 for Hindi. "
            "अंग्रेजी के लिए 1 दबाएं। हिंदी के लिए 2 दबाएं।",
            language=self.default_language
        )
        
        response.append(gather)
        
        # Default to English if no input
        response.say("Continuing in English.", language=self.default_language)
        response.redirect('/voice/incoming?language=english')
        
        return str(response)


# Quick testing
if __name__ == "__main__":
    handler = TwilioVoiceHandler()
    
    print("Testing Twilio Voice Handler\n")
    print("=" * 60)
    
    # Test 1: Welcome message
    print("\n1. Welcome Message (English):")
    print(handler.welcome_message('english'))
    
    # Test 2: Welcome message in Hindi
    print("\n2. Welcome Message (Hindi):")
    print(handler.welcome_message('hindi'))
    
    # Test 3: Generate response
    print("\n3. Sample Response:")
    chatbot_text = "At 20 weeks, you should get an ultrasound scan to check your baby's development."
    print(handler.generate_response(chatbot_text, 'english'))
    
    print("\n" + "=" * 60)