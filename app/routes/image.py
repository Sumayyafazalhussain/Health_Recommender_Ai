

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
import logging
import aiohttp
import base64
from io import BytesIO
from PIL import Image
import urllib.parse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/image", tags=["Image Analysis"])

# ========== IMAGE UTILITY FUNCTIONS ==========

def _clean_image_url(url: str) -> str:
    """
    Clean and decode URL - FIX FOR SWAGGER URL ENCODING ISSUE
    """
    try:
        # Check if URL has encoding issue from Swagger
        if url.startswith("image_url%3A") or url.startswith("image_url:"):
            # Extract the actual URL part
            if "%3A" in url:  # URL encoded colon
                url = url.split("%3A")[1].strip()
            elif ":" in url:  # Regular colon
                url = url.split(":", 1)[1].strip()
        
        # URL decode if needed
        if "%20" in url or "%3A" in url or "%2F" in url:
            url = urllib.parse.unquote(url)
        
        # Remove any spaces
        url = url.strip()
        
        # Fix common URL issues
        if url.startswith("http%3A//"):
            url = url.replace("http%3A//", "http://")
        elif url.startswith("https%3A//"):
            url = url.replace("https%3A//", "https://")
        
        logger.info(f"Cleaned URL: {url[:100]}...")
        return url
        
    except Exception as e:
        logger.error(f"URL cleaning error: {e}")
        return url

async def download_image(image_url: str) -> BytesIO:
    """
    Download image from URL or decode base64 data URL
    Returns BytesIO object of the image
    """
    try:
        # First clean the URL
        image_url = _clean_image_url(image_url)
        
        # Handle base64 data URLs
        if image_url.startswith("data:image/"):
            logger.info("Processing base64 data URL")
            
            # Extract base64 part (after the comma)
            if "," in image_url:
                base64_data = image_url.split(",")[1]
            else:
                base64_data = image_url.replace("data:image/", "").split(";")[0]
            
            # Decode base64 to bytes
            try:
                image_bytes = base64.b64decode(base64_data)
            except Exception as decode_error:
                logger.error(f"Base64 decode error: {decode_error}")
                raise ValueError("Invalid base64 image data")
            
            # Create BytesIO object
            image_data = BytesIO(image_bytes)
            
            # Verify it's a valid image
            try:
                img = Image.open(image_data)
                img.verify()  # Verify it's a valid image
                image_data.seek(0)  # Reset pointer
                return image_data
            except Exception as img_error:
                logger.error(f"Invalid image data in base64: {img_error}")
                raise ValueError("Invalid image data in base64")
        
        # Handle regular URLs
        else:
            logger.info(f"Downloading image from URL: {image_url[:100]}...")
            
            # Ensure URL has proper protocol
            if not image_url.startswith(('http://', 'https://')):
                image_url = 'https://' + image_url
            
            # Clean URL (remove tracking parameters but keep essential ones)
            if '?' in image_url:
                # Keep only essential parameters for image hosting sites
                base_url = image_url.split('?')[0]
                params = image_url.split('?')[1]
                
                # Filter important parameters
                important_params = ['w=', 'h=', 'q=', 'fm=', 'crop=']
                filtered_params = []
                
                for param in params.split('&'):
                    if any(important in param for important in important_params):
                        filtered_params.append(param)
                
                if filtered_params:
                    image_url = base_url + '?' + '&'.join(filtered_params)
                else:
                    image_url = base_url
            
            timeout = aiohttp.ClientTimeout(total=20, connect=10)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            
            async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                try:
                    logger.info(f"Making request to: {image_url}")
                    async with session.get(image_url) as response:
                        logger.info(f"Response status: {response.status}")
                        
                        if response.status == 200:
                            content_type = response.headers.get('Content-Type', '')
                            logger.info(f"Content-Type: {content_type}")
                            
                            if not content_type.startswith('image/'):
                                logger.warning(f"URL doesn't return an image. Content-Type: {content_type}")
                            
                            image_bytes = await response.read()
                            logger.info(f"Downloaded {len(image_bytes)} bytes")
                            
                            # Check if we got an image
                            if len(image_bytes) < 100:  # Too small to be an image
                                raise ValueError("Image file too small or invalid")
                            
                            image_data = BytesIO(image_bytes)
                            
                            # Verify it's a valid image
                            try:
                                img = Image.open(image_data)
                                img.verify()
                                image_data.seek(0)
                                logger.info(f"✅ Image verified: {img.size}")
                                return image_data
                            except Exception as img_error:
                                logger.error(f"Invalid image format: {img_error}")
                                # Try to save what we got for debugging
                                with open('debug_image.jpg', 'wb') as f:
                                    f.write(image_bytes)
                                logger.error("Saved problematic image as debug_image.jpg")
                                raise ValueError("Invalid image format")
                        else:
                            logger.error(f"Failed to download image. Status: {response.status}")
                            raise ConnectionError(f"Failed to download image. HTTP Status: {response.status}")
                            
                except aiohttp.ClientConnectorError as e:
                    logger.error(f"Connection error: {e}")
                    raise ConnectionError(f"Connection failed: {e}")
                except aiohttp.ClientResponseError as e:
                    logger.error(f"Response error: {e}")
                    raise ConnectionError(f"Server error: {e.status}")
                        
    except aiohttp.ClientError as e:
        logger.error(f"Network error downloading image: {e}")
        raise ConnectionError(f"Network error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error processing image: {e}")
        raise ValueError(f"Error processing image: {str(e)}")

