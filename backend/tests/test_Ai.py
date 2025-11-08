import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from documents.ai_processor import AIStoryTransformer

def test_ai_story():
    ai = AIStoryTransformer()
    
    test_cases = [
        {
            "text": "The technology company achieved remarkable 30% growth last quarter through strategic market expansion into emerging economies and the launch of innovative AI-powered products that revolutionized customer experience.",
            "interests": ["technology"],
            "level": "detailed"
        },
        {
            "text": "Researchers at the university discovered a groundbreaking carbon capture method using advanced nanomaterials that can absorb CO2 at unprecedented rates, potentially offering a scalable solution to climate change challenges worldwide.",
            "interests": ["science"],
            "level": "detailed" 
        },
        {
            "text": "Ancient Mesopotamian civilizations developed sophisticated irrigation systems around 6000 BCE that enabled agricultural surplus, supporting the growth of large urban populations and laying the foundation for modern civilization through advanced water management techniques.",
            "interests": ["history"],
            "level": "detailed"
        },
        {
            "text": "The startup secured $50 million in Series B funding after demonstrating 400% user growth, leveraging their unique platform that connects freelance professionals with enterprise clients through an AI-matching algorithm.",
            "interests": ["business"],
            "level": "casual"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📖 TEST CASE {i}:")
        print(f"Interest: {case['interests'][0].upper()}")
        print(f"Level: {case['level'].upper()}")
        print(f"\nOriginal: {case['text']}")
        print(f"\n{'='*80}")
        
        result = ai.transform_to_story(
            case['text'],
            case['interests'],
            case['level']
        )
        
        print(f"\nAI STORY:\n{result}")
        print(f"\nStory Length: {len(result)} characters")
        print(f"{'='*80}")

if __name__ == "__main__":
    test_ai_story()