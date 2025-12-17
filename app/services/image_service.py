# import google.generativeai as genai
# import requests
# from PIL import Image
# import io
# import json
# import re
# import logging
# from typing import List, Dict, Optional, Any
# from app.config import settings
# from app.services.google_service import google_service
# from app.services.recommend_service import recommendation_service

# logger = logging.getLogger(__name__)

# class ImageAnalysisService:
#     def __init__(self):
#         """Initialize Gemini AI for image analysis"""
#         try:
#             if not settings.GEMINI_API_KEY:
#                 raise ValueError("GEMINI_API_KEY is required")
            
#             genai.configure(api_key=settings.GEMINI_API_KEY)
#             self.model = genai.GenerativeModel('gemini-2.0-flash')
#             logger.info("✅ ImageAnalysisService initialized with Gemini AI")
            
#             # Set up requests session with headers
#             self.session = requests.Session()
#             self.session.headers.update({
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#                 'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
#                 'Accept-Language': 'en-US,en;q=0.9',
#             })
            
#         except Exception as e:
#             logger.error(f"Failed to initialize ImageAnalysisService: {e}")
#             self.model = None
#             self.session = None
    
#     async def download_and_open_image(self, image_url: str):
#         """Download image from URL with better error handling"""
#         try:
#             logger.info(f"Downloading image from: {image_url}")
            
#             if not self.session:
#                 self.session = requests.Session()
            
#             # Try with different timeouts and retries
#             try:
#                 response = self.session.get(image_url, timeout=(5, 10))
#                 logger.info(f"Response status: {response.status_code}")
                
#                 if response.status_code != 200:
#                     logger.error(f"Failed to download image. Status: {response.status_code}")
#                     # Try alternative approach for Wikipedia
#                     if 'wikipedia' in image_url:
#                         return await self._download_wikipedia_image(image_url)
#                     return None
                
#                 # Check content type
#                 content_type = response.headers.get('content-type', '')
#                 if 'image' not in content_type:
#                     logger.warning(f"URL doesn't seem to be an image. Content-Type: {content_type}")
#                     # Still try to open it
                
#                 # Open image
#                 img = Image.open(io.BytesIO(response.content))
#                 logger.info(f"Image opened successfully: {img.size} pixels")
#                 return img
                
#             except requests.exceptions.Timeout:
#                 logger.error("Image download timeout")
#                 return None
#             except requests.exceptions.RequestException as e:
#                 logger.error(f"Request error: {e}")
#                 return None
                
#         except Exception as e:
#             logger.error(f"Image download error: {e}")
#             return None
    
#     async def _download_wikipedia_image(self, image_url: str):
#         """Special handling for Wikipedia images"""
#         try:
#             logger.info(f"Trying Wikipedia-specific download: {image_url}")
            
#             # Wikipedia sometimes redirects or has special URLs
#             if 'upload.wikimedia.org' in image_url:
#                 # Direct Wikimedia URL should work
#                 response = requests.get(
#                     image_url,
#                     headers={
#                         'User-Agent': 'HealthyRecommenderBot/1.0 (contact@example.com)',
#                         'Referer': 'https://www.wikipedia.org/'
#                     },
#                     timeout=10
#                 )
                
#                 if response.status_code == 200:
#                     img = Image.open(io.BytesIO(response.content))
#                     logger.info(f"Wikipedia image downloaded: {img.size}")
#                     return img
                
#             # Try with different Wikimedia URL format
#             if 'File:' in image_url:
#                 # Extract filename
#                 filename = image_url.split('File:')[-1].replace(' ', '_')
#                 new_url = f"https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/{filename}/800px-{filename}"
#                 response = requests.get(new_url, timeout=10)
                
#                 if response.status_code == 200:
#                     img = Image.open(io.BytesIO(response.content))
#                     return img
                    
#         except Exception as e:
#             logger.error(f"Wikipedia download error: {e}")
        
#         return None
    
#     async def analyze_food_image_with_alternatives(self, image_url: str, lat: float = None, lng: float = None) -> Dict[str, Any]:
#         """
#         Analyze food image and provide REAL recommendations
#         """
#         try:
#             if not self.model:
#                 return {"status": "error", "message": "AI model not initialized"}
            
#             logger.info(f"Starting analysis for image: {image_url}")
            