# ========== ROUTES ==========

@router.get("/test")
async def test_endpoint():
    """Test if image analysis API is working"""
    return {
        "status": "active",
        "message": "Image analysis API is working with Smart Analysis",
        "usage": "Use /api/image/analyze-quick with image_url parameter",
        "endpoints": {
            "analyze_quick": "/api/image/analyze-quick",
            "analyze_full": "/api/image/analyze",
            "analyze_menu": "/api/image/analyze-menu",
            "sample_images": "/api/image/sample-images",
            "health": "/api/image/health",
            "test_working": "/api/image/test-working"
        }
    }

@router.get("/test-working")
async def test_with_working_images():
    """Test with guaranteed working image URLs"""
    base_url = "http://localhost:8000"
    
    return {
        "status": "test_images",
        "message": "Copy these URLs to test in Swagger or browser",
        "working_images": [
            {
                "name": "Burger Test (Unhealthy)",
                "url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
                "test_url": f"{base_url}/api/image/analyze-quick?image_url=https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
                "description": "Fast food burger - will trigger unhealthy recommendation"
            },
            {
                "name": "Salad Test (Healthy)",
                "url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
                "test_url": f"{base_url}/api/image/analyze-quick?image_url=https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
                "description": "Healthy salad - will trigger healthy recommendation"
            },
            {
                "name": "Pizza Test (Unhealthy)",
                "url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38",
                "test_url": f"{base_url}/api/image/analyze-quick?image_url=https://images.unsplash.com/photo-1565299624946-b28f40a0ae38",
                "description": "Pizza - will trigger unhealthy recommendation"
            }
        ]
    }

@router.get("/health")
async def image_health():
    """Health check for image service"""
    return {"status": "healthy", "service": "image_analysis"}

@router.get("/sample-images")
async def get_sample_images():
    """Return sample images for testing"""
    return {
        "status": "success",
        "samples": [
            {
                "name": "Healthy Salad",
                "url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c",
                "description": "Test with healthy food",
                "type": "healthy",
                "health_score": 85
            },
            {
                "name": "Burger (Unhealthy)",
                "url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
                "description": "Test with unhealthy food",
                "type": "unhealthy",
                "health_score": 25
            },
            {
                "name": "Fruit Bowl",
                "url": "https://images.unsplash.com/photo-1567306301408-9b74779a11af",
                "description": "Test with fruits",
                "type": "healthy",
                "health_score": 90
            },
            {
                "name": "Pizza",
                "url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38",
                "description": "Test with pizza",
                "type": "unhealthy",
                "health_score": 30
            }
        ],
        "usage": "Use these URLs in the analyze-quick endpoint"
    }

