import { useState } from 'react';
import './SearchBar.css';

interface SearchBarProps {
  onSearch: (query: string) => void;
  onUseLocation: () => void;
  loading: boolean;
}

export default function SearchBar({ onSearch, onUseLocation, loading }: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter location (e.g., New York, Delhi, Mumbai)"
            className="search-input"
            disabled={loading}
          />
          <button 
            type="submit" 
            className="search-button"
            disabled={loading || !query.trim()}
          >
            {loading ? (
              <span className="loading-text">Searching...</span>
            ) : (
              '🔍 Search'
            )}
          </button>
        </div>
        
        <div className="search-options">
          <button 
            type="button" 
            className="location-button"
            onClick={onUseLocation}
            disabled={loading}
          >
            📍 Use My Location
          </button>
          
          <div className="quick-searches">
            <span>Quick search:</span>
            {['New York', 'Delhi', 'London', 'Tokyo'].map((city) => (
              <button
                key={city}
                type="button"
                className="quick-search-button"
                onClick={() => {
                  setQuery(city);
                  onSearch(city);
                }}
                disabled={loading}
              >
                {city}
              </button>
            ))}
          </div>
        </div>
      </form>
    </div>
  );
}