






# import google.generativeai as genai
# from app.config import settings
# from typing import List
# import logging

# logger = logging.getLogger(__name__)

# class AIService:
#     def __init__(self):
#         """Initialize Gemini AI with real API"""
#         if not settings.GEMINI_API_KEY:
#             raise ValueError("GEMINI_API_KEY is required")
        
#         genai.configure(api_key=settings.GEMINI_API_KEY)
#         self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
#         logger.info(f"✅ Gemini AI initialized with model: {settings.GEMINI_MODEL}")
    
#     async def generate_recommendation_message(
#         self, 
#         trigger_category: str, 
#         recommendations: List[str],
#         user_context: str = ""
#     ) -> str:
#         """
#         Generate motivational message using Gemini AI
        
#         Args:
#             trigger_category: Detected unhealthy category
#             recommendations: List of healthy alternatives
#             user_context: Optional user context
        
#         Returns:
#             AI-generated motivational message
#         """
#         try:
#             prompt = f"""
#             You are a friendly health coach. A user is near a {trigger_category}.
            
#             Available healthy alternatives nearby:
#             {', '.join(recommendations) if recommendations else 'Various healthy options'}
            
#             Context: {user_context if user_context else 'General time of day'}
            
#             Write a short, positive, and motivational message (1-2 sentences) 
#             encouraging the user to choose a healthy alternative.
#             Make it feel personal, supportive, and actionable.
#             """
            
#             logger.info(f"🤖 Generating AI message for: {trigger_category}")
            
#             # Generate content
#             response = await self.model.generate_content_async(prompt)
#             message = response.text.strip()
            
#             logger.debug(f"AI Response: {message}")
#             return message
            
#         except Exception as e:
#             logger.error(f"Gemini AI error: {e}")
#             # Fallback to simple message if AI fails
#             fallback = f"Consider trying {recommendations[0] if recommendations else 'a healthy option'} instead of {trigger_category}!"
#             return fallback

# # Singleton instance
# ai_service = AIService()


# import google.generativeai as genai
# from app.config import settings
# from typing import List, Dict, Optional
# import logging

# logger = logging.getLogger(__name__)

# class AIService:
#     def __init__(self):
#         """Initialize Gemini AI with real API"""
#         if not settings.GEMINI_API_KEY:
#             raise ValueError("GEMINI_API_KEY is required")
        
#         genai.configure(api_key=settings.GEMINI_API_KEY)
#         self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
#         logger.info(f"✅ Gemini AI initialized with model: {settings.GEMINI_MODEL}")
    
#     async def generate_recommendation_message(
#         self, 
#         trigger_place_name: str,
#         trigger_category: str, 
#         recommendations: List[str],
#         user_context: str = ""
#     ) -> str:
#         """
#         Generate motivational message using Gemini AI
#         """
#         try:
#             prompt = f"""
#             You are a friendly health coach. A user is near {trigger_place_name} (a {trigger_category}).
            
#             Available healthy alternatives nearby:
#             {', '.join(recommendations) if recommendations else 'Various healthy options'}
            
#             Context: {user_context if user_context else 'General time of day'}
            
#             Write a short, positive, and motivational message (1-2 sentences) 
#             encouraging the user to choose a healthy alternative.
#             Make it feel personal, supportive, and actionable.
#             Include the specific place name {trigger_place_name} in your message.
#             """
            
#             logger.info(f"🤖 Generating AI message for: {trigger_place_name} ({trigger_category})")
            
#             response = await self.model.generate_content_async(prompt)
#             message = response.text.strip()
            
#             logger.debug(f"AI Response: {message}")
#             return message
            
#         except Exception as e:
#             logger.error(f"Gemini AI error: {e}")
#             fallback = f"Consider trying {recommendations[0] if recommendations else 'a healthy option'} instead of {trigger_place_name}!"
#             return fallback
    
#     async def generate_recommendation_with_specific_locations(
#         self,
#         trigger_place_name: str,
#         trigger_category: str,
#         specific_alternatives: List[Dict],
#         user_context: str = ""
#     ) -> str:
#         """
#         Generate motivational message WITH specific location suggestions
#         """
#         try:
#             # Format alternatives for prompt
#             alternatives_text = self._format_alternatives_for_ai(specific_alternatives)
            
