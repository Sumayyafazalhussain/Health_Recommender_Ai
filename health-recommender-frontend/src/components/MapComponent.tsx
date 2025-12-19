import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './MapComponent.css';

// Fix for default markers in React
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

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

interface MapComponentProps {
  center: [number, number];
  locations: MapLocation[];
  radius?: number;
  height?: string;
  zoom?: number;
}

const MapComponent: React.FC<MapComponentProps> = ({
  center,
  locations = [],
  radius = 1000,
  height = '500px',
  zoom = 15
}) => {
  
  const getMarkerIcon = (type: 'unhealthy' | 'healthy' | 'alternative') => {
    const iconSize: [number, number] = [32, 32];
    const iconAnchor: [number, number] = [16, 32];
    const popupAnchor: [number, number] = [0, -32];
    
    let iconUrl;
    let className = '';
    
    switch (type) {
      case 'unhealthy':
        iconUrl = 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png';
        className = 'unhealthy-marker';
        break;
      case 'healthy':
        iconUrl = 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png';
        className = 'healthy-marker';
        break;
      case 'alternative':
        iconUrl = 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png';
        className = 'alternative-marker';
        break;
    }
    
    return L.icon({
      iconUrl,
      iconSize,
      iconAnchor,
      popupAnchor,
      className
    });
  };

  const getPopupContent = (location: MapLocation) => {
    return `
      <div class="map-popup">
        <div class="popup-header">
          <span class="location-type ${location.type}">
            ${location.type === 'unhealthy' ? '🚫' : 
              location.type === 'healthy' ? '✅' : '📍'}
            ${location.type.toUpperCase()}
          </span>
          ${location.healthScore ? `<span class="health-score">${location.healthScore.toFixed(1)}/10</span>` : ''}
        </div>
        <h4>${location.name}</h4>
        <p class="address">📍 ${location.address}</p>
        ${location.rating ? `<p>⭐ ${location.rating}/5</p>` : ''}
        ${location.distance ? `<p>📏 ${location.distance.toFixed(1)} km</p>` : ''}
        ${location.description ? `<p class="description">${location.description}</p>` : ''}
      </div>
    `;
  };

  return (
    <div className="map-wrapper" style={{ height }}>
      <MapContainer 
        center={center} 
        zoom={zoom} 
        className="leaflet-map"
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Search radius circle */}
        <Circle
          center={center}
          radius={radius}
          pathOptions={{
            fillColor: '#10b981',
            fillOpacity: 0.1,
            color: '#10b981',
            weight: 2,
            opacity: 0.5
          }}
        />
        
        {/* Center marker */}
        <Marker position={center} icon={getMarkerIcon('healthy')}>
          <Popup>
            <div className="map-popup">
              <div className="popup-header">
                <span className="location-type center">📍</span>
                <span className="health-score">Search Center</span>
              </div>
              <h4>Your Search Location</h4>
              <p>📍 Lat: {center[0].toFixed(6)}, Lng: {center[1].toFixed(6)}</p>
              <p>📏 Search radius: {(radius/1000).toFixed(1)} km</p>
            </div>
          </Popup>
        </Marker>
        
        {/* Location markers */}
        {locations.map((location) => (
          <Marker
            key={location.id}
            position={location.coordinates}
            icon={getMarkerIcon(location.type)}
          >
            <Popup>
              <div 
                className="map-popup-content"
                dangerouslySetInnerHTML={{ __html: getPopupContent(location) }}
              />
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default MapComponent;