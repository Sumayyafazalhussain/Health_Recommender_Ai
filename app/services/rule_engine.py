# from typing import Dict, List, Optional
# from app.db.mongo import get_keywords_col, get_rules_col, get_categories_col
# import re
# import logging

# logger = logging.getLogger(__name__)

# class RuleEngine:
#     def __init__(self):
#         """Initialize Rule Engine with real database"""
#         self.keywords_col = get_keywords_col()
#         self.rules_col = get_rules_col()
#         self.categories_col = get_categories_col()
#         logger.info("✅ RuleEngine initialized")
    
#     def detect_category_from_place(self, name: str, types: List[str] = None) -> Optional[str]:
#         """
#         Detect category from place name and types using database keywords
        
#         Args:
#             name: Place name
#             types: Google Place types
        
#         Returns:
#             Category ID or None
#         """
#         if not name:
#             return None
        
#         name_lower = name.lower()
        
#         try:
#             # Get all keywords from database
#             keywords = list(self.keywords_col.find({}))
            
#             # 1. Check keyword matches in name
#             for kw in keywords:
#                 keyword = kw.get("keyword", "").lower()
#                 match_type = kw.get("match_type", "partial")
#                 category_id = kw.get("category_id")
                
#                 if not keyword or not category_id:
#                     continue
                
#                 if match_type == "exact" and keyword == name_lower:
#                     return category_id
#                 elif match_type == "partial" and keyword in name_lower:
#                     return category_id
#                 elif match_type == "type" and types:
#                     for place_type in types:
#                         if keyword == place_type.lower():
#                             return category_id
            
#             # 2. Check Google place types against keywords
#             if types:
#                 for place_type in types:
#                     kw = self.keywords_col.find_one({"keyword": place_type.lower()})
#                     if kw:
#                         return kw.get("category_id")
            
#             # 3. Use regex patterns as fallback
#             fast_food_patterns = [
#                 r'mcdonald', r'burger\s*king', r'kfc', r'wendy',
#                 r'subway', r'taco\s*bell', r'pizza\s*hut', r"domino'?s"
#             ]
            
#             bar_patterns = [
#                 r'\bbar\b', r'\bpub\b', r'tavern', r'lounge',
#                 r'nightclub', r'brewery', r'cocktail'
#             ]
            
#             for pattern in fast_food_patterns:
#                 if re.search(pattern, name_lower, re.IGNORECASE):
#                     return "fast_food"
            
#             for pattern in bar_patterns:
#                 if re.search(pattern, name_lower, re.IGNORECASE):
#                     return "bar"
            
#             return None
            
#         except Exception as e:
#             logger.error(f"Error in detect_category_from_place: {e}")
#             return None
    
#     def get_recommendations_for_category(self, category_id: str) -> List[str]:
#         """Get recommendations for a category from database rules"""
#         try:
#             # Find rule for this category
#             rule = self.rules_col.find_one({"trigger_category_id": category_id})
#             if not rule:
#                 rule = self.rules_col.find_one({"trigger": category_id})
            
#             if rule:
#                 recommended_ids = rule.get("recommended_category_ids") or rule.get("recommend", [])
                
#                 # Get category names
#                 recommendations = []
#                 for cat_id in recommended_ids:
#                     category = self.categories_col.find_one({"id": cat_id}) or \
#                                self.categories_col.find_one({"_id": cat_id})
#                     if category:
#                         recommendations.append(category.get("name", cat_id))
                
#                 return recommendations
            
#             return []
            
#         except Exception as e:
#             logger.error(f"Error in get_recommendations_for_category: {e}")
#             return []
    
#     def get_recommended_category_names(self, category_id: str) -> List[str]:
#         """Get recommended category names for a trigger category"""
#         try:
#             # Find rule for this category
#             rule = self.rules_col.find_one({"trigger_category_id": category_id})
#             if not rule:
#                 rule = self.rules_col.find_one({"trigger": category_id})
            
#             if rule:
#                 recommended_ids = rule.get("recommended_category_ids") or rule.get("recommend", [])
                
