import './PlaceCard.css';

interface PlaceCardProps {
  name: string;
  type: string;
  address: string;
  rating: number;
  distance: number;
  healthScore: number;
  onClick?: () => void;
}

export default function PlaceCard({
  name,
  type,
  address,
  rating,
  distance,
  healthScore,
  onClick
}: PlaceCardProps) {
  const getTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'restaurant': return '#10B981';
      case 'gym': return '#3B82F6';
      case 'cafe': return '#F59E0B';
      case 'park': return '#22C55E';
      default: return '#6B7280';
    }
  };

  const getTypeEmoji = (type: string) => {
    switch (type.toLowerCase()) {
      case 'restaurant': return '🍴';
      case 'gym': return '💪';
      case 'cafe': return '☕';
      case 'park': return '🌳';
      default: return '📍';
    }
  };

  return (
    <div className="place-card" onClick={onClick}>
      <div className="place-header">
        <div className="place-type" style={{ backgroundColor: getTypeColor(type) + '20', color: getTypeColor(type) }}>
          <span className="type-emoji">{getTypeEmoji(type)}</span>
          <span className="type-text">{type}</span>
        </div>
        <div className="health-score">
          <span className="score-value">{healthScore.toFixed(1)}</span>
          <span className="score-label">/10</span>
        </div>
      </div>
      
      <h3 className="place-name">{name}</h3>
      <p className="place-address">{address}</p>
      
      <div className="place-footer">
        <div className="rating">
          <div className="stars">
            {'★'.repeat(Math.floor(rating))}
            {rating % 1 >= 0.5 ? '½' : ''}
            {'☆'.repeat(5 - Math.ceil(rating))}
          </div>
          <span className="rating-value">{rating.toFixed(1)}</span>
        </div>
        <div className="distance">
          <span className="distance-value">{distance.toFixed(1)} km</span>
          <span className="distance-label">away</span>
        </div>
      </div>
      
      <button className="view-button">
        View on Map →
      </button>
    </div>
  );
}