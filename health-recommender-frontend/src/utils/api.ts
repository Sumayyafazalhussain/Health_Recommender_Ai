import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
});

export interface DetectedPlace {
  name: string;
  rating: number | string;
  vicinity: string;
  types: string[];
  category: string;
  category_id: string;
  is_unhealthy: boolean;
  price_level: string;
  place_id: string;
}

export interface AlternativePlace {
  name: string;
  category: string;
  rating: number | string;
  vicinity: string;
  distance: number;
  distance_text: string;
  price_level: string;
  types?: string[];
}

export interface RecommendationResponse {
  status: string;
  detected_place: DetectedPlace;
  recommendations: string[];
  healthy_alternatives: AlternativePlace[];
  ai_message: string;
  total_places_found: number;
}

export const apiService = {
  async healthCheck(): Promise<{ status: string }> {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch {
      return { status: 'disconnected' };
    }
  },

  async getRecommendations(lat: number, lng: number, radius: number = 1000): Promise<RecommendationResponse> {
    try {
      console.log(`🌐 Calling REAL backend: ${API_BASE_URL}/api/api/recommend`);
      
      const response = await apiClient.get('/api/api/recommend', {
        params: {
          lat,
          lng,
          radius,
          include_locations: true
        }
      });
      
      console.log('✅ REAL DATA RECEIVED:', response.data);
      return response.data;
      
    } catch (error: any) {
      console.error('❌ Backend error:', error);
      
      // Try direct endpoint if /api/api/recommend fails
      try {
        const response = await apiClient.get('/api/recommend', {
          params: { lat, lng, radius, include_locations: true }
        });
        return response.data;
      } catch {
        // Return demo data only if both endpoints fail
        return getDemoData(lat, lng);
      }
    }
  }
};

function getDemoData(lat: number, lng: number): RecommendationResponse {
  return {
    status: "demo_mode",
    detected_place: {
      name: "Demo Restaurant",
      rating: 3.5,
      vicinity: "Demo Street",
      types: ["restaurant", "fast_food"],
      category: "Fast Food",
      category_id: "fast_food",
      is_unhealthy: true,
      price_level: "$$",
      place_id: "demo_1"
    },
    recommendations: ["Healthy Cafe", "Fresh Juice Bar", "Salad Restaurant"],
    healthy_alternatives: [
      {
        name: "Green Leaf Cafe",
        category: "Cafe",
        rating: 4.5,
        vicinity: "123 Healthy Street",
        distance: 500,
        distance_text: "500m",
        price_level: "$$"
      },
      {
        name: "Fresh Juice Bar",
        category: "Juice Bar",
        rating: 4.8,
        vicinity: "456 Wellness Road",
        distance: 800,
        distance_text: "800m",
        price_level: "$"
      }
    ],
    ai_message: "This is demo data. Backend not connected.",
    total_places_found: 2
  };
}

export const getCoordinatesForCity = (city: string): { lat: number; lng: number } => {
  const cities: { [key: string]: { lat: number; lng: number } } = {
    'karachi': { lat: 24.8607, lng: 67.0011 },
    'lahore': { lat: 31.5497, lng: 74.3436 },
    'islamabad': { lat: 33.6844, lng: 73.0479 },
    'delhi': { lat: 28.6139, lng: 77.2090 },
    'mumbai': { lat: 19.0760, lng: 72.8777 },
    'dubai': { lat: 25.2048, lng: 55.2708 }
  };
  
  return cities[city.toLowerCase()] || { lat: 24.8607, lng: 67.0011 };
};






// Add these functions to your existing api.ts

// Generate random coordinates around a center point
export const generateRandomCoordinates = (
  centerLat: number, 
  centerLng: number, 
  radiusKm: number = 1
): [number, number] => {
  const radiusInDegrees = radiusKm / 111; // 1 degree ≈ 111km
  
  // Random angle
  const angle = Math.random() * 2 * Math.PI;
  
  // Random distance within radius
  const distance = Math.random() * radiusInDegrees;
  
  const lat = centerLat + (distance * Math.cos(angle));
  const lng = centerLng + (distance * Math.sin(angle));
  
  return [lat, lng];
};

// Calculate distance between two coordinates
export const calculateDistance = (
  lat1: number, 
  lng1: number, 
  lat2: number, 
  lng2: number
): number => {
  const R = 6371; // Earth's radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLng = (lng2 - lng1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLng/2) * Math.sin(dLng/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
};