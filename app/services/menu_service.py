# from typing import Dict, List, Optional, Any
# import logging
# from app.db.mongo import get_menus_col
# import googlemaps
# from app.config import settings
# from datetime import datetime, timedelta
# import re
# import asyncio
# import aiohttp

# logger = logging.getLogger(__name__)

# class MenuService:
#     def __init__(self):
#         self.gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY) if settings.GOOGLE_API_KEY else None
#         self.menus_col = get_menus_col()
        
#         # Google Cloud Vision (optional)
#         self.use_vision = False
#         try:
#             from google.cloud import vision
#             self.vision_client = vision.ImageAnnotatorClient()
#             self.use_vision = True
#             logger.info("✅ Google Cloud Vision initialized")
#         except ImportError:
#             logger.warning("Google Cloud Vision not installed - photo OCR will be disabled")
#         except Exception as e:
#             logger.warning(f"Google Cloud Vision initialization failed: {e}")
        
#         logger.info("✅ MenuService initialized")
    
#     async def get_menu_for_place(self, place_id: str, place_name: str = "") -> Optional[Dict[str, Any]]:
#         """
#         Get REAL menu data from Google - ACTUAL data only
#         """
#         try:
#             # 1. Check cache (12 hours only for freshness)
#             cached_menu = self.menus_col.find_one({"place_id": place_id})
#             if cached_menu:
#                 last_updated = cached_menu.get('last_updated')
#                 if last_updated:
#                     cache_date = last_updated if isinstance(last_updated, datetime) else datetime.fromisoformat(str(last_updated))
#                     if datetime.now() - cache_date < timedelta(hours=12):
#                         cached_menu["_id"] = str(cached_menu["_id"])
#                         if cached_menu.get('has_actual_data', False):
#                             return cached_menu
            
#             # 2. Fetch fresh REAL data
#             menu_data = await self._fetch_real_google_data(place_id, place_name)
            
#             # 3. Save only if we got ACTUAL data
#             if menu_data and menu_data.get('has_actual_data', False):
#                 menu_data['place_id'] = place_id
#                 menu_data['place_name'] = place_name
#                 menu_data['last_updated'] = datetime.now()
                
#                 self.menus_col.update_one(
#                     {"place_id": place_id},
#                     {"$set": menu_data},
#                     upsert=True
#                 )
                
#                 saved_menu = self.menus_col.find_one({"place_id": place_id})
#                 if saved_menu:
#                     saved_menu["_id"] = str(saved_menu["_id"])
                
#                 logger.info(f"✅ Saved REAL menu data for: {place_name}")
#                 return saved_menu
            
#             # 4. No actual data found
#             logger.info(f"⚠️  No actual menu data found for: {place_name}")
#             return None
            
#         except Exception as e:
#             logger.error(f"Error getting menu for {place_name}: {e}")
#             return None
    
#     async def _fetch_real_google_data(self, place_id: str, place_name: str) -> Optional[Dict[str, Any]]:
#         """
#         Fetch ACTUAL data from Google Places API
#         """
#         try:
#             if not self.gmaps:
#                 return None
            
#             logger.info(f"🔍 Fetching Google data for: {place_name}")
            
#             # Get comprehensive place data
#             place_details = self.gmaps.place(
#                 place_id=place_id,
#                 fields=[
#                     'name', 'website', 'formatted_phone_number', 
#                     'price_level', 'reviews', 'rating',
#                     'user_ratings_total', 'formatted_address',
#                     'url', 'opening_hours', 'types',
#                     'photos', 'editorial_summary'
#                 ]
#             )
            
#             result = place_details.get('result', {})
            
#             if not result:
#                 return {'has_actual_data': False, 'message': 'No data from Google'}
            
#             # Extract ACTUAL menu items from reviews
#             reviews = result.get('reviews', [])
#             actual_items = self._extract_actual_items_from_reviews(reviews)
            
#             # Check website for menu
#             website_items = []
#             website = result.get('website')
#             if website:
#                 website_items = await self._check_website_for_menu(website, place_name)
            
#             # Combine all actual items
#             all_actual_items = actual_items + website_items
            
#             # Build response
#             menu_data: Dict[str, Any] = {
#                 'place_name': result.get('name', place_name),
#                 'address': result.get('formatted_address'),
#                 'rating': result.get('rating'),
#                 'total_reviews': result.get('user_ratings_total'),
#                 'website': result.get('website'),
#                 'phone': result.get('formatted_phone_number'),
#                 'price_level': result.get('price_level'),
#                 'google_url': result.get('url'),
#                 'place_types': result.get('types', []),
#                 'has_actual_data': bool(all_actual_items),
#                 'last_updated': datetime.now()
#             }
            
