import { useState, useEffect } from 'react';
import { apiService, getCoordinatesForCity, type RecommendationResponse, type AlternativePlace } from './utils/api';
import MapComponent from './components/MapComponent';
import './App.css';

// Add these interfaces at the top
interface MapLocation {
  id: string;
  name: string;
  type: 'unhealthy' | 'healthy' | 'alternative';
  coordinates: [number, number];
  address: string;
  rating?: number;
  distance?: number;
  healthScore?: number;
  description?: string;
}

interface Place {
  id: string;
  name: string;
  type: string;
  address: string;
  coordinates: { lat: number; lng: number };
  rating: number;
  distance: number;
  healthScore: number;
  description?: string;
  price_range: string;
  isRealData: boolean;
}

function App() {
  const [places, setPlaces] = useState<Place[]>([]);
  const [loading, setLoading] = useState(false);
  const [location, setLocation] = useState('Enter location');
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');
  const [error, setError] = useState('');
  const [aiMessage, setAiMessage] = useState('');
  const [detectedPlace, setDetectedPlace] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [usingRealData, setUsingRealData] = useState(false);
  const [mapCenter, setMapCenter] = useState<[number, number]>([24.8607, 67.0011]);
  const [mapLocations, setMapLocations] = useState<MapLocation[]>([]);
  const [showMap, setShowMap] = useState(false);

  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    setBackendStatus('checking');
    try {
      const health = await apiService.healthCheck();
      setBackendStatus(health.status === 'healthy' ? 'connected' : 'disconnected');
    } catch {
      setBackendStatus('disconnected');
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    setError('');
    setLocation(searchQuery);
    setPlaces([]);
    setAiMessage('');
    setDetectedPlace(null);
    setMapLocations([]);
    setShowMap(false);

    try {
      let lat: number, lng: number;
      
      if (searchQuery.includes(',')) {
        const parts = searchQuery.split(',');
        lat = parseFloat(parts[0].trim());
        lng = parseFloat(parts[1].trim());
        if (isNaN(lat) || isNaN(lng)) {
          throw new Error('Invalid coordinates');
        }
      } else {
        const coords = getCoordinatesForCity(searchQuery);
        lat = coords.lat;
        lng = coords.lng;
      }

      // Set map center
      setMapCenter([lat, lng]);
      
      console.log('🔍 Searching at:', { lat, lng });
      
      const response = await apiService.getRecommendations(lat, lng, 1000);
      console.log('📦 Response:', response);
      
      // Check if we got real data
      const isRealData = response.status !== 'demo_mode';
      setUsingRealData(isRealData);
      
      if (isRealData) {
        setBackendStatus('connected');
        setError('');
      } else {
        setBackendStatus('disconnected');
        setError('Using demo data');
      }
      
      // Set AI message
      if (response.ai_message) {
        setAiMessage(response.ai_message);
      }
      
      // Set detected place
      if (response.detected_place) {
        setDetectedPlace(response.detected_place);
        
        // Add detected place to map
        const detectedMapLocation: MapLocation = {
          id: 'detected',
          name: response.detected_place.name,
          type: response.detected_place.is_unhealthy ? 'unhealthy' : 'healthy',
          coordinates: [lat, lng],
          address: response.detected_place.vicinity,
          rating: typeof response.detected_place.rating === 'string' ? 
            parseFloat(response.detected_place.rating) || 0 : 
            response.detected_place.rating || 0,
          healthScore: response.detected_place.is_unhealthy ? 3 : 8,
          description: response.detected_place.category
        };
        
        setMapLocations(prev => [...prev, detectedMapLocation]);
      }
      
      // Process places
      const processedPlaces: Place[] = [];
      const mapLocationsList: MapLocation[] = [];
      
      // Add healthy alternatives first (real data)
      if (response.healthy_alternatives && response.healthy_alternatives.length > 0) {
        response.healthy_alternatives.forEach((alt, index) => {
          const rating = typeof alt.rating === 'string' ? parseFloat(alt.rating) || 4.0 : alt.rating || 4.0;
          const distance = alt.distance ? alt.distance / 1000 : 0.5;
          const healthScore = getHealthScore(alt.category, rating);
          
          // Generate coordinates around center
          const coordLat = lat + (Math.random() * 0.01 - 0.005);
          const coordLng = lng + (Math.random() * 0.01 - 0.005);
          
          processedPlaces.push({
            id: `real_${index}`,
            name: alt.name,
            type: alt.category || 'Healthy Place',
            address: alt.vicinity,
            coordinates: { lat: coordLat, lng: coordLng },
            rating: rating,
            distance: distance,
            healthScore: healthScore,
            description: `${alt.category || 'Place'} • ${alt.price_level || 'Moderate'}`,
            price_range: alt.price_level || '$$',
            isRealData: true
          });
          
          // Add to map locations
          mapLocationsList.push({
            id: `map_alt_${index}`,
            name: alt.name,
            type: 'alternative',
            coordinates: [coordLat, coordLng],
            address: alt.vicinity,
            rating: rating,
            distance: distance,
            healthScore: healthScore,
            description: alt.category
          });
        });
      }
      
      // Add recommendations as fallback
      if (processedPlaces.length === 0 && response.recommendations) {
        response.recommendations.forEach((rec, index) => {
          const coordLat = lat + (Math.random() * 0.02 - 0.01);
          const coordLng = lng + (Math.random() * 0.02 - 0.01);
          const rating = 4.0 + Math.random();
          const distance = 0.5 + Math.random() * 3;
          const healthScore = 7.5 + Math.random() * 2.5;
          const type = getTypeFromName(rec);
          
          processedPlaces.push({
            id: `rec_${index}`,
            name: rec,
            type: type,
            address: `Recommended near ${searchQuery}`,
            coordinates: { lat: coordLat, lng: coordLng },
            rating: rating,
            distance: distance,
            healthScore: healthScore,
            description: 'Healthy alternative suggestion',
            price_range: '$$',
            isRealData: isRealData
          });
          
          // Add to map locations
          mapLocationsList.push({
            id: `map_rec_${index}`,
            name: rec,
            type: 'alternative',
            coordinates: [coordLat, coordLng],
            address: `Near ${searchQuery}`,
            rating: rating,
            distance: distance,
            healthScore: healthScore,
            description: type
          });
        });
      }
      
      setPlaces(processedPlaces);
      setMapLocations(prev => [...prev, ...mapLocationsList]);
      setShowMap(true);
      
    } catch (err: any) {
      console.error('Search error:', err);
      setError(err.message || 'Search failed');
      setBackendStatus('disconnected');
      setUsingRealData(false);
      
      // Show demo data
      const demoPlaces = getDemoPlaces();
      setPlaces(demoPlaces);
      setAiMessage("Error connecting to backend. Showing demo data.");
      
      // Add demo locations to map
      const demoMapLocations: MapLocation[] = demoPlaces.map((place, index) => ({
        id: `demo_${index}`,
        name: place.name,
        type: 'alternative',
        coordinates: [place.coordinates.lat, place.coordinates.lng],
        address: place.address,
        rating: place.rating,
        distance: place.distance,
        healthScore: place.healthScore,
        description: place.type
      }));
      setMapLocations(demoMapLocations);
      setShowMap(true);
    } finally {
      setLoading(false);
    }
  };

  const getHealthScore = (category: string = '', rating: number = 4): number => {
    let baseScore = 7;
    
    if (category.includes('Cafe') || category.includes('cafe')) baseScore = 8;
    if (category.includes('Juice') || category.includes('Smoothie')) baseScore = 9;
    if (category.includes('Gym') || category.includes('Fitness')) baseScore = 9;
    if (category.includes('Park')) baseScore = 9.5;
    if (category.includes('Fast') || category.includes('Burger')) baseScore = 3;
    
    return Math.min(10, baseScore + (rating - 4) / 2);
  };

  const getTypeFromName = (name: string): string => {
    if (name.includes('Cafe')) return 'Cafe';
    if (name.includes('Juice')) return 'Juice Bar';
    if (name.includes('Gym')) return 'Gym';
    if (name.includes('Park')) return 'Park';
    if (name.includes('Restaurant') || name.includes('Food')) return 'Restaurant';
    return 'Healthy Place';
  };

  const getDemoPlaces = (): Place[] => {
    return [
      {
        id: '1',
        name: 'Green Leaf Cafe',
        type: 'Cafe',
        address: '123 Healthy Street',
        coordinates: { lat: 24.8617, lng: 67.0021 },
        rating: 4.5,
        distance: 1.2,
        healthScore: 8.5,
        description: 'Organic vegan cafe',
        price_range: '$$',
        isRealData: false
      },
      {
        id: '2',
        name: 'Fresh Juice Bar',
        type: 'Juice Bar',
        address: '456 Wellness Ave',
        coordinates: { lat: 24.8597, lng: 67.0001 },
        rating: 4.8,
        distance: 0.8,
        healthScore: 9.2,
        description: 'Fresh juices & smoothies',
        price_range: '$',
        isRealData: false
      },
      {
        id: '3',
        name: 'FitLife Gym',
        type: 'Gym',
        address: '789 Fitness Road',
        coordinates: { lat: 24.8607, lng: 67.0031 },
        rating: 4.7,
        distance: 2.1,
        healthScore: 9.0,
        description: '24/7 fitness center',
        price_range: '$$$',
        isRealData: false
      }
    ];
  };

  const handleUseLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords;
          setSearchQuery(`${latitude.toFixed(6)}, ${longitude.toFixed(6)}`);
          setLocation('Your Location');
          handleSearch();
        },
        () => setError('Location access denied')
      );
    } else {
      setError('Geolocation not supported');
    }
  };

  const stats = {
    total: places.length,
    realCount: places.filter(p => p.isRealData).length,
    avgHealth: places.length > 0 ? (places.reduce((a, b) => a + b.healthScore, 0) / places.length).toFixed(1) : '0.0',
    avgRating: places.length > 0 ? (places.reduce((a, b) => a + b.rating, 0) / places.length).toFixed(1) : '0.0'
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <span className="logo-icon">🌿</span>
          <div>
            <h1>Healthy Recommender AI</h1>
            <p className="tagline">Real-time health recommendations with interactive map</p>
          </div>
        </div>
        <div className="backend-status">
          <span className={`status-badge ${backendStatus}`}>
            {backendStatus === 'connected' ? '✅ Connected' : 
             backendStatus === 'disconnected' ? '❌ Disconnected' : '🔄 Checking'}
          </span>
          {usingRealData && <span className="real-badge">REAL DATA</span>}
          <button onClick={checkConnection} className="refresh-btn" disabled={loading}>
            🔄
          </button>
        </div>
      </header>

      <section className="hero">
        <div className="hero-content">
          <h2>Find Healthy Alternatives</h2>
          <p>AI-powered recommendations with interactive map visualization</p>
          <div className="api-info">
            <code>Backend: http://localhost:8000</code>
            <span className="map-icon" title="Interactive Map Available">🗺️</span>
          </div>
        </div>
      </section>

      <section className="search-section">
        <div className="search-container">
          <div className="search-box">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Enter city or coordinates (e.g., Karachi or 24.8607,67.0011)"
              className="search-input"
              disabled={loading}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button onClick={handleSearch} className="search-button" disabled={loading}>
              {loading ? '🔍 Searching...' : '🔍 Search'}
            </button>
            <button onClick={handleUseLocation} className="location-button" disabled={loading}>
              📍 My Location
            </button>
          </div>
          
          {error && <div className="error-message">⚠️ {error}</div>}
          
          <div className="quick-filters">
            <span>Test locations:</span>
            {['24.8607,67.0011', 'Karachi', 'Lahore', 'Delhi'].map((loc) => (
              <button
                key={loc}
                className="filter-btn"
                onClick={() => {
                  setSearchQuery(loc);
                  handleSearch();
                }}
                disabled={loading}
              >
                {loc}
              </button>
            ))}
          </div>
        </div>
      </section>

      <main className="main-content">
        {/* AI Analysis */}
        {(aiMessage || detectedPlace) && (
          <div className="ai-message-card">
            <div className="ai-message-header">
              <span className="ai-icon">🤖</span>
              <h3>AI Analysis</h3>
            </div>
            {aiMessage && <p className="ai-message-text">{aiMessage}</p>}
            {detectedPlace && (
              <div className="detected-place">
                <div className="detected-header">
                  <span className="detected-label">Detected:</span>
                  <span className="detected-name">{detectedPlace.name}</span>
                  <span className={`health-tag ${detectedPlace.is_unhealthy ? 'unhealthy' : 'healthy'}`}>
                    {detectedPlace.is_unhealthy ? '🚫 Unhealthy' : '✅ Healthy'}
                  </span>
                </div>
                <div className="detected-details">
                  <span><strong>Type:</strong> {detectedPlace.category}</span>
                  <span><strong>Rating:</strong> {detectedPlace.rating}</span>
                  <span><strong>Price:</strong> {detectedPlace.price_level}</span>
                </div>
                <div className="detected-address">
                  <strong>📍</strong> {detectedPlace.vicinity}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Statistics */}
        {places.length > 0 && (
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">{stats.total}</div>
              <div className="stat-label">Places</div>
              {stats.realCount > 0 && <div className="stat-sub">({stats.realCount} real)</div>}
            </div>
            <div className="stat-card">
              <div className="stat-number">{stats.avgHealth}</div>
              <div className="stat-label">Health Score</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{stats.avgRating}</div>
              <div className="stat-label">Avg Rating</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{showMap ? '🗺️' : '📱'}</div>
              <div className="stat-label">{showMap ? 'Map Ready' : 'No Map'}</div>
            </div>
          </div>
        )}

        {/* Interactive Map Section */}
        {showMap && (
          <div className="map-section">
            <div className="section-header">
              <h3>
                <span className="map-icon-large">🗺️</span>
                Interactive Map View
              </h3>
              <div className="map-legend">
                <div className="legend-item">
                  <span className="legend-color unhealthy"></span>
                  <span>Unhealthy Places</span>
                </div>
                <div className="legend-item">
                  <span className="legend-color healthy"></span>
                  <span>Healthy Places</span>
                </div>
                <div className="legend-item">
                  <span className="legend-color alternative"></span>
                  <span>Alternatives</span>
                </div>
              </div>
            </div>
            <MapComponent
              center={mapCenter}
              locations={mapLocations}
              radius={1000}
              height="500px"
              zoom={15}
            />
          </div>
        )}

        {/* Places Grid */}
        {places.length > 0 ? (
          <>
            <div className="recommendations-header">
              <h3>Healthy Alternatives {location && `in ${location}`}</h3>
              <div className="results-info">
                <span className="results-count">{places.length} results</span>
                {usingRealData && <span className="real-badge-small">✅ Real Data</span>}
              </div>
            </div>

            <div className="recommendations-grid">
              {places.map((place) => (
                <div key={place.id} className={`place-card ${place.isRealData ? 'real' : 'demo'}`}>
                  <div className="place-header">
                    <span className={`place-type ${place.type.toLowerCase().replace(' ', '-')}`}>
                      {place.type === 'Cafe' ? '☕' :
                       place.type === 'Juice Bar' ? '🥤' :
                       place.type === 'Gym' ? '💪' :
                       place.type === 'Park' ? '🌳' : '🍴'}
                      {place.type}
                    </span>
                    <span className="health-score">
                      {place.healthScore.toFixed(1)}/10
                    </span>
                  </div>
                  
                  <h3 className="place-name">{place.name}</h3>
                  <p className="place-address">{place.address}</p>
                  
                  {place.description && (
                    <p className="place-description">{place.description}</p>
                  )}
                  
                  <div className="place-details">
                    <div className="rating">
                      <div className="stars">
                        {'★'.repeat(Math.floor(place.rating))}
                        {place.rating % 1 >= 0.5 ? '½' : ''}
                        {'☆'.repeat(5 - Math.ceil(place.rating))}
                      </div>
                      <span className="rating-value">{place.rating.toFixed(1)}</span>
                    </div>
                    <div className="distance">
                      {place.distance.toFixed(1)} km away
                    </div>
                  </div>
                  
                  <div className="place-footer">
                    <span className="price-range">{place.price_range}</span>
                    <span className={`data-source ${place.isRealData ? 'real' : 'demo'}`}>
                      {place.isRealData ? '✅ Real' : '📱 Demo'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : !loading && (
          <div className="no-results">
            <div className="no-results-icon">📍</div>
            <h4>Search for a location</h4>
            <p>Enter a city name or coordinates to find healthy alternatives</p>
            <button 
              className="test-btn"
              onClick={() => {
                setSearchQuery('24.8607,67.0011');
                handleSearch();
              }}
            >
              Test with KFC Coordinates
            </button>
          </div>
        )}

        {/* Backend Info */}
        <div className="api-section">
          <h3>Connection Status</h3>
          <div className="api-info-card">
            <div className="status-details">
              <div className="status-row">
                <span className="label">Backend:</span>
                <code className="value">http://localhost:8000</code>
              </div>
              <div className="status-row">
                <span className="label">Status:</span>
                <span className={`value status ${backendStatus}`}>
                  {backendStatus === 'connected' ? '✅ Connected' : '❌ Disconnected'}
                </span>
              </div>
              <div className="status-row">
                <span className="label">Data Source:</span>
                <span className={`value source ${usingRealData ? 'real' : 'demo'}`}>
                  {usingRealData ? '✅ Real Google Maps Data' : '📱 Demo Data'}
                </span>
              </div>
              <div className="status-row">
                <span className="label">Map Features:</span>
                <span className="value">✅ Interactive Map</span>
              </div>
            </div>
            
            <div className="action-buttons">
              <button 
                className="action-btn"
                onClick={() => window.open('http://localhost:8000/docs', '_blank')}
              >
                📚 API Docs
              </button>
              <button 
                className="action-btn"
                onClick={checkConnection}
              >
                🔄 Refresh
              </button>
              <button 
                className="action-btn"
                onClick={() => window.open('http://localhost:8000', '_blank')}
              >
                🌐 Backend
              </button>
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <div className="footer-content">
          <p>Healthy Recommender AI - Interactive Map & Real-time Recommendations</p>
          <div className="footer-info">
            <span>Backend: http://localhost:8000</span>
            <span>•</span>
            <span>Status: {backendStatus}</span>
            <span>•</span>
            <span>Map: {showMap ? 'Active' : 'Inactive'}</span>
          </div>
          <div className="footer-actions">
            <button 
              className="footer-btn"
              onClick={() => {
                setSearchQuery('24.8607,67.0011');
                handleSearch();
              }}
            >
              Test with KFC Coordinates
            </button>
            <button className="footer-btn" onClick={() => window.location.reload()}>
              Refresh
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;