import React from 'react';
import './BrowsingHistory.css';

const BrowsingHistory = ({ history, products, onClearHistory }) => {
  // TODO: Implement a browsing history display
  // This component should:
  // - Show products the user has clicked on
  // - Allow clearing the browsing history
  if (!history || history.length === 0) {
  return (
    
    <div className="history-container">
      <h3>Your Browsing History</h3>
      {/* Implement browsing history display here */}
      <p>The user had not viewed any product yet.</p>
    </div>
  );
};

const generateSummary = () => {
  // Count categories
  const categories = {};
  history.forEach(item => {
    if (item.category) {
      categories[item.category] = (categories[item.category] || 0) + 1;
    }
  });
  
  // Count brands
  const brands = {};
  history.forEach(item => {
    if (item.brand) {
      brands[item.brand] = (brands[item.brand] || 0) + 1;
    }
  });
  
  // Calculate average price
  const prices = history.map(item => item.price).filter(price => price !== undefined);
  const avgPrice = prices.length > 0 
    ? prices.reduce((sum, price) => sum + price, 0) / prices.length
    : 0;
  
  // Get top categories and brands
  const topCategories = Object.entries(categories)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 2)
    .map(entry => entry[0]);
    
  const topBrands = Object.entries(brands)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 2)
    .map(entry => entry[0]);
  
  return {
    itemCount: history.length,
    topCategories,
    topBrands,
    avgPrice
  };
};

const summary = generateSummary();
// adds products viewed by the user and also allows the user to clear all the history
return (
  <div className="history-container">
    <div className="history-header">
      <h3>Your Browsing History</h3>
      <button 
        className="clear-history-btn" 
        onClick={onClearHistory}
      >
        Clear All
      </button>
    </div>
    
    {/* Compact Summary Section */}
    <div className="history-summary">
      <h4>Summary</h4>
      <div className="summary-stats">
        <div className="summary-stat">
          <span className="stat-value">{summary.itemCount}</span>
          <span className="stat-label">Items viewed</span>
        </div>
        
        {summary.avgPrice > 0 && (
          <div className="summary-stat">
            <span className="stat-value">${summary.avgPrice.toFixed(2)}</span>
            <span className="stat-label">Avg. price</span>
          </div>
        )}
      </div>
      
      {summary.topCategories.length > 0 && (
        <div className="summary-interests">
          <span className="interests-label">Top interests:</span>
          <span className="interests-value">
            {summary.topCategories.join(', ')}
          </span>
        </div>
      )}
      
      {summary.topBrands.length > 0 && (
        <div className="summary-brands">
          <span className="brands-label">Preferred brands:</span>
          <span className="brands-value">
            {summary.topBrands.join(', ')}
          </span>
        </div>
      )}
    </div>
    
    <div className="history-items">
      {history.map((item) => (
        <div key={item.id} className="history-item">
          <div className="item-image">
            {item.image ? (
              <img src={item.image} alt={item.name} />
            ) : (
              <div className="image-placeholder"></div>
            )}
          </div>
          <div className="item-details">
            <h4 className="item-name">{item.name}</h4>
            <p className="item-price">${item.price?.toFixed(2) || 'N/A'}</p>
            <p className="item-category">{item.category}</p>
          </div>
        </div>
      ))}
    </div>
  </div>
);
};


export default BrowsingHistory;