#             if all_actual_items:
#                 menu_data.update({
#                     'source': 'google_actual_data',
#                     'menu_items': all_actual_items,
#                     'total_actual_items': len(all_actual_items),
#                     'data_sources': {
#                         'from_reviews': len(actual_items),
#                         'from_website': len(website_items)
#                     }
#                 })
                
#                 # Add food-related review snippets
#                 food_reviews = self._extract_food_reviews(reviews)
#                 if food_reviews:
#                     menu_data['food_reviews'] = food_reviews
#             else:
#                 menu_data.update({
#                     'source': 'google_basic_only',
#                     'message': 'No actual menu items found in Google data'
#                 })
            
#             return menu_data
            
#         except Exception as e:
#             logger.error(f"Error fetching Google data: {e}")
#             return {'has_actual_data': False, 'error': str(e)}
    
#     def _extract_actual_items_from_reviews(self, reviews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         """
#         Extract ACTUAL menu items mentioned in Google reviews
#         """
#         if not reviews:
#             return []
        
#         menu_items = []
#         item_counter = {}
        
#         # Enhanced patterns for Pakistani restaurant reviews
#         patterns = [
#             # Pattern 1: "ordered Chicken Biryani for Rs. 350"
#             r'(?:ordered|ate|tried|had|got|took|bought)\s+(?:the\s+)?([A-Za-z\s\-]{3,50}?)\s+(?:for|@|was|is)\s*(?:Rs\.?|PKR|₹|price\s*:?)\s*(\d+)',
            
#             # Pattern 2: "Chicken Biryani Rs. 350"
#             r'([A-Za-z\s\-]{3,50}?)\s*(?:Rs\.?|PKR|₹)\s*(\d+)',
            
#             # Pattern 3: "tried the mutton karahi" (without price)
#             r'\b(?:tried|had|ordered|ate|got|recommend|recommended|love|loved|enjoyed)\s+(?:the\s+)?([A-Za-z\s\-]{3,50}?)\b',
            
#             # Pattern 4: Price at the beginning "Rs. 350 for Chicken Biryani"
#             r'(?:Rs\.?|PKR|₹)\s*(\d+)\s+(?:for|of)\s+([A-Za-z\s\-]{3,50}?)',
#         ]
        
#         for review in reviews:
#             text = review.get('text', '').lower()
#             rating = review.get('rating', 0)
#             time = review.get('time', 0)
            
#             # Skip reviews older than 2 years
#             import time as time_module
#             if time_module.time() - time > 63072000:  # 2 years
#                 continue
            
#             for pattern in patterns:
#                 matches = re.finditer(pattern, text, re.IGNORECASE)
#                 for match in matches:
#                     if match.lastindex >= 1:
#                         # Determine which groups contain item name and price
#                         groups = match.groups()
#                         if len(groups) == 2:
#                             # Pattern with price
#                             if 'Rs' in match.group(0) or 'PKR' in match.group(0) or '₹' in match.group(0):
#                                 # Price mentioned in the match
#                                 if pattern == patterns[3]:  # Price first pattern
#                                     price = groups[0]
#                                     item_name = groups[1]
#                                 else:
#                                     item_name = groups[0]
#                                     price = groups[1]
#                             else:
#                                 item_name = groups[0]
#                                 price = groups[1] if len(groups) > 1 else None
#                         else:
#                             item_name = groups[0]
#                             price = None
                        
#                         if item_name:
#                             item_name = self._clean_item_name(item_name)
                            
#                             if self._is_valid_menu_item(item_name):
#                                 # Create menu item
#                                 menu_item = {
#                                     'name': item_name.title(),
#                                     'source': 'google_review',
#                                     'review_rating': rating,
#                                     'is_actual_data': True,
#                                     'data_confidence': 'high' if price else 'medium'
#                                 }
                                
#                                 if price and price.isdigit():
#                                     menu_item['price'] = int(price)
#                                     menu_item['has_price'] = True
                                
#                                 # Track frequency
#                                 key = item_name.lower()
#                                 if key in item_counter:
#                                     item_counter[key]['count'] += 1
#                                     if price and price.isdigit() and not item_counter[key].get('has_price'):
#                                         item_counter[key]['price'] = int(price)
#                                         item_counter[key]['has_price'] = True
#                                 else:
#                                     item_counter[key] = {
#                                         'item': menu_item,
#                                         'count': 1
#                                     }
        