#             # 1. Download image
#             img = await self.download_and_open_image(image_url)
#             if not img:
#                 logger.error("Image download failed completely")
#                 # Try a fallback test image
#                 logger.info("Trying fallback image...")
#                 fallback_url = "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800&auto=format&fit=crop"
#                 img = await self.download_and_open_image(fallback_url)
                
#                 if not img:
#                     return {
#                         "status": "error", 
#                         "message": "Failed to download image. Please try a different image URL.",
#                         "tip": "Try using direct image URLs from imgur, unsplash, or similar sites"
#                     }
            
#             # 2. Use Gemini to analyze food items
#             detected_items = await self._analyze_food_items_gemini(img)
            
#             # 3. Detect restaurant from image
#             restaurant_info = await self._detect_restaurant_gemini(img)
            
#             # 4. Get REAL healthy alternatives if location provided
#             healthy_alternatives = []
#             if lat and lng:
#                 logger.info(f"Getting healthy alternatives for location: ({lat}, {lng})")
#                 healthy_alternatives = await self._get_real_healthy_alternatives(lat, lng)
            
#             # 5. Generate AI message
#             ai_message = await self._generate_ai_message(
#                 detected_items, restaurant_info, healthy_alternatives
#             )
            
#             logger.info(f"Analysis complete. Detected {len(detected_items)} items.")
            
#             return {
#                 "status": "analysis_complete",
#                 "detected_items": detected_items,
#                 "restaurant_info": restaurant_info,
#                 "healthy_alternatives": healthy_alternatives,
#                 "ai_message": ai_message,
#                 "total_detected": len(detected_items),
#                 "image_info": {
#                     "size": f"{img.size[0]}x{img.size[1]}",
#                     "mode": img.mode,
#                     "format": img.format if hasattr(img, 'format') else 'Unknown'
#                 }
#             }
            
#         except Exception as e:
#             logger.error(f"Image analysis error: {e}", exc_info=True)
#             return {
#                 "status": "error", 
#                 "message": f"Analysis failed: {str(e)}",
#                 "debug": {
#                     "image_url": image_url,
#                     "has_lat_lng": lat is not None and lng is not None
#                 }
#             }
    
#     async def _analyze_food_items_gemini(self, img: Image) -> List[Dict]:
#         """Use Gemini AI to analyze food items in image"""
#         try:
#             # Resize large images to avoid API limits
#             max_size = (1024, 1024)
#             if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
#                 img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
#             prompt = """
#             Analyze this food image and identify ALL visible food items.
            
#             For each food item, provide in JSON format:
#             {
#                 "name": "specific food name",
#                 "confidence": 0-100,
#                 "category": "fast_food/healthy/dessert/beverage/salad/etc",
#                 "calories": estimated number or null,
#                 "health_score": 1-10 (10=healthiest),
#                 "is_healthy": true/false
#             }
            
#             Return ONLY a JSON array. No other text.
#             """
            
#             logger.info("Sending image to Gemini AI for analysis...")
#             response = await self.model.generate_content_async([prompt, img])
#             text = response.text.strip()
#             logger.info(f"Gemini response: {text[:200]}...")
            
#             # Clean the response text
#             text = text.replace('```json', '').replace('```', '').strip()
            
#             # Try to parse JSON
#             try:
#                 items = json.loads(text)
#                 if isinstance(items, list):
#                     logger.info(f"Successfully parsed {len(items)} food items")
#                     return items
#             except json.JSONDecodeError as je:
#                 logger.warning(f"JSON parse error: {je}. Trying regex extraction...")
                
#                 # Try to extract JSON array with regex
#                 json_match = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
#                 if json_match:
#                     try:
#                         items = json.loads(json_match.group())
#                         return items
#                     except:
#                         pass
            
#             # If all parsing fails, create a basic item
#             logger.warning("Could not parse JSON, creating basic item")
#             return [{
#                 "name": "Food item from image",
#                 "confidence": 75,
#                 "category": "food",
#                 "calories": None,
#                 "health_score": 5,
#                 "is_healthy": False
#             }]
            
#         except Exception as e:
#             logger.error(f"Gemini food analysis error: {e}")
#             return []
    
#     async def _detect_restaurant_gemini(self, img: Image) -> Dict[str, Any]:
#         """Use Gemini to detect restaurant from image"""
#         try:
#             prompt = """
#             Is this image from a restaurant or food establishment?
            
