"""
Use Case: What tests do I need? (DEMO)
Handles inquiries about required medical tests during pregnancy.
"""

import os
from anthropic import Anthropic
from ..knowledge.test_schedules import get_tests_for_week, get_trimester_from_week

class TestScreeningUseCase:
    def __init__(self):
        self.name = "test_screening"
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
    def handle(self, user_input, context):
        """
        Handle test inquiry based on pregnancy stage.
        
        Args:
            user_input (str): What the user said/asked
            context (dict): User context including pregnancy_week, language, etc.
        
        Returns:
            str: Natural language response about required tests
        """
        # Get pregnancy week from context
        pregnancy_week = context.get('pregnancy_week')
        language = context.get('language', 'english')
        user_name = context.get('name', 'there')
        
        if not pregnancy_week:
            return self._ask_for_pregnancy_week(language)
        
        # Get the test data
        test_data = get_tests_for_week(pregnancy_week)
        trimester = get_trimester_from_week(pregnancy_week)
        
        # Create a prompt for Claude with the medical data
        response = self._generate_response(
            user_input=user_input,
            test_data=test_data,
            pregnancy_week=pregnancy_week,
            trimester=trimester,
            language=language,
            user_name=user_name
        )
        
        return response
    
    def _generate_response(self, user_input, test_data, pregnancy_week, trimester, language, user_name):
        """
        Use Claude to generate a natural, empathetic response about tests.
        """
        # Format the test data for Claude
        tests_info = self._format_tests_for_prompt(test_data['tests'])
        
        # Create system prompt
        system_prompt = f"""You are a helpful, warm maternal health assistant for pregnant women in India.
You provide clear, accurate information about prenatal tests in a caring, reassuring way.

Guidelines:
- Speak in simple, easy-to-understand language
- Be warm and encouraging
- Explain WHY each test is important (not just what it is)
- Address the woman by name when appropriate
- If speaking in Hindi, use simple Hindi that's easy to understand
- Keep responses concise but complete (2-3 paragraphs max for voice)
- Focus on what's most important for their current stage

Current language: {language}
"""

        # Create user prompt with context
        user_prompt = f"""The pregnant woman (name: {user_name}) is at {pregnancy_week} weeks of pregnancy ({trimester}).

She asked: "{user_input}"

Here are the tests recommended for her current stage:

{tests_info}

Please provide a helpful, natural response that:
1. Addresses her question directly
2. Explains the 2-3 most important tests for her current week
3. Briefly mentions why each test matters
4. Is warm and reassuring in tone
5. Responds in {language}

Keep it conversational and suitable for a voice conversation (not too long)."""

        # Call Claude API
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return self._fallback_response(test_data, language)
    
    def _format_tests_for_prompt(self, tests):
        """Format test data into a readable string for Claude."""
        formatted = []
        for test in tests:
            test_str = f"""
Test: {test['name']}
- Timing: {test['timing']}
- Why: {test['why']}
- Normal Range: {test.get('normal_range', 'N/A')}
"""
            if 'hindi_name' in test:
                test_str += f"- Hindi Name: {test['hindi_name']}\n"
            formatted.append(test_str)
        
        return "\n".join(formatted)
    
    def _ask_for_pregnancy_week(self, language):
        """Ask user for their pregnancy week if not provided."""
        if language == 'hindi':
            return "आप गर्भावस्था के कितने सप्ताह में हैं? यह जानकर मैं आपको सही जानकारी दे सकूंगी।"
        else:
            return "To help you better, could you tell me how many weeks pregnant you are?"
    
    def _fallback_response(self, test_data, language):
        """Fallback response if Claude API fails."""
        tests = test_data['tests']
        
        if language == 'hindi':
            response = f"आपके लिए {len(tests)} महत्वपूर्ण परीक्षण हैं:\n"
            for i, test in enumerate(tests[:3], 1):  # Top 3 tests
                response += f"{i}. {test.get('hindi_name', test['name'])} - {test['timing']}\n"
        else:
            response = f"Here are the important tests for you:\n"
            for i, test in enumerate(tests[:3], 1):  # Top 3 tests
                response += f"{i}. {test['name']} - {test['timing']}\n"
        
        return response


# Helper function for quick testing
def quick_test(user_question, pregnancy_week, language='english'):
    """
    Quick test function for development.
    
    Usage:
        response = quick_test("What tests do I need?", 20)
    """
    use_case = TestScreeningUseCase()
    context = {
        'pregnancy_week': pregnancy_week,
        'language': language,
        'name': 'Priya'
    }
    return use_case.handle(user_question, context)


# Example usage and testing
if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    print("Testing TestScreeningUseCase\n")
    print("=" * 60)
    
    # Test scenarios
    test_cases = [
        {
            "question": "What tests do I need right now?",
            "week": 10,
            "language": "english"
        },
        {
            "question": "When should I get my ultrasound?",
            "week": 20,
            "language": "english"
        },
        {
            "question": "मुझे कौन से टेस्ट करवाने चाहिए?",
            "week": 30,
            "language": "hindi"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Week: {test['week']}")
        print(f"Question: {test['question']}")
        print(f"Language: {test['language']}")
        print("-" * 60)
        
        try:
            response = quick_test(
                test['question'],
                test['week'],
                test['language']
            )
            print(f"Response:\n{response}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("=" * 60)
    
    # Interactive test
    print("\n\nInteractive Test (press Ctrl+C to exit):")
    print("Enter pregnancy week and question to test the system")
    
    try:
        while True:
            week_input = input("\nPregnancy week (or 'quit'): ")
            if week_input.lower() == 'quit':
                break
            
            try:
                week = int(week_input)
                if week < 1 or week > 40:
                    print("Please enter a week between 1 and 40")
                    continue
            except ValueError:
                print("Please enter a valid number")
                continue
            
            question = input("Question: ")
            language = input("Language (english/hindi): ").lower()
            
            if language not in ['english', 'hindi']:
                language = 'english'
            
            print("\nGenerating response...")
            response = quick_test(question, week, language)
            print(f"\nResponse:\n{response}\n")
            
    except KeyboardInterrupt:
        print("\n\nGoodbye!")