#         # Convert counter to list and sort by frequency
#         for key, data in item_counter.items():
#             item = data['item']
#             item['mention_count'] = data['count']
#             menu_items.append(item)
        
#         # Sort by mention count
#         menu_items.sort(key=lambda x: x.get('mention_count', 0), reverse=True)
        
#         return menu_items[:20]
    
#     async def _check_website_for_menu(self, url: str, place_name: str) -> List[Dict[str, Any]]:
#         """
#         Check restaurant website for menu information
#         """
#         try:
#             headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#             }
            
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url, headers=headers, timeout=8) as response:
#                     if response.status == 200:
#                         html = await response.text()
                        
#                         # Simple text extraction
#                         import re
                        
#                         # Look for menu items with prices
#                         text = html.lower()
                        
#                         # Common Pakistani menu patterns
#                         menu_patterns = [
#                             r'([a-z\s]{3,40}?)\s*(?:rs\.?|pkr|₹)\s*(\d+)',
#                             r'price\s*:?\s*(?:rs\.?|pkr|₹)\s*(\d+)[^<]*?([a-z\s]{3,40})',
#                         ]
                        
#                         items = []
#                         for pattern in menu_patterns:
#                             matches = re.findall(pattern, text, re.IGNORECASE)
#                             for match in matches:
#                                 if len(match) == 2:
#                                     item_name = match[0].strip() if match[0] else match[1].strip()
#                                     price = match[1] if match[1].isdigit() else match[0]
                                    
#                                     if item_name and price and price.isdigit():
#                                         items.append({
#                                             'name': item_name.title(),
#                                             'price': int(price),
#                                             'source': 'website',
#                                             'is_actual_data': True,
#                                             'has_price': True,
#                                             'data_confidence': 'medium'
#                                         })
                        
#                         return items[:10]
            
#             return []
            
#         except Exception as e:
#             logger.debug(f"Website check failed for {url}: {e}")
#             return []
    
#     def _extract_food_reviews(self, reviews: List[Dict[str, Any]]) -> List[str]:
#         """Extract food-related review snippets"""
#         food_keywords = ['food', 'dish', 'meal', 'taste', 'flavor', 'delicious',
#                         'spicy', 'sweet', 'fresh', 'cooked', 'served', 'portion',
#                         'biryani', 'karahi', 'tikka', 'kebab', 'curry', 'naan']
        
#         food_reviews = []
#         for review in reviews[:5]:
#             text = review.get('text', '')
#             if any(keyword in text.lower() for keyword in food_keywords):
#                 # Take meaningful snippet
#                 snippet = text[:120] + '...' if len(text) > 120 else text
#                 food_reviews.append(snippet)
        
#         return food_reviews
    
#     def _clean_item_name(self, item_name: str) -> str:
#         """Clean item name"""
#         # Remove extra words
#         remove_words = ['the', 'a', 'an', 'and', 'or', 'but', 'for', 'with',
#                        'very', 'really', 'quite', 'too', 'so', 'just']
        
#         words = item_name.split()
#         cleaned_words = []
        
#         for word in words:
#             word_lower = word.lower()
#             if word_lower not in remove_words and len(word_lower) > 1:
#                 cleaned_words.append(word)
        
#         cleaned = ' '.join(cleaned_words)
#         # Remove special characters
#         cleaned = re.sub(r'[^\w\s\-]', '', cleaned)
        
#         return cleaned.strip()
    
#     def _is_valid_menu_item(self, item_name: str) -> bool:
#         """Check if text looks like a valid menu item"""
#         if len(item_name) < 3 or len(item_name) > 50:
#             return False
        
#         # Common non-menu words
#         non_menu_words = ['service', 'staff', 'ambience', 'place', 'restaurant',
#                          'experience', 'management', 'owner', 'waiter', 'clean',
#                          'atmosphere', 'location', 'parking', 'price', 'bill',
#                          'overall', 'definitely', 'probably', 'maybe']
        
#         item_lower = item_name.lower()
#         if any(word in item_lower for word in non_menu_words):
#             return False
        
#         # Should contain letters
#         if not any(c.isalpha() for c in item_name):
#             return False
        
#         # Check for common menu item patterns
#         menu_patterns = [
#             r'.*biryani.*', r'.*karahi.*', r'.*tikka.*', r'.*kebab.*',
#             r'.*curry.*', r'.*naan.*', r'.*roti.*', r'.*rice.*',
#             r'.*soup.*', r'.*salad.*', r'.*burger.*', r'.*pizza.*',
#             r'.*pasta.*', r'.*sandwich.*', r'.*juice.*', r'.*shake.*',
#             r'.*tea.*', r'.*coffee.*', r'.*water.*', r'.*soda.*'
#         ]
        