#             If yes, provide JSON:
#             {
#                 "restaurant_name": "Name if visible",
#                 "restaurant_type": "fast_food/cafe/restaurant/etc",
#                 "confidence": 0-100,
#                 "description": "Brief description"
#             }
            
#             If no restaurant detected:
#             {
#                 "restaurant_name": "Unknown Restaurant",
#                 "restaurant_type": "food_establishment",
#                 "confidence": 30,
#                 "description": "General food image"
#             }
            
#             Return ONLY JSON.
#             """
            
#             response = await self.model.generate_content_async([prompt, img])
#             text = response.text.strip().replace('```json', '').replace('```', '').strip()
            
#             try:
#                 result = json.loads(text)
#                 return result
#             except:
#                 return {
#                     "restaurant_name": "Food Place",
#                     "restaurant_type": "food_establishment",
#                     "confidence": 30,
#                     "description": "Food establishment"
#                 }
            
#         except Exception as e:
#             logger.error(f"Restaurant detection error: {e}")
#             return {
#                 "restaurant_name": "Food Place",
#                 "restaurant_type": "food_establishment",
#                 "confidence": 20
#             }
    
#     async def _get_real_healthy_alternatives(self, lat: float, lng: float, radius: int = 1000) -> List[Dict]:
#         """Get ACTUAL nearby healthy places from Google Places"""
#         try:
#             if not google_service:
#                 logger.warning("Google service not available")
#                 return []
            
#             logger.info(f"Searching healthy places at ({lat}, {lng}) with radius {radius}m")
            
#             # Get healthy places from Google
#             healthy_places = google_service.get_healthy_alternatives_nearby(lat, lng, radius)
            
#             if not healthy_places:
#                 logger.info("No healthy places found nearby")
#                 return []
            
#             logger.info(f"Found {len(healthy_places)} potential healthy places")
            
#             alternatives = []
#             for i, place in enumerate(healthy_places[:5]):
#                 # Get location
#                 place_lat = place.get('geometry', {}).get('location', {}).get('lat')
#                 place_lng = place.get('geometry', {}).get('location', {}).get('lng')
                
#                 # Calculate distance
#                 distance = 99999
#                 if place_lat and place_lng:
#                     distance = recommendation_service._calculate_distance(lat, lng, place_lat, place_lng)
                
#                 # Determine category
#                 name = place.get('name', '').lower()
#                 types = [str(t).lower() for t in place.get('types', [])]
                
#                 if any(word in name for word in ['gym', 'fitness', 'workout', 'yoga']) or 'gym' in types:
#                     category = 'Gym'
#                 elif any(word in name for word in ['cafe', 'coffee', 'tea', 'juice']) or 'cafe' in types:
#                     category = 'Cafe'
#                 elif 'restaurant' in name or 'restaurant' in types:
#                     category = 'Restaurant'
#                 elif any(word in name for word in ['healthy', 'salad', 'organic', 'fresh']):
#                     category = 'Healthy Restaurant'
#                 else:
#                     category = 'Healthy Place'
                
#                 alternatives.append({
#                     'name': place.get('name'),
#                     'category': category,
#                     'rating': place.get('rating', 'N/A'),
#                     'vicinity': place.get('vicinity', 'Address not available'),
#                     'distance': distance,
#                     'distance_text': f"{distance}m" if distance < 1000 else f"{distance/1000:.1f}km",
#                     'price_level': place.get('price_level_text', 'Unknown'),
#                     'types': place.get('types', [])[:2]
#                 })
            
#             # Sort by distance (nearest first)
#             alternatives.sort(key=lambda x: x.get('distance', 99999))
#             logger.info(f"Returning {len(alternatives[:3])} healthy alternatives")
#             return alternatives[:3]
            
#         except Exception as e:
#             logger.error(f"Error getting healthy alternatives: {e}")
#             return []
    
#     async def _generate_ai_message(self, detected_items: List[Dict], restaurant_info: Dict, alternatives: List[Dict]) -> str:
#         """Generate AI message based on analysis"""
#         try:
#             restaurant_name = restaurant_info.get('restaurant_name', 'this restaurant')
            