#             prompt = f"""
#             You are a friendly health coach in Pakistan. 
            
#             Current Situation:
#             - User is near: {trigger_place_name} (a {trigger_category})
            
#             ACTUAL healthy alternatives available NEARBY:
#             {alternatives_text}
            
#             User Context: {user_context if user_context else 'Looking for healthy options'}
            
#             Write a SHORT, POSITIVE, and ACTIONABLE message (2-3 sentences MAX):
#             1. Mention {trigger_place_name} that user should avoid
#             2. Suggest 1-2 SPECIFIC healthy alternatives from the list
#             3. Mention distance if available
#             4. Make it encouraging and culturally appropriate
#             5. Add 1-2 relevant emojis
            
#             Example: "Skip {trigger_place_name} and try [Place Name] just [distance] away!"
            
#             Keep it natural and conversational.
#             """
            
#             logger.info(f"🤖 Generating AI message with locations for: {trigger_place_name}")
            
#             response = await self.model.generate_content_async(prompt)
#             message = response.text.strip()
            
#             logger.debug(f"AI Response with locations: {message}")
#             return message
            
#         except Exception as e:
#             logger.error(f"Gemini AI error (with locations): {e}")
#             if specific_alternatives:
#                 alt = specific_alternatives[0]
#                 return f"Try {alt.get('name')} ({alt.get('distance', '')}m away) instead of {trigger_place_name}!"
#             return f"Consider a healthy alternative instead of {trigger_place_name}!"
    
#     def _format_alternatives_for_ai(self, alternatives: List[Dict]) -> str:
#         """Format alternatives for AI prompt"""
#         if not alternatives:
#             return "No specific healthy places found nearby."
        
#         formatted = []
#         for i, alt in enumerate(alternatives[:5], 1):
#             line = f"{i}. {alt.get('name', 'Unknown')}"
            
#             # Add distance
#             if alt.get('distance'):
#                 line += f" - {alt.get('distance')}m away"
            
#             # Add rating
#             if alt.get('rating'):
#                 line += f" ⭐ {alt.get('rating')}/5"
            
#             # Add vicinity
#             if alt.get('vicinity'):
#                 line += f"\n   📍 {alt.get('vicinity')}"
            
#             formatted.append(line)
        
#         return '\n\n'.join(formatted)

# # Singleton instance
# ai_service = AIService()


# Add this new method to AIService class:





# import google.generativeai as genai
# from app.config import settings
# from typing import Dict, List, Optional, Any
# import logging

# logger = logging.getLogger(__name__)

# class AIService:
#     def __init__(self):
#         """Initialize Gemini AI with real API"""
#         if not settings.GEMINI_API_KEY:
#             raise ValueError("GEMINI_API_KEY is required")
        
#         genai.configure(api_key=settings.GEMINI_API_KEY)
#         self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
#         logger.info(f"✅ Gemini AI initialized with model: {settings.GEMINI_MODEL}")
    
#     async def generate_recommendation_message(
#         self, 
#         trigger_place_name: str,
#         trigger_category: str, 
#         recommendations: List[str],
#         user_context: str = ""
#     ) -> str:
#         """
#         Generate motivational message using Gemini AI
#         """
#         try:
#             prompt = f"""
#             You are a friendly health coach. A user is near {trigger_place_name} (a {trigger_category}).
            
#             Available healthy alternatives nearby:
#             {', '.join(recommendations) if recommendations else 'Various healthy options'}
            
#             Context: {user_context if user_context else 'General time of day'}
            
#             Write a short, positive, and motivational message (1-2 sentences) 
#             encouraging the user to choose a healthy alternative.
#             Make it feel personal, supportive, and actionable.
#             Include the specific place name {trigger_place_name} in your message.
#             """
            
#             logger.info(f"🤖 Generating AI message for: {trigger_place_name} ({trigger_category})")
            
#             response = await self.model.generate_content_async(prompt)
#             message = response.text.strip()
            
#             logger.debug(f"AI Response: {message}")
#             return message
            