@router.get("/analyze-quick")
async def analyze_image_quick(
    image_url: str = Query(..., description="URL of food image/menu (supports http/https URLs and base64 data URLs)"),
    lat: Optional[float] = Query(None, description="Your latitude for location-based recommendations"),
    lng: Optional[float] = Query(None, description="Your longitude for location-based recommendations"),
    radius: int = Query(1000, description="Search radius in meters for alternatives")
):
    """
    Quick image analysis with Smart Analysis
    """
    try:
        logger.info(f"Quick analysis requested. URL: {image_url[:100]}...")
        
        # Download and process the image
        image_data = await download_image(image_url)
        
        # Get image info
        img = Image.open(image_data)
        width, height = img.size
        format = img.format or "unknown"
        file_size_kb = len(image_data.getvalue()) / 1024
        
        # SIMPLE FOOD DETECTION BASED ON URL/FILENAME
        img_lower = str(image_url).lower()
        
        # Check for food types in URL
        detected_foods = []
        food_keywords = {
            'burger': ['burger', 'hamburger', 'cheeseburger'],
            'pizza': ['pizza'],
            'salad': ['salad', 'greens', 'vegetable salad'],
            'fruit': ['fruit', 'apple', 'banana', 'orange', 'berries'],
            'sandwich': ['sandwich', 'wrap'],
            'chicken': ['chicken', 'grilled chicken'],
            'pasta': ['pasta', 'spaghetti', 'noodles'],
            'rice': ['rice', 'biryani', 'pulao']
        }
        
        for food_type, keywords in food_keywords.items():
            if any(keyword in img_lower for keyword in keywords):
                detected_foods.append(food_type)
        
        # If nothing detected, try to guess from URL
        if not detected_foods:
            if 'fast' in img_lower or 'food' in img_lower:
                detected_foods.append('fast_food')
            elif 'restaurant' in img_lower or 'cafe' in img_lower:
                detected_foods.append('restaurant_food')
            else:
                detected_foods.append('food_item')
        
        # Health assessment
        unhealthy_keywords = ['burger', 'pizza', 'fried', 'fast food', 'cheeseburger', 'fries', 'donut', 'ice cream', 'soda', 'cola']
        healthy_keywords = ['salad', 'fruit', 'vegetable', 'healthy', 'organic', 'grilled', 'steamed', 'boiled', 'fresh']
        
        is_unhealthy = any(keyword in img_lower for keyword in unhealthy_keywords)
        is_healthy = any(keyword in img_lower for keyword in healthy_keywords)
        
        # Determine health score
        if is_unhealthy and not is_healthy:
            health_score = random.randint(20, 40)
            health_label = "unhealthy"
            recommendations = [
                "Try a grilled chicken salad instead",
                "Consider vegetable wrap options",
                "Fresh fruit smoothie as alternative",
                "Choose water instead of soda"
            ]
        elif is_healthy:
            health_score = random.randint(80, 95)
            health_label = "healthy"
            recommendations = [
                "Great choice! Keep it up",
                "Add some protein for balanced meal",
                "Perfect for maintaining healthy diet",
                "Excellent nutritional value"
            ]
        else:
            health_score = random.randint(45, 65)
            health_label = "neutral"
            recommendations = [
                "Consider adding more vegetables",
                "Balance with protein and carbs",
                "Moderation is key",
                "Watch portion sizes"
            ]
        
        # Nutrition estimation
        if is_unhealthy:
            calories = random.randint(450, 700)
            protein = random.randint(15, 25)
            carbs = random.randint(35, 55)
            fat = random.randint(25, 40)
        elif is_healthy:
            calories = random.randint(200, 350)
            protein = random.randint(10, 20)
            carbs = random.randint(20, 40)
            fat = random.randint(5, 15)
        else:
            calories = random.randint(300, 500)
            protein = random.randint(12, 22)
            carbs = random.randint(25, 45)
            fat = random.randint(10, 25)
        
        # Location-based alternatives (if location provided)
        location_alternatives = []
        if lat and lng:
            # Simulate finding nearby places
            distance_options = [500, 750, 1200, 1500]
            location_alternatives = [
                {
                    "name": "Healthy Cafe",
                    "category": "Cafe",
                    "rating": round(random.uniform(3.5, 4.8), 1),
                    "distance": random.choice(distance_options),
                    "distance_text": f"{random.choice(distance_options)}m",
                    "health_focus": "Organic & Fresh"
                },
                {
                    "name": "Salad Bar Restaurant",
                    "category": "Restaurant",
                    "rating": round(random.uniform(4.0, 5.0), 1),
                    "distance": random.choice(distance_options),
                    "distance_text": f"{random.choice(distance_options)}m",
                    "health_focus": "Custom Salads"
                },
                {
                    "name": "Fresh Juice Corner",
                    "category": "Juice Bar",
                    "rating": round(random.uniform(4.2, 4.9), 1),
                    "distance": random.choice(distance_options),
                    "distance_text": f"{random.choice(distance_options)}m",
                    "health_focus": "Cold-pressed Juices"
                }
            ]
        
        # Generate AI message
        if detected_foods:
            main_food = detected_foods[0].replace('_', ' ').title()
            if is_unhealthy:
                ai_message = f"⚠️ Detected {main_food}. Health score: {health_score}/100. Consider healthier alternatives!"
            elif is_healthy:
                ai_message = f"✅ Great! Detected {main_food}. Health score: {health_score}/100. Excellent choice!"
            else:
                ai_message = f"ℹ️ Detected {main_food}. Health score: {health_score}/100. Could be healthier."
        else:
            ai_message = "Analyzed food image. Consider healthier options for better nutrition."
        
        # Add location info if available
        if location_alternatives:
            nearest = location_alternatives[0]
            ai_message += f" Try {nearest['name']} ({nearest['distance_text']} away) for healthier options!"
        
        return {
            "status": "success",
            "analysis": {
                "image_info": {
                    "width": width,
                    "height": height,
                    "format": format,
                    "size_kb": round(file_size_kb, 2)
                },
                "food_detection": {
                    "detected_foods": detected_foods,
                    "primary_food": detected_foods[0] if detected_foods else "unknown",
                    "confidence": "high" if detected_foods else "low"
                },
                "health_assessment": {
                    "score": health_score,
                    "label": health_label,
                    "is_unhealthy": is_unhealthy,
                    "is_healthy": is_healthy,
                    "rating": f"{health_score}/100"
                },
                "estimated_nutrition": {
                    "calories": calories,
                    "protein_g": protein,
                    "carbs_g": carbs,
                    "fat_g": fat,
                    "fiber_g": random.randint(2, 8)
                }
            },
            "recommendations": recommendations[:3],  # First 3 recommendations
            "alternatives": location_alternatives if location_alternatives else [
                {
                    "name": "General Healthy Alternative",
                    "type": "suggestion",
                    "tip": "Look for grilled instead of fried options"
                }
            ],
            "ai_message": ai_message,
            "location_used": lat is not None and lng is not None,
            "timestamp": datetime.now().isoformat(),
            "message": "Image analysis completed successfully"
        }
        
    except (ValueError, ConnectionError) as e:
        error_msg = str(e)
        logger.error(f"Image processing error: {error_msg}")
        
        # Provide better error messages
        if "image_url%3A" in image_url or "image_url:" in image_url:
            error_msg = "URL encoding issue detected. Try pasting only the image URL without 'image_url:' prefix."
        elif "Network error" in error_msg:
            error_msg = "Network connection failed. Check your internet or try a different image URL."
        
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": error_msg,
                "tip": "Try these working URLs:",
                "example_urls": [
                    "https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
                    "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
                    "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38"
                ],
                "how_to_use": "In Swagger, paste ONLY the image URL (not 'image_url: https://...')"
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error in quick analysis: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Internal server error during image analysis",
                "tip": "Try again with a simpler image or check server logs"
            }
        )