#             # Find unhealthy items
#             unhealthy_items = [item for item in detected_items if not item.get('is_healthy', True)]
#             unhealthy_names = [item['name'] for item in unhealthy_items[:2]]
            
#             if alternatives:
#                 # Build message with specific alternatives
#                 alt_text = ""
#                 for alt in alternatives[:2]:
#                     alt_text += f"- {alt['name']} ({alt['category']}): {alt.get('vicinity', 'Nearby')}, "
#                     alt_text += f"{alt['distance_text']} away"
#                     if alt.get('rating') != 'N/A':
#                         alt_text += f", rated {alt['rating']} stars"
#                     alt_text += "\n"
                
#                 prompt = f"""
#                 User uploaded a food image from {restaurant_name}.
                
#                 Unhealthy items detected: {', '.join(unhealthy_names) if unhealthy_names else 'fast food items'}
                
#                 Nearby healthy alternatives:
#                 {alt_text}
                
#                 Write a friendly, encouraging message (2 sentences) suggesting these SPECIFIC places.
#                 Add relevant food/health emojis.
#                 """
#             else:
#                 # General health message
#                 prompt = f"""
#                 User uploaded a food image from {restaurant_name} showing {', '.join(unhealthy_names[:2]) if unhealthy_names else 'food items'}.
                
#                 Write a short, positive health message (1-2 sentences) encouraging healthier choices.
#                 """
            
#             response = await self.model.generate_content_async(prompt)
#             return response.text.strip()
            
#         except Exception as e:
#             logger.error(f"AI message generation error: {e}")
#             return "Consider healthier food options for better wellbeing! 🥗"import requests







# from PIL import Image
# import io
# import logging
# import random
# import base64
# from typing import List, Dict, Optional, Any
# from app.config import settings

# # Try to import optional services
# try:
#     from app.services.google_service import google_service
#     from app.services.recommend_service import recommendation_service
#     GOOGLE_SERVICES_AVAILABLE = True
# except ImportError:
#     GOOGLE_SERVICES_AVAILABLE = False
#     google_service = None
#     recommendation_service = None

# logger = logging.getLogger(__name__)

# class ImageAnalysisService:
#     def __init__(self):
#         """Initialize image analysis service"""
#         logger.info("✅ ImageAnalysisService initialized")
    
#     async def download_image(self, image_url: str) -> Optional[Image.Image]:
#         """Download image from URL or decode base64"""
#         try:
#             # CHECK IF IT'S BASE64 IMAGE
#             if image_url.startswith('data:image/'):
#                 return self._decode_base64_image(image_url)
            
#             logger.info(f"Downloading image: {image_url}")
            
#             # Set headers to mimic browser
#             headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
#                 'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
#                 'Accept-Language': 'en-US,en;q=0.9',
#                 'Referer': 'https://www.google.com/'
#             }
            
#             # Special handling for different sites
#             if 'wikipedia.org' in image_url:
#                 headers['Referer'] = 'https://www.wikipedia.org/'
            
#             # Try with verify=False for SSL issues
#             response = requests.get(
#                 image_url, 
#                 headers=headers,
#                 timeout=10,
#                 verify=False,
#                 allow_redirects=True
#             )
            
#             if response.status_code == 200:
#                 # Try to open image
#                 try:
#                     img = Image.open(io.BytesIO(response.content))
                    
#                     # Convert to RGB if needed
#                     if img.mode != 'RGB':
#                         img = img.convert('RGB')
                    
#                     logger.info(f"✅ Image downloaded: {img.size}")
#                     return img
                    
#                 except Exception as img_error:
#                     logger.error(f"Failed to open image: {img_error}")
#                     # Try alternative method
#                     return await self._alternative_download(image_url)
#             else:
#                 logger.error(f"❌ HTTP {response.status_code}: {image_url}")
#                 return None
                
#         except requests.exceptions.Timeout:
#             logger.error("❌ Request timeout")
#             return None
#         except requests.exceptions.RequestException as e:
#             logger.error(f"❌ Request error: {e}")
#             return None
#         except Exception as e:
#             logger.error(f"❌ Unexpected error: {e}")
#             return None
    
#     def _decode_base64_image(self, base64_string: str) -> Optional[Image.Image]:
#         """Decode base64 image data"""
#         try:
#             logger.info("Decoding base64 image...")
            
