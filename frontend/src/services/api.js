const API_BASE_URL = 'http://localhost:8080/api';

// Fetch all products from the API
export const fetchProducts = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/products`);
    console.log(response);
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

// Get recommendations based on user preferences and browsing history
export const getRecommendations = async (preferences, browsingHistory) => {
  console.log(browsingHistory);
  const historyIds = browsingHistory.map(item => 
    typeof item === 'object' ? item.id : item
  );
  try {
    const response = await fetch(`${API_BASE_URL}/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        preferences: preferences,
        browsing_history: historyIds
      }),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting recommendations:', error);
    throw error;
  }
};