#         except Exception as e:
#             logger.error(f"Gemini AI error: {e}")
#             fallback = f"Consider trying {recommendations[0] if recommendations else 'a healthy option'} instead of {trigger_place_name}!"
#             return fallback
    
#     async def generate_recommendation_with_specific_locations(
#         self,
#         trigger_place_name: str,
#         trigger_category: str,
#         specific_alternatives: List[Dict[str, Any]],
#         user_context: str = ""
#     ) -> str:
#         """
#         Generate motivational message WITH specific location suggestions
#         """
#         try:
#             # Format alternatives for prompt
#             alternatives_text = self._format_alternatives_for_ai(specific_alternatives)
            
#             prompt = f"""
#             You are a friendly health coach in Pakistan. 
            
#             Current Situation:
#             - User is near: {trigger_place_name} (a {trigger_category})
            
#             ACTUAL healthy alternatives available NEARBY:
#             {alternatives_text}
            
#             User Context: {user_context if user_context else 'Looking for healthy options'}
            
#             Write a SHORT, POSITIVE, and ACTIONABLE message (2-3 sentences MAX):
#             1. Mention {trigger_place_name} that user should avoid
#             2. Suggest 1-2 SPECIFIC healthy alternatives from the list
#             3. Mention distance if available
#             4. Make it encouraging and culturally appropriate
#             5. Add 1-2 relevant emojis
            
#             Example: "Skip {trigger_place_name} and try [Place Name] just [distance] away!"
            
#             Keep it natural and conversational.
#             """
            
#             logger.info(f"🤖 Generating AI message with locations for: {trigger_place_name}")
            
#             response = await self.model.generate_content_async(prompt)
#             message = response.text.strip()
            
#             logger.debug(f"AI Response with locations: {message}")
#             return message
            
#         except Exception as e:
#             logger.error(f"Gemini AI error (with locations): {e}")
#             if specific_alternatives:
#                 alt = specific_alternatives[0]
#                 return f"Try {alt.get('name')} ({alt.get('distance', '')}m away) instead of {trigger_place_name}!"
#             return f"Consider a healthy alternative instead of {trigger_place_name}!"
    
#     def _format_alternatives_for_ai(self, alternatives: List[Dict[str, Any]]) -> str:
#         """Format alternatives for AI prompt"""
#         if not alternatives:
#             return "No specific healthy places found nearby."
        
#         formatted = []
#         for i, alt in enumerate(alternatives[:5], 1):
#             line = f"{i}. {alt.get('name', 'Unknown')}"
            
#             # Add distance
#             if alt.get('distance'):
#                 line += f" - {alt.get('distance')}m away"
            
#             # Add rating
#             if alt.get('rating'):
#                 line += f" ⭐ {alt.get('rating')}/5"
            
#             # Add vicinity
#             if alt.get('vicinity'):
#                 line += f"\n   📍 {alt.get('vicinity')}"
            
#             # Add menu items if available
#             if alt.get('top_menu_items'):
#                 menu_items = []
#                 for item in alt['top_menu_items'][:2]:
#                     item_str = item.get('name', 'Item')
#                     if item.get('price'):
#                         item_str += f" (Rs. {item['price']})"
#                     menu_items.append(item_str)
                
#                 if menu_items:
#                     line += f"\n   🍽️ Popular: {', '.join(menu_items)}"
            
#             formatted.append(line)
        
#         return '\n\n'.join(formatted)

# # Singleton instance
# ai_service = AIService()