#         for pattern in menu_patterns:
#             if re.match(pattern, item_lower):
#                 return True
        
#         # If it has at least 2 words and looks reasonable
#         words = item_name.split()
#         return len(words) >= 1 and len(words) <= 5
    
#     def get_top_menu_items(self, menu_data: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
#         """Get top actual menu items"""
#         if not menu_data or not menu_data.get('menu_items'):
#             return []
        
#         items = menu_data['menu_items']
        
#         # Filter for actual data
#         actual_items = [item for item in items if item.get('is_actual_data', False)]
        
#         if not actual_items:
#             return []
        
#         # Sort by mention count and price availability
#         sorted_items = sorted(actual_items,
#                             key=lambda x: (
#                                 x.get('mention_count', 0),
#                                 1 if x.get('has_price') else 0,
#                                 x.get('review_rating', 0)
#                             ),
#                             reverse=True)
        
#         return sorted_items[:limit]
    
#     def format_menu_for_display(self, menu_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Format menu for API response"""
#         if not menu_data:
#             return {
#                 'available': False,
#                 'is_actual_data': False,
#                 'message': 'No data available'
#             }
        
#         has_actual = menu_data.get('has_actual_data', False)
        
#         formatted = {
#             'available': has_actual,
#             'is_actual_data': has_actual,
#             'place_name': menu_data.get('place_name', ''),
#             'source': menu_data.get('source', 'unknown'),
#             'rating': menu_data.get('rating'),
#             'total_reviews': menu_data.get('total_reviews'),
#             'address': menu_data.get('address'),
#         }
        
#         if menu_data.get('price_level') is not None:
#             formatted['price_level'] = menu_data['price_level']
        
#         if menu_data.get('website'):
#             formatted['website'] = menu_data['website']
        
#         if menu_data.get('phone'):
#             formatted['phone'] = menu_data['phone']
        
#         # Add actual menu items if available
#         top_items = self.get_top_menu_items(menu_data, 6)
#         if top_items:
#             formatted['top_items'] = top_items
#             formatted['total_actual_items'] = len(top_items)
            
#             # Add price stats
#             priced_items = [item for item in top_items if item.get('price')]
#             if priced_items:
#                 prices = [item['price'] for item in priced_items]
#                 formatted['price_stats'] = {
#                     'min': min(prices),
#                     'max': max(prices),
#                     'avg': sum(prices) // len(prices)
#                 }
        
#         # Add food reviews if available
#         if menu_data.get('food_reviews'):
#             formatted['food_reviews'] = menu_data['food_reviews'][:3]
        
#         return formatted

# # Singleton instance
# menu_service = MenuService()


















# import asyncio
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# async def test_photo_menu():
#     from app.services.google_service import google_service
#     from app.services.menu_service import menu_service
    
#     # Test coordinates
#     lat, lng = 24.8607, 67.0011
    
#     print("🔍 Testing Photo Menu Detection")
#     print("=" * 60)
    
#     try:
#         # Get nearby places
#         places = google_service.get_nearby_places(lat, lng, radius=1000)
        
#         if not places:
#             print("No places found")
#             return
        
#         print(f"Found {len(places)} places")
        
#         # Find places with photos
#         places_with_photos = []
#         for place in places[:5]:
#             if place.get('photos'):
#                 places_with_photos.append(place)
        
#         print(f"\nPlaces with photos: {len(places_with_photos)}")
        
#         # Test photo extraction
#         for i, place in enumerate(places_with_photos[:2], 1):
#             place_name = place.get('name', 'Unknown')
#             place_id = place.get('place_id')
#             photos = place.get('photos', [])
            
#             print(f"\n{i}. {place_name}")
#             print(f"   Photos available: {len(photos)}")
            
#             if place_id:
#                 menu = await menu_service.get_menu_for_place(place_id, place_name)
                
#                 if menu:
#                     print(f"   ✅ Menu data retrieved")
                    
#                     if menu.get('has_photos'):
#                         print(f"   📸 Has photos: Yes")
                        
#                         if menu.get('photo_menu_detected'):
#                             print(f"   ✅ Menu detected in photos!")
#                             items_from_photos = menu.get('menu_items_from_photos', 0)
#                             print(f"   Items from photos: {items_from_photos}")
#                         else:
#                             print(f"   ⚠️  No menu detected in photos")
                    