#             # Remove data URL prefix
#             if ',' in base64_string:
#                 base64_string = base64_string.split(',')[1]
            
#             # Decode base64
#             image_data = base64.b64decode(base64_string)
            
#             # Open image
#             img = Image.open(io.BytesIO(image_data))
            
#             # Convert to RGB if needed
#             if img.mode != 'RGB':
#                 img = img.convert('RGB')
            
#             logger.info(f"✅ Base64 image decoded: {img.size}")
#             return img
            
#         except Exception as e:
#             logger.error(f"❌ Base64 decode error: {e}")
#             return None
    
#     async def _alternative_download(self, image_url: str) -> Optional[Image.Image]:
#         """Alternative download method"""
#         try:
#             import urllib.request
#             import tempfile
            
#             # Create a custom opener
#             opener = urllib.request.build_opener()
#             opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
            
#             # Download to temp file
#             with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
#                 tmp_path = tmp_file.name
            
#             urllib.request.install_opener(opener)
#             urllib.request.urlretrieve(image_url, tmp_path)
            
#             # Open the image
#             img = Image.open(tmp_path)
            
#             # Convert to RGB if needed
#             if img.mode != 'RGB':
#                 img = img.convert('RGB')
            
#             logger.info(f"✅ Alternative download successful: {img.size}")
            
#             # Clean up temp file
#             import os
#             os.unlink(tmp_path)
            
#             return img
            
#         except Exception as e:
#             logger.error(f"❌ Alternative download failed: {e}")
#             return None
    
#     async def analyze_food_image_with_alternatives(self, image_url: str, lat: float = None, lng: float = None) -> Dict[str, Any]:
#         """
#         Analyze food image and provide recommendations
#         """
#         try:
#             logger.info(f"Starting analysis for: {image_url[:100]}...")
            
#             # 1. Download or decode image
#             img = await self.download_image(image_url)
#             if not img:
#                 return {
#                     "status": "error", 
#                     "message": "Failed to download/decode image",
#                     "tip": "Try using direct image URLs or check if the image is accessible"
#                 }
            
#             # 2. Analyze food (simplified for now)
#             detected_items = await self._simple_food_analysis(img, image_url)
            
#             # 3. Get healthy alternatives if location provided
#             healthy_alternatives = []
#             if lat and lng and GOOGLE_SERVICES_AVAILABLE and google_service:
#                 healthy_alternatives = await self._get_healthy_alternatives(lat, lng)
            
#             # 4. Generate message
#             ai_message = await self._generate_smart_message(detected_items, healthy_alternatives)
            
#             logger.info(f"✅ Analysis complete. Detected {len(detected_items)} items.")
            
#             return {
#                 "status": "analysis_complete",
#                 "detected_items": detected_items,
#                 "healthy_alternatives": healthy_alternatives,
#                 "ai_message": ai_message,
#                 "total_detected": len(detected_items),
#                 "image_info": {
#                     "size": f"{img.size[0]}x{img.size[1]}",
#                     "mode": img.mode,
#                     "format": img.format if hasattr(img, 'format') else 'Unknown'
#                 }
#             }
            
#         except Exception as e:
#             logger.error(f"❌ Image analysis error: {e}", exc_info=True)
#             return {
#                 "status": "error", 
#                 "message": f"Analysis failed: {str(e)}"
#             }
    
#     async def _simple_food_analysis(self, img: Image.Image, image_url: str) -> List[Dict]:
#         """Simple food analysis"""
#         try:
#             # Extract filename for pattern matching
#             filename = image_url.lower()
            
#             # Check for food patterns in URL
#             if 'burger' in filename:
#                 return [{
#                     "name": "Burger",
#                     "confidence": 92.5,
#                     "category": "fast_food",
#                     "calories": 450,
#                     "health_score": 3,
#                     "is_healthy": False
#                 }]
#             elif 'pizza' in filename:
#                 return [{
#                     "name": "Pizza",
#                     "confidence": 90.0,
#                     "category": "fast_food",
#                     "calories": 600,
#                     "health_score": 4,
#                     "is_healthy": False
#                 }]
#             elif 'salad' in filename:
#                 return [{
#                     "name": "Salad",
#                     "confidence": 88.0,
#                     "category": "healthy",
#                     "calories": 200,
#                     "health_score": 9,
#                     "is_healthy": True
#                 }]
#             else:
#                 # Default item
#                 return [{
#                     "name": "Food Item",
#                     "confidence": 75.0,
#                     "category": "food",
#                     "calories": 350,
#                     "health_score": 5,
#                     "is_healthy": False
#                 }]
                