#                 # Get category names
#                 category_names = []
#                 for cat_id in recommended_ids:
#                     category = self.categories_col.find_one({"id": cat_id}) or \
#                                self.categories_col.find_one({"_id": cat_id})
#                     if category:
#                         category_names.append(category.get("name", ""))
                
#                 # Filter out empty names and return
#                 return [name for name in category_names if name]
            
#             return []
            
#         except Exception as e:
#             logger.error(f"Error in get_recommended_category_names: {e}")
#             return []
    
#     def analyze_place(self, name: str, types: List[str] = None) -> Dict:
#         """
#         Analyze a place and return recommendations if needed
        
#         Returns:
#             Dictionary with analysis results
#         """
#         try:
#             category_id = self.detect_category_from_place(name, types)
            
#             if category_id:
#                 recommendations = self.get_recommendations_for_category(category_id)
                
#                 # Get category name
#                 category = self.categories_col.find_one({"id": category_id}) or \
#                            self.categories_col.find_one({"_id": category_id})
#                 category_name = category.get("name", category_id) if category else category_id
                
#                 return {
#                     "triggered": True,
#                     "category_id": category_id,
#                     "category_name": category_name,
#                     "recommendations": recommendations
#                 }
            
#             return {"triggered": False}
            
#         except Exception as e:
#             logger.error(f"Error in analyze_place: {e}")
#             return {"triggered": False}
    
#     def get_recommended_categories_for_trigger(self, trigger_category_id: str) -> List[str]:
#         """Get recommended category IDs for a trigger category"""
#         try:
#             rule = self.rules_col.find_one({"trigger_category_id": trigger_category_id})
#             if not rule:
#                 rule = self.rules_col.find_one({"trigger": trigger_category_id})
            
#             if rule:
#                 return rule.get("recommended_category_ids", []) or rule.get("recommend", [])
            
#             return []
            
#         except Exception as e:
#             logger.error(f"Error in get_recommended_categories_for_trigger: {e}")
#             return []





# from typing import Dict, List, Optional
# from app.db.mongo import get_keywords_col, get_rules_col, get_categories_col
# import re
# import logging

# logger = logging.getLogger(__name__)

# class RuleEngine:
#     def __init__(self):
#         """Initialize Rule Engine"""
#         self.keywords_col = get_keywords_col()
#         self.rules_col = get_rules_col()
#         self.categories_col = get_categories_col()
        
#         # EXCLUDE these place types (NOT restaurants, cafes, gyms)
#         self.excluded_types = [
#             'locality', 'political', 'hospital', 'clinic', 'health', 
#             'shopping_mall', 'store', 'school', 'university', 'office',
#             'company', 'bank', 'atm', 'parking', 'cemetery', 'church',
#             'mosque', 'temple', 'government', 'post_office', 'library'
#         ]
        
#         # ONLY detect these categories
#         self.target_categories = {
#             'fast_food': ['mcdonald', 'kfc', 'burger king', 'pizza', 'subway',
#                          'fast food', 'fried chicken', 'shwarma', 'burger'],
#             'restaurant': ['restaurant', 'food', 'diner', 'eatery', 'bistro'],
#             'cafe': ['cafe', 'coffee', 'starbucks', 'coffee shop', 'espresso'],
#             'gym': ['gym', 'fitness', 'workout', 'exercise', 'yoga'],
#             'bar_pub': ['bar', 'pub', 'nightclub', 'lounge', 'brewery']
#         }
        
#         logger.info("✅ RuleEngine - ONLY restaurants, cafes, gyms")
    
#     def detect_category_from_place(self, name: str, types: List[str] = None) -> Optional[str]:
#         """
#         ONLY detect restaurants, cafes, gyms - ignore everything else
#         """
#         if not name:
#             return None
        
#         name_lower = name.lower()
        
#         # 1. FIRST: Check if place has excluded types
#         if types:
#             for excluded_type in self.excluded_types:
#                 if excluded_type in types:
#                     logger.debug(f"Ignoring '{name}' - has excluded type: {excluded_type}")
#                     return None
        
#         # 2. Check for target categories
#         for category_id, keywords in self.target_categories.items():
#             for keyword in keywords:
#                 if keyword in name_lower:
#                     logger.debug(f"Detected '{keyword}' in '{name}' -> {category_id}")
#                     return category_id
        