#                     # Show items
#                     top_items = menu_service.get_top_menu_items(menu, 3)
#                     if top_items:
#                         print(f"   Top menu items:")
#                         for j, item in enumerate(top_items, 1):
#                             source = item.get('source', 'unknown')
#                             price = f"Rs. {item['price']}" if item.get('price') else "Price N/A"
#                             print(f"     {j}. {item['name']} - {price} ({source})")
#                 else:
#                     print(f"   ❌ No menu data")
        
#     except Exception as e:
#         print(f"❌ Error: {e}")

# if __name__ == "__main__":
#     asyncio.run(test_photo_menu())





import re
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional

class MenuService:
    def __init__(self):
        self.common_menu_keywords = [
            'burger', 'pizza', 'pasta', 'biryani', 'karahi', 'tikka', 'roll',
            'sandwich', 'salad', 'soup', 'rice', 'naan', 'roti', 'chicken',
            'beef', 'mutton', 'fish', 'vegetable', 'dessert', 'ice cream',
            'drink', 'juice', 'coffee', 'tea'
        ]
    
    def extract_menu_from_website(self, url: str) -> Dict[str, Any]:
        """Try to extract menu items from a restaurant website"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find menu-related sections
                menu_items = []
                
                # Look for common menu patterns
                menu_patterns = [
                    {'tag': 'div', 'class': ['menu', 'menu-item', 'food-item']},
                    {'tag': 'li', 'class': ['item', 'product', 'food']},
                    {'tag': 'tr', 'class': ['menu-row']},
                    {'tag': 'section', 'id': ['menu', 'food-menu']}
                ]
                
                for pattern in menu_patterns:
                    elements = soup.find_all(pattern['tag'], class_=pattern.get('class'))
                    for elem in elements:
                        text = elem.get_text(strip=True)
                        if text and len(text) < 100:  # Reasonable menu item length
                            # Check if it contains food-related keywords
                            if any(keyword in text.lower() for keyword in self.common_menu_keywords):
                                menu_items.append(text)
                
                # Also look for prices
                price_items = []
                price_pattern = re.compile(r'Rs\.?\s*\d+|\$\s*\d+|\d+\s*(RS|rs|Rupees)', re.IGNORECASE)
                price_elements = soup.find_all(text=price_pattern)
                
                for elem in price_elements:
                    price_items.append(elem.strip())
                
                return {
                    'success': True,
                    'menu_items': list(set(menu_items[:20])),  # Limit to 20 unique items
                    'price_references': list(set(price_items[:10])),
                    'website': url
                }
        
        except Exception as e:
            print(f"Error extracting menu from {url}: {e}")
        
        return {
            'success': False,
            'menu_items': [],
            'price_references': [],
            'website': url
        }
    
    def get_menu_from_place(self, place_details: Dict) -> Dict[str, Any]:
        """Get menu information from place details"""
        menu_data = {
            'has_menu': False,
            'menu_source': 'none',
            'menu_items': [],
            'menu_url': '',
            'price_range': ''
        }
        
        # Check website for menu
        website = place_details.get('website', '')
        if website:
            extracted_menu = self.extract_menu_from_website(website)
            if extracted_menu['success'] and extracted_menu['menu_items']:
                menu_data['has_menu'] = True
                menu_data['menu_source'] = 'website_scraped'
                menu_data['menu_items'] = extracted_menu['menu_items']
                menu_data['menu_url'] = website
        
        # Check if it's a known chain
        place_name = place_details.get('name', '').lower()
        known_chains = {
            'kfc': ['chicken bucket', 'zinger burger', 'twister', 'popcorn chicken'],
            'mcdonald': ['big mac', 'mcchicken', 'fries', 'happy meal'],
            'burger king': ['whopper', 'chicken royale', 'fries', 'onion rings'],
            'pizza hut': ['pizza', 'pasta', 'garlic bread', 'wings'],
            'domino': ['pizza', 'garlic bread', 'pasta', 'wings'],
            'subway': ['sub', 'sandwich', 'cookies', 'salad']
        }
        
        for chain, items in known_chains.items():
            if chain in place_name:
                menu_data['has_menu'] = True
                menu_data['menu_source'] = 'known_chain'
                menu_data['menu_items'] = items
                break
        
        # Determine price range from price_level
        price_level = place_details.get('price_level')
        price_map = {
            0: 'Free',
            1: 'Inexpensive',
            2: 'Moderate',
            3: 'Expensive',
            4: 'Very Expensive'
        }
        if price_level is not None:
            menu_data['price_range'] = price_map.get(price_level, 'Unknown')
        
        return menu_data