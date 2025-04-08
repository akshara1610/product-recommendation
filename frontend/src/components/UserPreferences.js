import React, { useState, useEffect } from 'react';
import './UserPreferences.css';

const UserPreferences = ({ preferences, products, onPreferencesChange }) => {
  // fixed category values based on the readme
  const fixedCategories = [
    'Electronics',
    'Clothing',
    'Home goods',
    'Beauty & Personal Care',
    'Sports & Outdoors'
  ];
  
 
  const [formData, setFormData] = useState({
    priceRange: { min: '', max: '' },
    categories: [],
    brands: []
  });
  
  
  // all brands extracted
  const [availableBrands, setAvailableBrands] = useState([]);
  
  useEffect(() => {
    if (products && products.length > 0) {
      const uniqueBrands = [...new Set(products.map(p => p.brand).filter(Boolean))];
      setAvailableBrands(uniqueBrands);
    }
  }, [products]);
  
  // taking price as an input
  const handleMinPriceChange = (e) => {
    const inputValue = e.target.value;
    setFormData(prev => ({
      ...prev,
      priceRange: { 
        min: inputValue,
        max: prev.priceRange.max 
      }
    }));
  };
  
  const handleMaxPriceChange = (e) => {
    const inputValue = e.target.value;
    setFormData(prev => ({
      ...prev,
      priceRange: { 
        min: prev.priceRange.min,
        max: inputValue 
      }
    }));
  };
  
  const handleCategoryChange = (e) => {
    const category = e.target.value;
    const isChecked = e.target.checked;
    
    setFormData(prev => ({
      ...prev,
      categories: isChecked 
        ? [...prev.categories, category] 
        : prev.categories.filter(c => c !== category)
    }));
  };
  
  const handleBrandChange = (e) => {
    const brand = e.target.value;
    const isChecked = e.target.checked;
    
    setFormData(prev => ({
      ...prev,
      brands: isChecked 
        ? [...prev.brands, brand] 
        : prev.brands.filter(b => b !== brand)
    }));
  };

  
  // submit form: called when button Add Preferences is called
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("FormData at start",formData);
    
    // formatted data to match api request format
    const apiFormattedData = {
      priceRange: formData.priceRange.min && formData.priceRange.max 
        ? `${formData.priceRange.min}-${formData.priceRange.max}`
        : "all",
      categories: [...formData.categories],
      brands: [...formData.brands]
    };
    
    if (onPreferencesChange) {
      onPreferencesChange(apiFormattedData);
    }
    console.log("FormData at End",formData);
  };
  
  // reset preferences
  const handleReset = () => {
    
    const defaultFormData = {
      priceRange: { min: '', max: '' },
      categories: [],
      brands: []
    };
    
    setFormData(defaultFormData);
    
    if (onPreferencesChange) {
      onPreferencesChange({
        priceRange: "all",
        categories: [],
        brands: []
      });
    }
  };
  
  return (
    <div className="preferences-container">
      <h3>Your Preferences</h3>
      
      <form onSubmit={handleSubmit}>
        {/* Price Range Selection */}
        <div className="preference-section">
          <h4>Price Range</h4>
          <div className="price-inputs">
            <div className="price-field">
              <label htmlFor="min-price">Min ($)</label>
              <input
                type="number"
                id="min-price"
                name="minPrice"
                value={formData.priceRange.min}
                onChange={handleMinPriceChange}
                min="0"
                placeholder="Min"
              />
            </div>
            <div className="price-field">
              <label htmlFor="max-price">Max ($)</label>
              <input
                type="number"
                id="max-price"
                name="maxPrice"
                value={formData.priceRange.max}
                onChange={handleMaxPriceChange}
                placeholder="Max"
              />
            </div>
          </div>
          <div className="checkbox-item price-option">
            <input
              type="checkbox"
              id="price-all"
              checked={!formData.priceRange.min && !formData.priceRange.max}
              onChange={() => {
                //console.log("Onchange triggered",formData.priceRange);
                if (formData.priceRange.min || formData.priceRange.max) {
                  //console.log("inside if");
                  // If any price is set, clear both to indicate "all prices"
                  setFormData(prev => ({
                    ...prev,
                    priceRange: { min: '', max: '' }
                  }));
                }
              }}
            />
            <label htmlFor="price-all">All prices</label>
          </div>
        </div>
        
        {/* Category Selection */}
        <div className="preference-section">
          <h4>Categories</h4>
          <div className="checkbox-group">
            {fixedCategories.map((category) => (
              <div key={category} className="checkbox-item">
                <input
                  type="checkbox"
                  id={`category-${category}`}
                  name="categories"
                  value={category}
                  checked={formData.categories.includes(category)}
                  onChange={handleCategoryChange}
                />
                <label htmlFor={`category-${category}`}>{category}</label>
              </div>
            ))}
          </div>
        </div>
        
        {/* Brand Selection */}
        <div className="preference-section">
          <h4>Brands</h4>
          {availableBrands.length > 0 ? (
            <div className="checkbox-group">
              {availableBrands.map((brand) => (
                <div key={brand} className="checkbox-item">
                  <input
                    type="checkbox"
                    id={`brand-${brand}`}
                    name="brands"
                    value={brand}
                    checked={formData.brands.includes(brand)}
                    onChange={handleBrandChange}
                  />
                  <label htmlFor={`brand-${brand}`}>{brand}</label>
                </div>
              ))}
            </div>
          ) : (
            <p className="no-options">No brands available</p>
          )}
        </div>
        
        
        {/* Form Buttons */}
        <div className="preference-buttons">
          <button type="submit" className="apply-btn">Add Preferences</button>
          <button type="button" onClick={handleReset} className="reset-btn">Reset</button>
        </div>
      </form>
    </div>
  );
};

export default UserPreferences;