#         # 3. Check place types (only food/gym related)
#         if types:
#             type_mapping = {
#                 'restaurant': 'restaurant',
#                 'food': 'restaurant',
#                 'meal_takeaway': 'fast_food',
#                 'cafe': 'cafe',
#                 'gym': 'gym',
#                 'bar': 'bar_pub',
#                 'night_club': 'bar_pub'
#             }
            
#             for place_type in types:
#                 if place_type in type_mapping:
#                     return type_mapping[place_type]
        
#         # 4. Database keywords (only for target categories)
#         try:
#             keywords = list(self.keywords_col.find({}))
#             for kw in keywords:
#                 keyword = kw.get("keyword", "").lower()
#                 category_id = kw.get("category_id")
                
#                 # Only check for our target categories
#                 if (keyword and category_id and keyword in name_lower and 
#                     category_id in ['fast_food', 'restaurant', 'cafe', 'gym', 'bar_pub']):
#                     return category_id
#         except:
#             pass
        
#         # Not a restaurant, cafe, or gym - ignore it
#         logger.debug(f"Ignoring '{name}' - not a restaurant, cafe, or gym")
#         return None
    
#     def get_recommendations_for_category(self, category_id: str) -> List[str]:
#         """Get recommendations - ONLY restaurant, cafe, gym suggestions"""
#         # Recommendations map (only food/gym places)
#         recommendations_map = {
#             'fast_food': ['Healthy Cafe', 'Fresh Juice Bar', 'Salad Restaurant', 'Vegetarian Cafe'],
#             'restaurant': ['Healthy Restaurant', 'Salad Bar', 'Fresh Juice Cafe', 'Vegetarian Place'],
#             'cafe': ['Healthy Cafe', 'Fresh Juice Bar', 'Salad Restaurant'],
#             'gym': ['Protein Cafe', 'Healthy Restaurant', 'Smoothie Bar'],
#             'bar_pub': ['Coffee Shop', 'Healthy Cafe', 'Gym', 'Juice Bar']
#         }
        
#         return recommendations_map.get(category_id, ['Healthy Cafe', 'Fresh Juice', 'Salad Restaurant'])
    
#     def analyze_place(self, name: str, types: List[str] = None) -> Dict:
#         """Analyze place - ONLY for restaurants, cafes, gyms"""
#         try:
#             category_id = self.detect_category_from_place(name, types)
            
#             if category_id:
#                 recommendations = self.get_recommendations_for_category(category_id)
                
#                 # Get category name
#                 category = self.categories_col.find_one({"_id": category_id})
#                 category_name = category.get("name", category_id) if category else category_id
                
#                 # Determine if unhealthy
#                 is_unhealthy = category_id in ['fast_food', 'bar_pub']
                
#                 return {
#                     "triggered": True,
#                     "category_id": category_id,
#                     "category_name": category_name,
#                     "recommendations": recommendations,
#                     "is_unhealthy": is_unhealthy
#                 }
            
#             return {"triggered": False}
            
#         except Exception as e:
#             logger.error(f"Error analyzing place: {e}")
#             return {"triggered": False}


from typing import Dict, List, Optional
from app.db.mongo import get_keywords_col, get_rules_col, get_categories_col
import re
import logging

logger = logging.getLogger(__name__)