import google.generativeai as genai
from app.config import settings
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        """Initialize Gemini AI with real API"""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        logger.info(f"✅ Gemini AI initialized with model: {settings.GEMINI_MODEL}")
    
    async def generate_recommendation_message(
        self, 
        trigger_place_name: str,
        trigger_category: str, 
        recommendations: List[str],
        user_context: str = ""
    ) -> str:
        """
        Generate motivational message using Gemini AI
        """
        try:
            prompt = f"""
            You are a friendly health coach. A user is near {trigger_place_name} (a {trigger_category}).
            
            Available healthy alternatives nearby:
            {', '.join(recommendations) if recommendations else 'Various healthy options'}
            
            Context: {user_context if user_context else 'General time of day'}
            
            Write a short, positive, and motivational message (1-2 sentences) 
            encouraging the user to choose a healthy alternative.
            Make it feel personal, supportive, and actionable.
            Include the specific place name {trigger_place_name} in your message.
            """
            
            logger.info(f"🤖 Generating AI message for: {trigger_place_name} ({trigger_category})")
            
            response = await self.model.generate_content_async(prompt)
            message = response.text.strip()
            
            logger.debug(f"AI Response: {message}")
            return message
            
        except Exception as e:
            logger.error(f"Gemini AI error: {e}")
            fallback = f"Consider trying {recommendations[0] if recommendations else 'a healthy option'} instead of {trigger_place_name}!"
            return fallback
    
    async def generate_recommendation_with_specific_locations(
        self,
        trigger_place_name: str,
        trigger_category: str,
        specific_alternatives: List[Dict[str, Any]],
        user_context: str = ""
    ) -> str:
        """
        Generate motivational message WITH specific location suggestions
        """
        try:
            # Format alternatives for prompt
            alternatives_text = self._format_alternatives_for_ai(specific_alternatives)
            
            prompt = f"""
            You are a friendly health coach in Pakistan. 
            
            Current Situation:
            - User is near: {trigger_place_name} (a {trigger_category})
            
            ACTUAL healthy alternatives available NEARBY:
            {alternatives_text}
            
            User Context: {user_context if user_context else 'Looking for healthy options'}
            
            Write a SHORT, POLITE message (2 sentences MAX):
            1. Gently suggest avoiding {trigger_place_name}
            2. Recommend 2-3 SPECIFIC places from the list above
            3. Mention their distances
            4. Be encouraging and positive
            
            Example format: 
            "Instead of {trigger_place_name}, try [Place 1] ([distance]) or [Place 2] ([distance]). 
            They offer great healthy options! 😊"
            
            Use the EXACT place names and distances from the list above.
            """
            
            logger.info(f"🤖 Generating AI message with locations for: {trigger_place_name}")
            
            response = await self.model.generate_content_async(prompt)
            message = response.text.strip()
            
            logger.debug(f"AI Response with locations: {message}")
            return message
            
        except Exception as e:
            logger.error(f"Gemini AI error (with locations): {e}")
            # Create simple message with available data
            if specific_alternatives:
                messages = []
                for i, alt in enumerate(specific_alternatives[:3]):
                    name = alt.get('name', 'a healthy place')
                    distance = alt.get('distance_text', 'nearby')
                    if not distance and alt.get('distance'):
                        dist = alt.get('distance')
                        distance = f"{dist}m away" if dist < 1000 else f"{dist/1000:.1f}km away"
                    
                    rating = alt.get('rating', '')
                    rating_text = f" ({rating}★)" if rating and rating != 'N/A' else ""
                    
                    category = alt.get('category', '')
                    category_text = f" ({category})" if category else ""
                    
                    messages.append(f"{name}{rating_text}{category_text} ({distance})")
                
                return f"Skip {trigger_place_name}! Try {', '.join(messages)} for healthier options! 🥗"
            return f"Consider a healthy alternative instead of {trigger_place_name}!"
    
    def _format_alternatives_for_ai(self, alternatives: List[Dict[str, Any]]) -> str:
        """Format alternatives for AI prompt - SIMPLER VERSION"""
        if not alternatives:
            return "No specific healthy places found nearby."
        
        formatted = []
        for i, alt in enumerate(alternatives[:5], 1):
            line = f"{i}. {alt.get('name', 'Unknown')}"
            
            # Add distance
            if alt.get('distance_text'):
                line += f" - {alt.get('distance_text')}"
            elif alt.get('distance'):
                dist = alt.get('distance')
                line += f" - {dist}m away" if dist < 1000 else f" - {dist/1000:.1f}km away"
            
            # Add rating
            if alt.get('rating') and alt.get('rating') != 'N/A':
                line += f" (⭐ {alt.get('rating')}/5)"
            
            # Add category if available
            if alt.get('category'):
                line += f" - {alt.get('category')}"
            
            formatted.append(line)
        
        return '\n'.join(formatted)

# Singleton instance
ai_service = AIService()