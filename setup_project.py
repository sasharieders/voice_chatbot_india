#!/usr/bin/env python3
"""
Setup script to create the voice_chatbot_india project structure.
Run this from inside your voice_chatbot_india directory.

Usage: python setup_project.py
"""

import os
from pathlib import Path

def create_file(path):
    """Create an empty file."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).touch()
    print(f"✓ Created: {path}")

def create_dir(path):
    """Create a directory."""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created: {path}/")

# All files to create (empty)
files = [
    # Root files
    'README.md',
    '.env.example',
    '.gitignore',
    'requirements.txt',
    'package.json',
    'Dockerfile',
    'docker-compose.yml',
    
    # Documentation
    'docs/architecture.md',
    'docs/use_cases.md',
    'docs/api_docs.md',
    'docs/demo_setup.md',
    
    # Main app
    'src/app.py',
    
    # Demo
    'src/demo/__init__.py',
    'src/demo/demo_handler.py',
    'src/demo/demo_data.py',
    
    # Voice
    'src/voice/__init__.py',
    'src/voice/call_handler.py',
    'src/voice/speech_to_text.py',
    'src/voice/text_to_speech.py',
    'src/voice/audio_utils.py',
    
    # Conversation
    'src/conversation/__init__.py',
    'src/conversation/intent_classifier.py',
    'src/conversation/dialogue_manager.py',
    'src/conversation/context_manager.py',
    'src/conversation/response_generator.py',
    
    # Use Cases
    'src/use_cases/__init__.py',
    'src/use_cases/base_use_case.py',
    'src/use_cases/anc1_facility.py',
    'src/use_cases/anc1_timing.py',
    'src/use_cases/facility_hours.py',
    'src/use_cases/visit_cadence.py',
    'src/use_cases/test_screening.py',
    'src/use_cases/results_understanding.py',
    'src/use_cases/supplement_adherence.py',
    'src/use_cases/facility_selection.py',
    
    # Knowledge
    'src/knowledge/__init__.py',
    'src/knowledge/anc_guidelines.py',
    'src/knowledge/facility_finder.py',
    'src/knowledge/test_schedules.py',
    'src/knowledge/supplement_info.py',
    'src/knowledge/risk_assessment.py',
    
    # LLM
    'src/llm/__init__.py',
    'src/llm/openai_client.py',
    'src/llm/prompts.py',
    'src/llm/function_calling.py',
    'src/llm/rag_engine.py',
    
    # Data
    'src/data/__init__.py',
    'src/data/facilities.json',
    'src/data/anc_schedule.json',
    'src/data/test_protocols.json',
    'src/data/supplements.json',
    'src/data/demo/sample_facilities.json',
    'src/data/demo/sample_user.json',
    'src/data/translations/hindi.json',
    'src/data/translations/english.json',
    
    # Database
    'src/database/__init__.py',
    'src/database/models.py',
    'src/database/queries.py',
    'src/database/init_db.py',
    
    # Integrations
    'src/integrations/__init__.py',
    'src/integrations/twilio_client.py',
    'src/integrations/twilio_webhooks.py',
    'src/integrations/sms_service.py',
    
    # Analytics
    'src/analytics/__init__.py',
    'src/analytics/call_logger.py',
    'src/analytics/metrics.py',
    
    # Utils
    'src/utils/__init__.py',
    'src/utils/validators.py',
    'src/utils/formatters.py',
    'src/utils/language_detector.py',
    'src/utils/location_utils.py',
    'src/utils/config.py',
    
    # Tests
    'tests/unit/test_use_cases.py',
    'tests/unit/test_openai_client.py',
    'tests/unit/test_knowledge.py',
    'tests/integration/test_demo_flow.py',
    'tests/integration/test_twilio_integration.py',
    'tests/fixtures/sample_calls.json',
    
    # Scripts
    'scripts/setup_db.py',
    'scripts/load_demo_data.py',
    'scripts/test_openai.py',
    'scripts/test_twilio.py',
    'scripts/start_demo.sh',
    'scripts/ngrok_setup.sh',
    
    # Config
    'config/config.yaml',
    'config/prompts/system_prompt.txt',
    'config/prompts/anc1_facility.txt',
    'config/prompts/anc1_timing.txt',
    'config/prompts/facility_hours.txt',
    'config/prompts/visit_cadence.txt',
    'config/prompts/test_screening.txt',
    'config/prompts/results_understanding.txt',
    'config/prompts/supplement_adherence.txt',
    'config/prompts/facility_selection.txt',
    'config/functions/facility_search.json',
    'config/functions/appointment_check.json',
    'config/functions/test_lookup.json',
    
    # Notebooks
    'notebooks/test_openai_prompts.ipynb',
    'notebooks/demo_walkthrough.ipynb',
    
    # Demo frontend (optional)
    'demo_frontend/index.html',
    'demo_frontend/script.js',
    'demo_frontend/styles.css',
]

def main():
    print("Creating voice_chatbot_india project structure...\n")
    
    for file_path in files:
        create_file(file_path)
    
    print(f"\n✅ Created {len(files)} files!")
    print("\nProject structure is ready. Next steps:")
    print("1. Add your API keys to .env.example and rename to .env")
    print("2. Fill in requirements.txt with dependencies")
    print("3. Start coding! Focus on src/use_cases/test_screening.py for demo")

if __name__ == '__main__':
    main()