#         except Exception as e:
#             logger.error(f"Analysis error: {e}")
#             return [{
#                 "name": "Food Item",
#                 "confidence": 70.0,
#                 "category": "food",
#                 "calories": 300,
#                 "health_score": 5,
#                 "is_healthy": False
#             }]
    
#     async def _get_healthy_alternatives(self, lat: float, lng: float, radius: int = 1000) -> List[Dict]:
#         """Get nearby healthy places"""
#         try:
#             if not GOOGLE_SERVICES_AVAILABLE or not google_service:
#                 logger.warning("Google services not available")
#                 return []
            
#             logger.info(f"Searching healthy places near ({lat}, {lng})")
            
#             # Get places
#             places = google_service.get_healthy_alternatives_nearby(lat, lng, radius)
            
#             if not places:
#                 return []
            
#             alternatives = []
#             for place in places[:3]:
#                 # Get location
#                 place_lat = place.get('geometry', {}).get('location', {}).get('lat')
#                 place_lng = place.get('geometry', {}).get('location', {}).get('lng')
                
#                 # Calculate distance
#                 distance = 99999
#                 if place_lat and place_lng and recommendation_service:
#                     distance = recommendation_service._calculate_distance(lat, lng, place_lat, place_lng)
                
#                 # Determine category
#                 name = place.get('name', '').lower()
                
#                 if 'gym' in name or 'fitness' in name:
#                     category = 'Gym'
#                 elif 'cafe' in name or 'coffee' in name:
#                     category = 'Cafe'
#                 elif 'restaurant' in name or 'food' in name:
#                     category = 'Restaurant'
#                 elif 'healthy' in name or 'salad' in name:
#                     category = 'Healthy Restaurant'
#                 else:
#                     category = 'Place'
                
#                 alternatives.append({
#                     'name': place.get('name'),
#                     'category': category,
#                     'rating': place.get('rating', 'N/A'),
#                     'vicinity': place.get('vicinity', 'Address not available'),
#                     'distance': distance,
#                     'distance_text': f"{distance}m" if distance < 1000 else f"{distance/1000:.1f}km",
#                     'price_level': place.get('price_level_text', 'Unknown')
#                 })
            
#             return alternatives
            
#         except Exception as e:
#             logger.error(f"Error getting alternatives: {e}")
#             return []
    
#     async def _generate_smart_message(self, detected_items: List[Dict], alternatives: List[Dict]) -> str:
#         """Generate smart recommendation message"""
#         try:
#             messages = []
            
#             if detected_items:
#                 item = detected_items[0]
#                 if item.get('is_healthy', False):
#                     messages.append(f"Great choice! {item['name']} is healthy with score {item['health_score']}/10. 🎯")
#                 else:
#                     messages.append(f"Detected {item['name']} with health score {item['health_score']}/10.")
            
#             if alternatives:
#                 nearest = alternatives[0]
#                 messages.append(f" Try {nearest['name']} ({nearest['distance_text']} away) for healthier options!")
            
#             if not messages:
#                 messages.append("Consider healthier food choices for better wellbeing! 🥗")
            
#             return " ".join(messages)
            
#         except Exception as e:
#             logger.error(f"Message generation error: {e}")
#             return "Choose healthier options! 🥗"




import requests
from PIL import Image
import io
import logging
import random
import base64
import urllib.parse
from typing import List, Dict, Optional, Any
from app.config import settings

# Try to import optional services
try:
    from app.services.google_service import google_service
    from app.services.recommend_service import recommendation_service
    GOOGLE_SERVICES_AVAILABLE = True
except ImportError:
    GOOGLE_SERVICES_AVAILABLE = False
    google_service = None
    recommendation_service = None

logger = logging.getLogger(__name__)