class RuleEngine:
    def __init__(self):
        """Initialize Rule Engine"""
        self.keywords_col = get_keywords_col()
        self.rules_col = get_rules_col()
        self.categories_col = get_categories_col()
        
        # EXCLUDE these place types (NOT restaurants, cafes, gyms)
        self.excluded_types = [
            'locality', 'political', 'hospital', 'clinic', 'health', 
            'shopping_mall', 'store', 'school', 'university', 'office',
            'company', 'bank', 'atm', 'parking', 'cemetery', 'church',
            'mosque', 'temple', 'government', 'post_office', 'library'
        ]
        
        # ONLY detect these categories
        self.target_categories = {
            'fast_food': ['mcdonald', 'kfc', 'burger king', 'pizza', 'subway',
                         'fast food', 'fried chicken', 'shwarma', 'burger', 
                         'krunchy', 'karachy', 'bbq', 'fried'],
            'restaurant': ['restaurant', 'food', 'diner', 'eatery', 'bistro', 'hotel'],
            'cafe': ['cafe', 'coffee', 'starbucks', 'coffee shop', 'espresso', 
                    'tea shop', 'juice', 'sandwich'],
            'gym': ['gym', 'fitness', 'workout', 'exercise', 'yoga', 'muscle', 'club'],
            'bar_pub': ['bar', 'pub', 'nightclub', 'lounge', 'brewery', 'wine']
        }
        
        logger.info("✅ RuleEngine - ONLY restaurants, cafes, gyms")
    
    def detect_category_from_place(self, name: str, types: List[str] = None) -> Optional[str]:
        """
        ONLY detect restaurants, cafes, gyms - ignore everything else
        """
        if not name:
            return None
        
        name_lower = name.lower()
        
        # 1. FIRST: Check if place has excluded types
        if types:
            for excluded_type in self.excluded_types:
                if excluded_type in types:
                    logger.debug(f"Ignoring '{name}' - has excluded type: {excluded_type}")
                    return None
        
        # 2. Check for target categories
        for category_id, keywords in self.target_categories.items():
            for keyword in keywords:
                if keyword in name_lower:
                    logger.debug(f"Detected '{keyword}' in '{name}' -> {category_id}")
                    return category_id
        
        # 3. Check place types (only food/gym related)
        if types:
            type_mapping = {
                'restaurant': 'restaurant',
                'food': 'restaurant',
                'meal_takeaway': 'fast_food',
                'cafe': 'cafe',
                'gym': 'gym',
                'bar': 'bar_pub',
                'night_club': 'bar_pub'
            }
            
            for place_type in types:
                if place_type in type_mapping:
                    return type_mapping[place_type]
        
        # 4. Database keywords (only for target categories)
        try:
            keywords = list(self.keywords_col.find({}))
            for kw in keywords:
                keyword = kw.get("keyword", "").lower()
                category_id = kw.get("category_id")
                
                # Only check for our target categories
                if (keyword and category_id and keyword in name_lower and 
                    category_id in ['fast_food', 'restaurant', 'cafe', 'gym', 'bar_pub']):
                    return category_id
        except:
            pass
        
        # Not a restaurant, cafe, or gym - ignore it
        logger.debug(f"Ignoring '{name}' - not a restaurant, cafe, or gym")
        return None
    
    def get_recommendations_for_category(self, category_id: str) -> List[str]:
        """Get recommendations - ONLY restaurant, cafe, gym suggestions"""
        # Recommendations map (only food/gym places)
        recommendations_map = {
            'fast_food': ['Healthy Cafe', 'Fresh Juice Bar', 'Salad Restaurant', 'Vegetarian Cafe'],
            'restaurant': ['Healthy Restaurant', 'Salad Bar', 'Fresh Juice Cafe', 'Vegetarian Place'],
            'cafe': ['Healthy Cafe', 'Fresh Juice Bar', 'Salad Restaurant'],
            'gym': ['Protein Cafe', 'Healthy Restaurant', 'Smoothie Bar'],
            'bar_pub': ['Coffee Shop', 'Healthy Cafe', 'Gym', 'Juice Bar']
        }
        
        return recommendations_map.get(category_id, ['Healthy Cafe', 'Fresh Juice', 'Salad Restaurant'])
    
    def analyze_place(self, name: str, types: List[str] = None) -> Dict:
        """Analyze place - ONLY for restaurants, cafes, gyms"""
        try:
            category_id = self.detect_category_from_place(name, types)
            
            if category_id:
                recommendations = self.get_recommendations_for_category(category_id)
                
                # Get category name
                category = self.categories_col.find_one({"_id": category_id})
                category_name = category.get("name", category_id) if category else category_id
                
                # Determine if unhealthy
                is_unhealthy = category_id in ['fast_food', 'bar_pub']
                
                return {
                    "triggered": True,
                    "category_id": category_id,
                    "category_name": category_name,
                    "recommendations": recommendations,
                    "is_unhealthy": is_unhealthy
                }
            
            return {"triggered": False}
            
        except Exception as e:
            logger.error(f"Error analyzing place: {e}")
            return {"triggered": False}