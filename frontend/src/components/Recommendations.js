import React from 'react';
import './Recommendations.css';

const Recommendations = ({ recommendations, isLoading }) => {
  // TODO: Implement a display for recommended products
  // This component should:
  // - Display recommended products with explanations
  // - Show a loading state when recommendations are being generated
  // - Handle cases where no recommendations are available
  console.log(recommendations);
  return (
    <div className="recommendations-container">
     {isLoading ? (
        <div className="loading-recommendations">
          <div className="loading-spinner"></div>
          <p>Generating personalized recommendations...</p>
        </div>
      ) : recommendations.length > 0 ? (
        <div className="recommendations-content">
          <p className="recommendations-subtitle">Based on your preferences and browsing history</p>
          
          <div className="product-grid">
            {recommendations.map((recommendation) => (
              <div 
                key={recommendation.product.id} 
                className="product-card"
              >
                <div className="product-image-container">
                  {recommendation.product.image ? (
                    <img 
                      src={recommendation.product.image} 
                      alt={recommendation.product.name} 
                      className="product-image" 
                    />
                  ) : (
                    <div className="product-image-placeholder">
                      No Image
                    </div>
                  )}
                  <div className="confidence-badge">
                    Match: {recommendation.confidence_score}/10
                  </div>
                </div>

                <div className="product-info">
                  <h3 className="product-name">{recommendation.product.name}</h3>
                  <p className="product-price">${recommendation.product.price?.toFixed(2) || 'N/A'}</p>
                  
                  <div className="product-details">
                    {recommendation.product.brand && (
                      <p className="product-brand">
                        <span className="detail-label">Brand:</span> {recommendation.product.brand}
                      </p>
                    )}
                    
                    {recommendation.product.category && (
                      <p className="product-category">
                        <span className="detail-label">Category:</span> {recommendation.product.category}
                      </p>
                    )}
                    
                    {recommendation.product.rating && (
                      <div className="product-rating">
                        <span className="detail-label">Rating:</span> {recommendation.product.rating}/5
                      </div>
                    )}
                  </div>
                  
                  <div className="recommendation-explanation">
                    <h4>Why we recommend this:</h4>
                    <p>{recommendation.explanation}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="no-recommendations">
          <h3>No recommendations yet</h3>
          <p>Set your preferences and browse some products to get personalized recommendations!</p>
        </div>
      )}
    </div>
  );
};

export default Recommendations;
