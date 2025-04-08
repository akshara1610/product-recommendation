import React, { useState, useEffect } from 'react';
import './Catalog.css';
// as there were no images as a part of the data I have implemented placeholder for images saying no image
const Catalog = ({ products, onProductClick, browsingHistory }) => {
  const [viewMode, setViewMode] = useState('grid');
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [filters, setFilters] = useState({
    search: '',
    category: 'all',
    rating: 0,
  });
  const [sortOption, setSortOption] = useState('default');
  // all categories are extracted
  const [categories, setCategories] = useState(['all']);
  
  useEffect(() => {
    if (products && products.length > 0) {
      // setting unique categories 
      const uniqueCategories = [...new Set(products.map(p => p.category).filter(Boolean))];
      setCategories(['all', ...uniqueCategories]);

      applyFiltersAndSort(products, filters, sortOption);
    }
  }, [products]);
  
  //filters and sorting
  useEffect(() => {
    applyFiltersAndSort(products, filters, sortOption);
  }, [filters, sortOption, products]);
  
  // check for product in browsing history (used later)
  const isInBrowsingHistory = (productId) => {
    if (!browsingHistory || !Array.isArray(browsingHistory)) {
      return false;
    }
    
    if (browsingHistory.length > 0 && typeof browsingHistory[0] === 'object') {
      return browsingHistory.some(item => item.id === productId);
    }
    
    return browsingHistory.includes(productId);
  };
  

  const applyFiltersAndSort = (products, filters, sortOption) => {
    let result = [...products];
    

    if (filters.search.trim()) {
      const searchTerm = filters.search.toLowerCase();
      result = result.filter(product => 
        product.name.toLowerCase().includes(searchTerm) ||
        (product.description && product.description.toLowerCase().includes(searchTerm)) ||
        (product.category && product.category.toLowerCase().includes(searchTerm)) ||
        (product.brand && product.brand.toLowerCase().includes(searchTerm))
      );
    }
    
    //filtered using category
    if (filters.category !== 'all') {
      result = result.filter(product => product.category === filters.category);
    }
    
    // filtered using rating
    if (filters.rating > 0) {
      result = result.filter(product => product.rating >= filters.rating);
    }
    
    // sorting feature
    switch(sortOption) {
      case 'price-asc':
        result.sort((a, b) => a.price - b.price);
        break;
      case 'price-desc':
        result.sort((a, b) => b.price - a.price);
        break;
      case 'name-asc':
        result.sort((a, b) => a.name.localeCompare(b.name));
        break;
      case 'name-desc':
        result.sort((a, b) => b.name.localeCompare(a.name));
        break;
      case 'rating-desc':
        result.sort((a, b) => (b.rating || 0) - (a.rating || 0));
        break;
      default:
        break;
    }
    
    setFilteredProducts(result);
  };
  

  const handleFilterChange = (name, value) => {
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
 
  const handlePriceChange = (type, value) => {
    setFilters(prev => ({
      ...prev,
      priceRange: {
        ...prev.priceRange,
        [type]: value
      }
    }));
  };
  
  // if a product is clicked tagged as recently viewed
  const handleProductClick = (product) => {
    if (onProductClick) {
      onProductClick(product);
    }
  };
  
  // reset
  const handleResetFilters = () => {
    setFilters({
      search: '',
      priceRange: { min: '', max: '' },
      category: 'all',
      rating: 0,
      inStock: false
    });
    setSortOption('default');
  };
  
  if (!products || products.length === 0) {
    return <div className="empty-catalog">No products available</div>;
  }
  
  return (
    <div className="catalog-container">
      {/* Filtering and Sorting Controls */}
      <div className="catalog-controls">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search products..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="filter-bar">
          <div className="filter-group">
            <label>Category:</label>
            <select 
              value={filters.category}
              onChange={(e) => handleFilterChange('category', e.target.value)}
              className="filter-select"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category === 'all' ? 'All Categories' : category}
                </option>
              ))}
            </select>
          </div>
          
          
          <div className="filter-group">
            <label>Rating:</label>
            <select 
              value={filters.rating}
              onChange={(e) => handleFilterChange('rating', parseFloat(e.target.value))}
              className="filter-select"
            >
              <option value={0}>Any Rating</option>
              <option value={3}>3+ Stars</option>
              <option value={4}>4+ Stars</option>
              <option value={4.5}>4.5+ Stars</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label>Sort By:</label>
            <select 
              value={sortOption}
              onChange={(e) => setSortOption(e.target.value)}
              className="filter-select"
            >
              <option value="default">Default</option>
              <option value="price-asc">Price: Low to High</option>
              <option value="price-desc">Price: High to Low</option>
              <option value="name-asc">Name: A to Z</option>
              <option value="name-desc">Name: Z to A</option>
              <option value="rating-desc">Highest Rated</option>
            </select>
          </div>
          
          
          <button className="reset-filters-btn" onClick={handleResetFilters}>
            Reset Filters
          </button>
        </div>
      </div>
      
      {/* Product Count */}
      <div className="catalog-info">
        <div className="catalog-count">{filteredProducts.length} products</div>
      </div>
      
      {/* Products Grid */}
      <div className="catalog-scrollable">
        {filteredProducts.length > 0 ? (
          <div className="product-grid">
            {filteredProducts.map((product) => (
              <div 
                key={product.id} 
                className={`product-card ${isInBrowsingHistory(product.id) ? 'viewed' : ''}`}
                onClick={() => handleProductClick(product)}
              >
                <div className="product-image-container">
                  {product.image ? (
                    <img 
                      src={product.image} 
                      alt={product.name} 
                      className="product-image" 
                    />
                  ) : (
                    <div className="product-image-placeholder">
                      No Image
                    </div>
                  )}
                  {isInBrowsingHistory(product.id) && (
                    <div className="recently-viewed-badge">
                      Recently Viewed
                    </div>
                  )}
                  {product.inventory === 0 && (
                    <div className="out-of-stock-badge">
                      Out of Stock
                    </div>
                  )}
                </div>

                <div className="product-info">
                  <h3 className="product-name">{product.name}</h3>
                  <p className="product-price">${product.price?.toFixed(2) || 'N/A'}</p>
                  
                  <div className="product-details">
                    {product.brand && (
                      <p className="product-brand">
                        <span className="detail-label">Brand:</span> {product.brand}
                      </p>
                    )}
                    
                    {product.category && (
                      <p className="product-category">
                        <span className="detail-label">Category:</span> {product.category}
                      </p>
                    )}
                    
                    {product.rating && (
                      <div className="product-rating">
                        <span className="detail-label">Rating:</span> {product.rating}/5
                      </div>
                    )}
                  </div>
                  
                  <button className="view-details-btn">
                    Check Product
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-results">
            <p>No products match your current filters.</p>
            <button className="reset-filters-btn" onClick={handleResetFilters}>
              Reset Filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Catalog;