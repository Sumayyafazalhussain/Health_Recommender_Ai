
# app/services/rule_engine.py
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class RuleEngine:
    def __init__(self):
        """Initialize Rule Engine"""
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
        
        logger.info("✅ RuleEngine initialized")
    
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
        
        # Not a restaurant, cafe, or gym - ignore it
        logger.debug(f"Ignoring '{name}' - not a restaurant, cafe, or gym")
        return None
    
    def get_recommendations_for_category(self, category_id: str) -> List[str]:
        """Get recommendations - ONLY restaurant, cafe, gym suggestions"""
        # Fallback recommendations if no rule found
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
                
                # Determine if unhealthy
                is_unhealthy = category_id in ['fast_food', 'bar_pub']
                category_name = category_id.replace('_', ' ').title()
                
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

# Create a global instance
rule_engine = RuleEngine()