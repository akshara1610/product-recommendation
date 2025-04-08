import openai
from .cache_service import LLMCacheService
from config import config

class LLMService:
    """
    Service to handle interactions with the LLM API
    """
    
    def __init__(self):
        """
        Initialize the LLM service with configuration
        """
        openai.api_key = config['OPENAI_API_KEY']
        self.model_name = config['MODEL_NAME']
        self.max_tokens = config['MAX_TOKENS']
        self.temperature = config['TEMPERATURE']
        self.cache_service = LLMCacheService(
            cache_dir=config.get('CACHE_DIR', 'cache'),
            ttl_hours=config.get('CACHE_TTL_HOURS', 24)
        )

        self.use_cache = config.get('USE_CACHE', True)

        if self.use_cache:
            self.cache_service.clear_expired_cache()

        
    
    def generate_recommendations(self, user_preferences, browsing_history, all_products):
        """
        Generate personalized product recommendations based on user preferences and browsing history
        
        Parameters:
        - user_preferences (dict): User's stated preferences
        - browsing_history (list): List of product IDs the user has viewed
        - all_products (list): Full product catalog
        
        Returns:
        - dict: Recommended products with explanations
        """
        # TODO: Implement LLM-based recommendation logic
        # This is where your prompt engineering expertise will be evaluated
        if self.use_cache:
            cached_recommendations = self.cache_service.get_cached_recommendations(
                user_preferences, browsing_history
            )
            
            if cached_recommendations:
                # Add cache metadata to help with debugging
                cached_recommendations['cached'] = True
                return cached_recommendations
        # Get browsed products details
        browsed_products = []
        #print(browsing_history)
        for product_id in browsing_history:
            for product in all_products:
                if product["id"] == product_id:
                    browsed_products.append(product)
                    break
        
        # Create a prompt for the LLM
        # IMPLEMENT YOUR PROMPT ENGINEERING HERE
        #print(user_preferences,browsing_history)
        prompt = self._create_recommendation_prompt(user_preferences, browsed_products, all_products)
        
        # Call the LLM API
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful eCommerce product recommendation assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            #print(response)
            
            # Parse the LLM response to extract recommendations
            # IMPLEMENT YOUR RESPONSE PARSING LOGIC HERE
            recommendations = self._parse_recommendation_response(response.choices[0].message.content, all_products)
            #print("Items Recommended",recommendations[0])
            if self.use_cache and recommendations.get("recommendations"):
                self.cache_service.cache_recommendations(
                    user_preferences, browsing_history, recommendations
                )
            
            return recommendations
            
        except Exception as e:
            # Handle any errors from the LLM API
            print(f"Error calling LLM API: {str(e)}")
            raise Exception(f"Failed to generate recommendations: {str(e)}")
    
    def _create_recommendation_prompt(self, user_preferences, browsed_products, all_products):
        """
        Create a prompt for the LLM to generate recommendations
        
        This is where you should implement your prompt engineering strategy.
        
        Parameters:
        - user_preferences (dict): User's stated preferences
        - browsed_products (list): Products the user has viewed
        - all_products (list): Full product catalog
        
        Returns:
        - str: Prompt for the LLM
        """
        # TODO: Implement your prompt engineering strategy
        # THIS FUNCTION MUST BE IMPLEMENTED BY THE CANDIDATE
        prompt = "You are an expert e-commerce recommendation system. Your task is to recommend exactly 3 products that will genuinely interest this specific user.\n\n"
        
        # added user preferneces from the data received
        prompt += "===== USER PREFERENCES =====\n"
        
        # user preference of price range
        if user_preferences['priceRange'] == 'all':
            prompt += "Price Range: Any price\n"
        else:
            try:
                min_price, max_price = user_preferences['priceRange'].split('-')
                prompt += f"Price Range: ${min_price} to ${max_price}\n"
            except:
                prompt += f"Price Range: {user_preferences['priceRange']}\n"
        
        # mention categories in the prompt that the user chose
        categories = user_preferences['categories']
        prompt += f"The user wants products specific to these categories: {', '.join(categories) if categories else 'No specific preference'}\n"
        # mention brands that the user chose
        brands = user_preferences['brands']
        prompt += f"The user wants to products specific to these brands: {', '.join(brands) if brands else 'No specific preference'}\n"
        
        # add the browsing history of the user to the prompt
        prompt += "\n===== BROWSING HISTORY =====\n"
        if browsed_products:
            for product in browsed_products:
                prompt += f"• {product['name']}\n"
                prompt += f"  - ID: {product['id']}\n"
                prompt += f"  - Category: {product['category']}\n"
                prompt += f"  - Price: ${product['price']}\n"
                if 'brand' in product:
                    prompt += f"  - Brand: {product['brand']}\n"
                if 'rating' in product:
                    prompt += f"  - Rating: {product['rating']}/5\n"
                
                # include tags and features that have the most relevance, top 3
                if 'features' in product and product['features']:
                    prompt += f"  - Features: {', '.join(product['features'][:3])}\n"
                if 'tags' in product and product['tags']:
                    prompt += f"  - Tags: {', '.join(product['tags'][:3])}\n"
        else:
            # if there is no browsing history
            prompt += "User has not viewed any products yet.\n"
        
        # Select a smaller subset of relevant products to stay within token limits
        relevant_products = self._select_relevant_products(user_preferences, browsed_products, all_products)
        relevant_products = relevant_products[:15]  # Limit to 15 candidates to save tokens
        
        prompt += f"\n===== CANDIDATE PRODUCTS ({len(relevant_products)} selected) =====\n"
        for product in relevant_products:
            prompt += f"• {product['name']}\n"
            prompt += f"  - ID: {product['id']}\n"
            prompt += f"  - Category: {product['category']}\n"
            prompt += f"  - Price: ${product['price']}\n"
            if 'brand' in product:
                prompt += f"  - Brand: {product['brand']}\n"
            if 'rating' in product:
                prompt += f"  - Rating: {product['rating']}/5\n"
            if 'features' in product and product['features']:
                prompt += f"  - Features: {', '.join(product['features'][:2])}\n"
        
        prompt += "==== RECOMMENDATION REQUIREMENTS ====\n"
        prompt += "Select EXACTLY 5 products that would create the most compelling and personalized recommendations for this specific user.\n\n"
        
        # recommendation strategy
        prompt += "Your recommendation strategy should include:\n\n"
        
        prompt += "1. RELEVANCE & INTENT MATCHING:\n"
        prompt += "   - Products that directly satisfy the intent signaled by their browsing behavior\n"
        prompt += "   - Items that strongly align with their explicitly stated preferences\n\n"
        
        prompt += "2. PSYCHOGRAPHIC MATCHING:\n"
        prompt += "   - Consider the customer persona suggested by their browsing patterns\n"
        prompt += "   - Match to products that appeal to similar customer segments\n\n"
        
        prompt += "3. STRATEGIC RECOMMENDATION MIX:\n"
        prompt += "   - Core Recommendations: 2-3 products very closely matching their demonstrated interests\n"
        prompt += "   - Complementary Products: 1-2 items that enhance products they've browsed\n"
        prompt += "   - Discovery Product: 1 unexpected but relevant item to expand their horizons\n\n"
        
        prompt += "4. DETAILED PERSONALIZED REASONING:\n"
        prompt += "   - For each product, explain specifically WHY it matches this particular user\n"
        prompt += "   - Reference concrete aspects of their behavior or preferences\n"
        prompt += "   - Highlight key product features that address their specific needs or interests\n"
        prompt += "   - Use insights from similar customer purchase patterns where relevant\n\n"
        
        # specific examples of excellent vs. poor explanations
        prompt += "QUALITY BENCHMARK EXAMPLES:\n"
        prompt += "✓ EXCELLENT: \"This wireless charger complements the premium smartphone you viewed earlier, addressing your interest in fast-charging technology (which appeared in 3 of your browsed items). Its compact design also aligns with the portable accessories you've been exploring.\"\n\n"
        
        prompt += "✗ POOR: \"This is a highly-rated product that many customers enjoy and would be a good match for your preferences.\"\n\n"
        
        # response format
        prompt += "FORMAT YOUR RESPONSE AS A JSON ARRAY EXACTLY LIKE THIS:\n"
        # many shot prompting
        prompt += """[
      {
        "product_id": "prod123",
        "explanation": "Clear reasoning for this recommendation that connects to the user's specific interests",
        "score": 8
      },
      {
        "product_id": "prod456",
        "explanation": "Explanation for second product",
        "score": 7
      },
      {
        "product_id": "prod789",
        "explanation": "Explanation for third product",
        "score": 6
      }
    ]"""
        
        return prompt
    
    def _select_relevant_products(self, user_preferences, browsed_products, all_products, max_products=15):
        """
        Enhanced selection of relevant products from the catalog for recommendations.
        Uses a more sophisticated scoring algorithm to find the most relevant matches.
        
        Parameters:
        - user_preferences (dict): User's stated preferences
        - browsed_products (list): Products the user has viewed
        - all_products (list): Full product catalog
        - max_products (int): Maximum number of products to include
        
        Returns:
        - list: Filtered and sorted list of products most relevant to the user
        """
        # browsing history
        browsed_ids = set()
        browsed_categories = set()
        browsed_brands = set()
        browsed_tags = set()
        browsed_price_points = []
        
        for product in browsed_products:
            browsed_ids.add(product['id'])
            if 'category' in product:
                browsed_categories.add(product['category'])
            if 'brand' in product:
                browsed_brands.add(product['brand'])
            if 'tags' in product and product['tags']:
                browsed_tags.update(product['tags'])
            if 'price' in product:
                browsed_price_points.append(product['price'])
        
        # user's preferred categories and brands
        preferred_categories = set(user_preferences['categories']) if user_preferences['categories'] else set()
        preferred_brands = set(user_preferences['brands']) if user_preferences['brands'] else set()
        
        #all_categories = browsed_categories.union(preferred_categories)
        #all_brands = browsed_brands.union(preferred_brands)
        
        # price range metrics 
        avg_browsed_price = None
        if browsed_price_points:
            avg_browsed_price = sum(browsed_price_points) / len(browsed_price_points)
        
        # scores for each product
        product_scores = []
        
        for product in all_products:
            if product['id'] in browsed_ids:
                continue
                
            score = 0
            
            #feature matching
            if 'category' in product:
                # Strong match for explicitly preferred categories
                if product['category'] in preferred_categories:
                    score += 4
                # Good match for categories in browsing history
                elif product['category'] in browsed_categories:
                    score += 3
                   
            if 'brand' in product:
                # Strong match for explicitly preferred brands
                if product['brand'] in preferred_brands:
                    score += 4
                # Good match for brands in browsing history
                elif product['brand'] in browsed_brands:
                    score += 2.5
            
            if user_preferences['priceRange'] != 'all' and 'price' in product:
                try:
                    min_price, max_price = map(float, user_preferences['priceRange'].split('-'))
                    # Full points if within range
                    if min_price <= product['price'] <= max_price:
                        score += 3
                    # Partial points if close to range (within 20 percent)
                    elif (product['price'] < min_price and product['price'] >= min_price * 0.8) or \
                         (product['price'] > max_price and product['price'] <= max_price * 1.2):
                        score += 1
                except:
                    pass
            # browsing history without price preferneces
            elif avg_browsed_price is not None and 'price' in product:
                # Price similarity to browsed products
                price_diff_ratio = abs(product['price'] - avg_browsed_price) / avg_browsed_price if avg_browsed_price > 0 else 1
                if price_diff_ratio <= 0.2:  # within 20 percent  of average browsed price
                    score += 2
                elif price_diff_ratio <= 0.4:  # within 40 percent of average browsed price
                    score += 1
            

            if 'rating' in product:
                if product['rating'] >= 4.7:
                    score += 2
                elif product['rating'] >= 4.5:
                    score += 1.5
                elif product['rating'] >= 4.0:
                    score += 1
            

            if 'tags' in product and product['tags'] and browsed_tags:
                common_tags = set(product['tags']).intersection(browsed_tags)
                # More points for more tag matches
                score += len(common_tags) * 0.75

            if browsed_products and 'features' in product and product['features']:
                # Extract features from browsed products
                browsed_features = set()
                for bp in browsed_products:
                    if 'features' in bp and bp['features']:
                        browsed_features.update(bp['features'])
                
                #text matching implemented
                feature_matches = 0
                for feature in product['features']:
                    feature_lower = feature.lower()
                    for browsed_feature in browsed_features:
                        if any(word in feature_lower for word in browsed_feature.lower().split()):
                            feature_matches += 1
                            break
                
                score += feature_matches * 0.5
            

            if preferred_categories and 'category' in product:
                if product['category'] not in browsed_categories and product['category'] in preferred_categories:
                    score += 1  
            
            
            product_scores.append((product, score))
        
        # sorting products via relevance scores higher to lower
        product_scores.sort(key=lambda x: x[1], reverse=True)
        
        # exploring other products if there are no enough products for recommendation
        selected_products = []
        selected_categories = set()
        
       # adding most relevant product
        if product_scores:
            selected_products.append(product_scores[0][0])
            if 'category' in product_scores[0][0]:
                selected_categories.add(product_scores[0][0]['category'])
        
        # adding more products, ensuring category diversity
        remaining_scores = product_scores[1:]
        
        # adding some products from different categories 
        for product, score in remaining_scores:
            if len(selected_products) >= max_products:
                break
                
            category = product.get('category', '')
            
            if len(selected_categories) >= 3 or not category or category in selected_categories:
                continue
            
            selected_products.append(product)
            if category:
                selected_categories.add(category)
        

        for product, score in remaining_scores:
            if len(selected_products) >= max_products:
                break
                
            if product not in selected_products:
                selected_products.append(product)
        
        return selected_products[:max_products]
    def _parse_recommendation_response(self, llm_response, all_products):
        """
        Parse the LLM response to extract product recommendations
        
        Parameters:
        - llm_response (str): Raw response from the LLM
        - all_products (list): Full product catalog to match IDs with full product info
        
        Returns:
        - dict: Structured recommendations
        """
        # TODO: Implement response parsing logic
        # THIS FUNCTION MUST BE IMPLEMENTED BY THE CANDIDATE
        
        # Example implementation (very basic, should be improved):
        try:
            import json
            import re
            # Attempt to parse JSON from the response
            # Note: This is a simplistic approach and should be made more robust
            # The candidate should implement better parsing logic
            
            # Find JSON content in the response
            code_block_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
            code_block_match = re.search(code_block_pattern, llm_response)
            
            if code_block_match:
                # Extract content from inside code blocks
                json_str = code_block_match.group(1)
            else:
                # Fall back to original approach - find JSON array directly
                start_idx = llm_response.find('[')
                end_idx = llm_response.rfind(']') + 1
                
                if start_idx == -1 or end_idx == 0:
                    # Fallback if JSON parsing fails
                    return {
                        "recommendations": [],
                        "error": "Could not parse recommendations from LLM response"
                    }
                
                json_str = llm_response[start_idx:end_idx]
            
            rec_data = json.loads(json_str)
            
            # Enrich recommendations with full product details
            recommendations = []
            for rec in rec_data:
                product_id = rec.get('product_id')
                product_details = None
                
                # Find the full product details
                for product in all_products:
                    if product['id'] == product_id:
                        product_details = product
                        break
                
                if product_details:
                    recommendations.append({
                        "product": product_details,
                        "explanation": rec.get('explanation', ''),
                        "confidence_score": rec.get('score', 5)
                    })
            #print(recommendations)
            return {
                "recommendations": recommendations,
                "count": len(recommendations)
            }
            
        except Exception as e:
            print(f"Error parsing LLM response: {str(e)}")
            return {
                "recommendations": [],
                "error": f"Failed to parse recommendations: {str(e)}"
            }