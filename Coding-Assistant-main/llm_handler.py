from langchain_community.llms import Ollama
from typing import List
import os

class LLMHandler:
    def __init__(self, model: str = "llama3.1:latest", use_gemini: bool = False, api_key: str = None):
        self.use_gemini = use_gemini
        self.model_name = model
        
        if use_gemini and api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.llm = genai.GenerativeModel('gemini-2.0-flash-exp')
                self.gemini_model = "gemini-2.0-flash-exp"
                self.is_gemini = True
            except ImportError:
                raise ImportError("Please install google-generativeai: pip install google-generativeai")
            except Exception as e:
                print(f"Error initializing Gemini: {e}")
                # Fallback to Ollama
                self.llm = Ollama(model=model, temperature=0.7)
                self.is_gemini = False
        else:
            self.llm = Ollama(model=model, temperature=0.7)
            self.is_gemini = False
            
        self.system_prompt = """You are a chill tech bro coding assistant who's really good at solving problems. You're knowledgeable, confident, and make coding feel easy.

Your vibe:
- Talk like a friendly developer who's been there, done that
- Use casual language but stay professional
- Drop occasional tech terms naturally (like "ship it", "refactor", "optimize", "scale")
- Be encouraging and make the user feel like they got this
- Keep it real - if something's tricky, say so, but always have a solution

When helping:
- If someone greets you, greet them back casually and ask what they're building
- Answer coding questions directly with clear explanations
- Only write code when they ask you to write, create, or generate something
- Use markdown code blocks with language tags
- Explain WHY your solution works, not just HOW
- Give pro tips when relevant
- Be concise but thorough

Examples of your style:
- "Yo! What are we building today?"
- "Alright, here's the deal with that bug..."
- "Easy fix! Just need to..."
- "Pro tip: you could also..."
- "Let's ship this!"

Stay helpful, stay cool, and help them write better code."""
    
    def generate_response(self, user_query: str, context: str = "", 
                         chat_history: List = None) -> str:
        """Generate AI response with optional context and history"""
        if self.is_gemini:
            # Gemini API format - Simple and direct
            full_prompt = self.system_prompt + "\n\n"
            
            if chat_history and len(chat_history) > 0:
                # Only include last 3 exchanges
                recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
                for msg in recent_history:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    full_prompt += f"{role}: {msg['content']}\n"
            
            full_prompt += f"User: {user_query}\nAssistant:"
            
            response = self.llm.generate_content(full_prompt)
            return response.text
        else:
            # Ollama format - Simple and direct
            full_prompt = self.system_prompt + "\n\n"
            
            if chat_history and len(chat_history) > 0:
                # Only include last 3 exchanges
                recent_history = chat_history[-6:] if len(chat_history) > 6 else chat_history
                for msg in recent_history:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    full_prompt += f"{role}: {msg['content']}\n"
            
            full_prompt += f"User: {user_query}\nAssistant:"
            
            response = self.llm.invoke(full_prompt)
            return response
    
    def generate_code(self, prompt: str, language: str) -> str:
        """Generate code based on description"""
        full_prompt = f"""You are a code generation expert. Generate clean, efficient, and well-commented {language} code.

{prompt}

Provide ONLY the code without explanations. Make it production-ready."""
        
        if self.is_gemini:
            response = self.llm.generate_content(full_prompt)
            return response.text
        else:
            return self.llm.invoke(full_prompt)
    
    def fix_bug(self, prompt: str, language: str) -> str:
        """Fix bugs in code"""
        full_prompt = f"""You are a debugging expert. Analyze and fix the bugs in the provided {language} code.

{prompt}

Provide ONLY the fixed code without explanations."""
        
        if self.is_gemini:
            response = self.llm.generate_content(full_prompt)
            return response.text
        else:
            return self.llm.invoke(full_prompt)
    
    def analyze_quality(self, prompt: str) -> str:
        """Analyze code quality"""
        full_prompt = f"""You are a code quality expert. Provide a detailed analysis covering:
1. Issues found (with severity: Critical/High/Medium/Low)
2. Specific recommendations for improvement
3. Code examples for fixes

{prompt}"""
        
        if self.is_gemini:
            response = self.llm.generate_content(full_prompt)
            return response.text
        else:
            return self.llm.invoke(full_prompt)
    
    def refactor_code(self, prompt: str, language: str) -> str:
        """Refactor code"""
        full_prompt = f"""You are a refactoring expert. Refactor the provided {language} code according to the specified goals.

{prompt}

Provide ONLY the refactored code without explanations."""
        
        if self.is_gemini:
            response = self.llm.generate_content(full_prompt)
            return response.text
        else:
            return self.llm.invoke(full_prompt)
    
    def generate_docs(self, prompt: str, language: str) -> str:
        """Generate documentation"""
        full_prompt = f"""You are a technical documentation expert. Generate comprehensive documentation for the {language} code.

{prompt}"""
        
        if self.is_gemini:
            response = self.llm.generate_content(full_prompt)
            return response.text
        else:
            return self.llm.invoke(full_prompt)
    
    def generate_tests(self, prompt: str, language: str) -> str:
        """Generate unit tests"""
        full_prompt = f"""You are a test automation expert. Generate comprehensive unit tests for the {language} code.

{prompt}

Provide ONLY the test code without explanations."""
        
        if self.is_gemini:
            response = self.llm.generate_content(full_prompt)
            return response.text
        else:
            return self.llm.invoke(full_prompt)
    
    def explain_code(self, prompt: str) -> str:
        """Explain code"""
        full_prompt = f"""You are a code educator. Provide a clear, structured explanation of the code.

{prompt}

Structure your explanation with:
1. Overview of what the code does
2. Step-by-step breakdown
3. Key concepts and patterns used
4. Potential improvements or considerations"""
        
        if self.is_gemini:
            response = self.llm.generate_content(full_prompt)
            return response.text
        else:
            return self.llm.invoke(full_prompt)
