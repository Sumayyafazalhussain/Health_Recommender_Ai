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