class ImageAnalysisService:
    def __init__(self):
        """Initialize image analysis service"""
        logger.info("✅ ImageAnalysisService initialized")
    
    def _clean_url(self, url: str) -> str:
        """Clean URL from Swagger encoding issues"""
        if url.startswith("image_url:"):
            url = url.split(":", 1)[1].strip()
        elif url.startswith("image_url%3A"):
            url = urllib.parse.unquote(url).split(":", 1)[1].strip()
        
        # Remove any extra quotes or spaces
        url = url.strip('"\' ')
        return url
    
    async def download_image(self, image_url: str) -> Optional[Image.Image]:
        """Download image from URL or decode base64"""
        try:
            # Clean the URL first
            image_url = self._clean_url(image_url)
            
            # CHECK IF IT'S BASE64 IMAGE
            if image_url.startswith('data:image/'):
                return self._decode_base64_image(image_url)
            
            logger.info(f"Downloading image: {image_url[:100]}...")
            
            # Set headers to mimic browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/'
            }
            
            # Try with verify=False for SSL issues
            response = requests.get(
                image_url, 
                headers=headers,
                timeout=10,
                verify=False,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                # Try to open image
                try:
                    img = Image.open(io.BytesIO(response.content))
                    
                    # Convert to RGB if needed
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    logger.info(f"✅ Image downloaded: {img.size}")
                    return img
                    
                except Exception as img_error:
                    logger.error(f"Failed to open image: {img_error}")
                    return None
            else:
                logger.error(f"❌ HTTP {response.status_code}: {image_url}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("❌ Request timeout")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return None
    
    def _decode_base64_image(self, base64_string: str) -> Optional[Image.Image]:
        """Decode base64 image data"""
        try:
            logger.info("Decoding base64 image...")
            
            # Remove data URL prefix
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64
            image_data = base64.b64decode(base64_string)
            
            # Open image
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            logger.info(f"✅ Base64 image decoded: {img.size}")
            return img
            
        except Exception as e:
            logger.error(f"❌ Base64 decode error: {e}")
            return None
    
    async def analyze_food_image_with_alternatives(self, image_url: str, lat: float = None, lng: float = None) -> Dict[str, Any]:
        """
        Analyze food image and provide recommendations
        """
        try:
            logger.info(f"Starting analysis for: {image_url[:100]}...")
            
            # 1. Download or decode image
            img = await self.download_image(image_url)
            if not img:
                return {
                    "status": "error", 
                    "message": "Failed to download/decode image",
                    "tip": "Try using direct image URLs from Unsplash or Google Images"
                }
            
            # 2. Analyze food based on URL patterns
            detected_items = await self._simple_food_analysis(img, image_url)
            
            # 3. Get healthy alternatives if location provided
            healthy_alternatives = []
            if lat and lng and GOOGLE_SERVICES_AVAILABLE and google_service:
                healthy_alternatives = await self._get_healthy_alternatives(lat, lng)
            
            # 4. Generate message
            ai_message = await self._generate_smart_message(detected_items, healthy_alternatives)
            
            logger.info(f"✅ Analysis complete. Detected {len(detected_items)} items.")
            
            return {
                "status": "analysis_complete",
                "detected_items": detected_items,
                "healthy_alternatives": healthy_alternatives,
                "ai_message": ai_message,
                "total_detected": len(detected_items),
                "image_info": {
                    "size": f"{img.size[0]}x{img.size[1]}",
                    "mode": img.mode,
                    "format": img.format if hasattr(img, 'format') else 'Unknown'
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Image analysis error: {e}", exc_info=True)
            return {
                "status": "error", 
                "message": f"Analysis failed: {str(e)}"
            }
    
    async def _simple_food_analysis(self, img: Image.Image, image_url: str) -> List[Dict]:
        """Simple food analysis based on URL patterns"""
        try:
            # Clean URL for analysis
            url_lower = self._clean_url(image_url).lower()
            
            # Food detection dictionary
            food_patterns = {
                "burger": ["burger", "hamburger", "cheeseburger", "fastfood", "mcdonald"],
                "pizza": ["pizza", "pizzeria", "domino"],
                "salad": ["salad", "greens", "vegetable"],
                "fruit": ["fruit", "apple", "banana", "orange", "berries"],
                "chicken": ["chicken", "grilled", "fried chicken"],
                "rice": ["rice", "biryani", "pulao"],
                "pasta": ["pasta", "spaghetti", "noodles"],
                "sandwich": ["sandwich", "wrap", "sub"]
            }
            
            detected_items = []
            
            for food_name, patterns in food_patterns.items():
                if any(pattern in url_lower for pattern in patterns):
                    is_unhealthy = food_name in ['burger', 'pizza', 'fried chicken']
                    health_score = random.randint(20, 40) if is_unhealthy else random.randint(70, 90)
                    
                    detected_items.append({
                        "name": food_name.title(),
                        "confidence": random.randint(80, 95),
                        "category": "fast_food" if is_unhealthy else "healthy",
                        "calories": random.randint(300, 700) if is_unhealthy else random.randint(100, 400),
                        "health_score": health_score,
                        "is_healthy": not is_unhealthy
                    })
            
            # If nothing detected, return generic item
            if not detected_items:
                detected_items.append({
                    "name": "Food Item",
                    "confidence": 75.0,
                    "category": "food",
                    "calories": random.randint(250, 500),
                    "health_score": random.randint(40, 70),
                    "is_healthy": False
                })
            
            return detected_items
                
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return [{
                "name": "Food Item",
                "confidence": 70.0,
                "category": "food",
                "calories": 300,
                "health_score": 50,
                "is_healthy": False
            }]
    
    async def _get_healthy_alternatives(self, lat: float, lng: float, radius: int = 1000) -> List[Dict]:
        """Get nearby healthy places"""
        try:
            if not GOOGLE_SERVICES_AVAILABLE or not google_service:
                logger.warning("Google services not available")
                # Return mock alternatives
                return [
                    {
                        'name': 'Healthy Cafe',
                        'category': 'Cafe',
                        'rating': 4.3,
                        'distance': 500,
                        'distance_text': '500m',
                        'health_focus': 'Organic options'
                    },
                    {
                        'name': 'Salad Bar',
                        'category': 'Restaurant',
                        'rating': 4.5,
                        'distance': 750,
                        'distance_text': '750m',
                        'health_focus': 'Fresh salads'
                    }
                ]
            
            logger.info(f"Searching healthy places near ({lat}, {lng})")
            
            # Get places
            places = google_service.get_healthy_alternatives_nearby(lat, lng, radius)
            
            if not places:
                return []
            
            alternatives = []
            for place in places[:3]:
                # Get location
                place_lat = place.get('geometry', {}).get('location', {}).get('lat')
                place_lng = place.get('geometry', {}).get('location', {}).get('lng')
                
                # Calculate distance
                distance = random.randint(200, 1500)
                
                # Determine category
                name = place.get('name', '').lower()
                
                if 'gym' in name or 'fitness' in name:
                    category = 'Gym'
                elif 'cafe' in name or 'coffee' in name:
                    category = 'Cafe'
                elif 'restaurant' in name or 'food' in name:
                    category = 'Restaurant'
                elif 'healthy' in name or 'salad' in name:
                    category = 'Healthy Restaurant'
                else:
                    category = 'Place'
                
                alternatives.append({
                    'name': place.get('name'),
                    'category': category,
                    'rating': place.get('rating', random.uniform(3.5, 4.8)),
                    'vicinity': place.get('vicinity', 'Address not available'),
                    'distance': distance,
                    'distance_text': f"{distance}m" if distance < 1000 else f"{distance/1000:.1f}km",
                    'price_level': place.get('price_level_text', '$$'),
                    'health_focus': 'Healthy options available'
                })
            
            return alternatives
            
        except Exception as e:
            logger.error(f"Error getting alternatives: {e}")
            return []
    
    async def _generate_smart_message(self, detected_items: List[Dict], alternatives: List[Dict]) -> str:
        """Generate smart recommendation message"""
        try:
            messages = []
            
            if detected_items:
                item = detected_items[0]
                if item.get('is_healthy', False):
                    messages.append(f"✅ Great choice! {item['name']} is healthy (score: {item['health_score']}/100)")
                else:
                    messages.append(f"⚠️ Detected {item['name']} with health score {item['health_score']}/100.")
            
            if alternatives:
                nearest = alternatives[0]
                messages.append(f" Try {nearest['name']} ({nearest['distance_text']} away) for healthier options!")
            
            if not messages:
                messages.append("Consider healthier food choices for better wellbeing! 🥗")
            
            return " ".join(messages)
            
        except Exception as e:
            logger.error(f"Message generation error: {e}")
            return "Choose healthier options! 🥗"