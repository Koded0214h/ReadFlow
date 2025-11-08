from transformers import pipeline, set_seed
import nltk
import re

class AIStoryTransformer:
    def __init__(self):
        print("🚀 Loading AI story generator...")
        # Try DialoGPT-medium which is better for conversational/story content
        self.story_generator = pipeline(
            "text-generation", 
            model="microsoft/DialoGPT-medium",
            device=-1
        )
        print("✅ AI story generator ready!")
        
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def transform_to_story(self, text, user_interests, reading_level='casual'):
        """Transform plain text into engaging story based on user interests"""
        cleaned_text = self.clean_text(text)
        narrative_prompt = self.create_conversational_prompt(cleaned_text, user_interests, reading_level)
        story_content = self.generate_conversational_content(narrative_prompt)
        return story_content
    
    def clean_text(self, text):
        """Clean and prepare text for AI processing"""
        text = re.sub(r'\s+', ' ', text.strip())
        
        if len(text) > 350:
            sentences = nltk.tokenize.sent_tokenize(text)
            shortened = []
            total_length = 0
            
            for sentence in sentences:
                if total_length + len(sentence) < 350:
                    shortened.append(sentence)
                    total_length += len(sentence)
                else:
                    break
            
            text = ' '.join(shortened)
            if shortened:
                text += "..."
        
        return text
    
    def create_conversational_prompt(self, text, interests, reading_level):
        """Create prompts that work better with DialoGPT"""
        primary_interest = interests[0] if interests else 'general'
        
        # Conversational prompts that work better with DialoGPT
        interest_prompts = {
            'technology': f"Tell me an interesting story about technology innovation: {text}",
            'business': f"Share an inspiring business success story: {text}", 
            'fiction': f"Create a fictional story based on this: {text}",
            'science': f"Tell me about a scientific discovery: {text}",
            'history': f"Share a historical story: {text}",
            'biography': f"Tell me a personal success story: {text}",
            'general': f"Tell me an interesting story: {text}"
        }
        
        base_prompt = interest_prompts.get(primary_interest, interest_prompts['general'])
        
        return base_prompt
    
    def generate_conversational_content(self, prompt):
        """Generate content using DialoGPT with better parameters"""
        try:
            set_seed(42)
            
            generated = self.story_generator(
                prompt,
                max_length=300,
                min_length=100,
                temperature=0.9,  # Higher temperature for more creativity
                do_sample=True,
                num_return_sequences=1,
                pad_token_id=50256,
                repetition_penalty=1.2,
                no_repeat_ngram_size=2
            )[0]['generated_text']
            
            # Extract content after the prompt
            story_content = generated[len(prompt):].strip()
            
            # Enhanced cleaning for DialoGPT output
            story_content = self.clean_dialogue_output(story_content)
            
            return story_content if story_content and len(story_content) > 80 else self.create_smart_fallback(prompt)
            
        except Exception as e:
            print(f"🤖 AI generation failed: {e}")
            return self.create_smart_fallback(prompt)
    
    def clean_dialogue_output(self, text):
        """Clean DialoGPT-specific output patterns"""
        # Remove common dialogue markers if they appear
        text = re.sub(r'^(User|Bot|Human|AI):\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(Learn more|Click here|Follow|Sign up|Subscribe)\b.*$', '', text, flags=re.IGNORECASE)
        text = re.sub(r'www\..*?(?=\s|$)', '', text)
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'@\w+', '', text)  # Remove Twitter handles
        
        # Normalize and clean
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Ensure proper ending
        if text and not text[-1] in '.!?"\'':
            text += '.'
        
        return text
    
    def create_smart_fallback(self, prompt):
        """Create intelligent fallback content"""
        # Extract the core content using multiple methods
        content_match = re.search(r':\s*(.*?)$', prompt)
        if not content_match:
            content_match = re.search(r'story(?:.*?):\s*(.*?)$', prompt)
        
        if content_match:
            original_text = content_match.group(1).strip()
            
            # Create context-aware fallbacks
            if 'technology' in prompt.lower():
                return f"""In the world of technological advancement, {original_text} represents a significant milestone. This breakthrough demonstrates how innovation can transform industries and create new possibilities. The team behind this achievement combined technical expertise with strategic vision to create something truly remarkable. As technology continues to evolve, developments like this pave the way for future innovations that will shape our digital landscape for years to come."""
            
            elif 'business' in prompt.lower():
                return f"""In the competitive business world, {original_text} stands as a testament to strategic execution and market understanding. This success story highlights the importance of innovation, timing, and customer focus in today's dynamic business environment. The achievement reflects careful planning and the ability to adapt to changing market conditions while maintaining a clear vision for growth and impact."""
            
            elif 'science' in prompt.lower():
                return f"""In scientific research, {original_text} represents an important discovery with far-reaching implications. This breakthrough came through dedicated research, collaboration, and persistent effort to solve complex challenges. The findings contribute valuable knowledge to the scientific community and open new avenues for future exploration and application in addressing real-world problems."""
            
            elif 'history' in prompt.lower():
                return f"""Throughout history, {original_text} marked a pivotal moment in human development. This historical achievement demonstrates human ingenuity and the capacity for innovation across generations. Understanding these historical developments helps us appreciate the foundations of modern society and the continuous thread of progress that connects past achievements with present possibilities."""
            
            else:
                return f"""This story about {original_text} represents an important achievement worth celebrating. The details reveal a journey of dedication, innovation, and strategic thinking that led to meaningful outcomes. Such accomplishments often combine multiple factors including timing, expertise, and the ability to see opportunities where others see challenges."""
        
        return """Our storytelling AI is currently preparing an engaging narrative based on your content. The final story will provide context, meaning, and an engaging perspective that makes the information more accessible and memorable. Please check back shortly for the transformed content."""