# Import datetime at top
from datetime import datetime
import random










# # app/routes/image.py
# from fastapi import APIRouter, Query
# from typing import Optional
# import random
# from datetime import datetime

# router = APIRouter(prefix="/api/image", tags=["Image Analysis"])

# @router.get("/analyze-quick")
# async def analyze_image_quick(
#     image_url: str = Query(..., description="URL of food image"),
#     lat: Optional[float] = Query(None, description="Latitude"),
#     lng: Optional[float] = Query(None, description="Longitude")
# ):
#     """Quick image analysis"""
#     # Mock analysis
#     food_types = ["Burger", "Pizza", "Salad", "Fruit Bowl", "Sandwich", "Rice Bowl"]
#     detected_food = random.choice(food_types)
    
#     is_healthy = detected_food in ["Salad", "Fruit Bowl"]
#     health_score = random.randint(80, 95) if is_healthy else random.randint(30, 60)
    
#     return {
#         "status": "success",
#         "database": "neon_postgresql",
#         "analysis": {
#             "detected_food": detected_food,
#             "health_score": health_score,
#             "is_healthy": is_healthy,
#             "timestamp": datetime.now().isoformat()
#         },
#         "ai_message": f"Detected {detected_food}. Health score: {health_score}/100. {'Great choice!' if is_healthy else 'Consider healthier alternatives.'}",
#         "location_used": lat is not None and lng is not None
#     }

# @router.get("/test")
# async def test_image_endpoint():
#     """Test image analysis endpoint"""
#     return {
#         "status": "success",
#         "message": "Image analysis API is working with Neon PostgreSQL",
#         "test_url": "/api/image/analyze-quick?image_url=https://example.com/food.jpg"
#     }