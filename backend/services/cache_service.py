import datetime
import hashlib
import json
import os
import time


class LLMCacheService:
    """
    Service to cache LLM responses to improve performance and reduce API costs.
    Implements a simple file-based caching system with TTL (time-to-live).
    """
    
    def __init__(self, cache_dir="cache", ttl_hours=24):
        """
        Initialize the cache service
        
        Parameters:
        - cache_dir (str): Directory to store cache files
        - ttl_hours (int): Time-to-live for cache entries in hours
        """
        self.cache_dir = cache_dir
        self.ttl_hours = float(ttl_hours)
        
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def _generate_cache_key(self, user_preferences, browsing_history):
        """
        Generate a unique cache key based on user preferences and browsing history
        
        Returns:
        - str: A hash that uniquely identifies this recommendation request
        """

        key_data = {
            "preferences": user_preferences,
            "browsing_history": browsing_history,
            "version": "1.0"
        }
        
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _get_cache_file_path(self, cache_key):
        """Get the file path for a cache key"""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get_cached_recommendations(self, user_preferences, browsing_history):
        """
        Try to get cached recommendations for the given parameters
        
        Returns:
        - dict or None: Cached recommendations if found and valid, None otherwise
        """
        cache_key = self._generate_cache_key(user_preferences, browsing_history)
        cache_file = self._get_cache_file_path(cache_key)
        
        # checking for cache file
        if not os.path.exists(cache_file):
            return None
        
        try:
            # reading cache file
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # checking expiry of cache file
            timestamp = cache_data.get('timestamp', 0)
            current_time = time.time()
            ttl_seconds = self.ttl_hours * 3600
            
            if current_time - timestamp > ttl_seconds:
                print(f"Cache expired for key: {cache_key}")
                return None
            
            # return cached recommendations
            print(f"Cache hit for key: {cache_key}")
            return cache_data.get('recommendations')
        
        except Exception as e:
            print(f"Error reading cache: {str(e)}")
            return None
    
    def cache_recommendations(self, user_preferences, browsing_history, recommendations):
        """
        Cache recommendations for future use
        
        Parameters:
        - user_preferences (dict): User preferences used for recommendation
        - browsing_history (list): User browsing history used for recommendation
        - recommendations (dict): Recommendation results to cache
        
        Returns:
        - bool: True if successfully cached, False otherwise
        """
        cache_key = self._generate_cache_key(user_preferences, browsing_history)
        cache_file = self._get_cache_file_path(cache_key)
        
        try:
            #  cache data structure
            cache_data = {
                'timestamp': time.time(),
                'recommendations': recommendations,
                'metadata': {
                    'cache_date': datetime.datetime.now().isoformat(),
                    'expires_at': (datetime.datetime.now() + datetime.timedelta(hours=self.ttl_hours)).isoformat(),
                    'preferences': user_preferences,
                    'browsing_history_count': len(browsing_history)
                }
            }
            
            # write to cache file
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
            
            print(f"Cached recommendations for key: {cache_key}")
            return True
        
        except Exception as e:
            print(f"Error writing cache: {str(e)}")
            return False
    
    def clear_expired_cache(self):
        """
        Clear all expired cache entries
        
        Returns:
        - int: Number of cache entries cleared
        """
        cleared_count = 0
        current_time = time.time()
        ttl_seconds = self.ttl_hours * 3600
        
        for filename in os.listdir(self.cache_dir):
            if not filename.endswith('.json'):
                continue
                
            cache_file = os.path.join(self.cache_dir, filename)
            
            try:
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                timestamp = cache_data.get('timestamp', 0)
                
                if current_time - timestamp > ttl_seconds:
                    # delete expired cache file
                    os.remove(cache_file)
                    cleared_count += 1
            
            except Exception as e:
                print(f"Error clearing cache file {filename}: {str(e)}")
                # delete invalid cache file
                try:
                    os.remove(cache_file)
                    cleared_count += 1
                except:
                    pass
        
        return cleared_count
    
    def clear_all_cache(self):
        """
        Clear all cache entries regardless of expiration
        
        Returns:
        - int: Number of cache entries cleared
        """
        cleared_count = 0
        
        for filename in os.listdir(self.cache_dir):
            if not filename.endswith('.json'):
                continue
                
            cache_file = os.path.join(self.cache_dir, filename)
            
            try:
                os.remove(cache_file)
                cleared_count += 1
            except Exception as e:
                print(f"Error deleting cache file {filename}: {str(e)}")
        
        return cleared_count
    
    def get_cache_stats(self):
        """
        Get statistics about the current cache
        
        Returns:
        - dict: Cache statistics
        """
        total_entries = 0
        total_size = 0
        expired_entries = 0
        current_time = time.time()
        ttl_seconds = self.ttl_hours * 3600
        
        for filename in os.listdir(self.cache_dir):
            if not filename.endswith('.json'):
                continue
                
            cache_file = os.path.join(self.cache_dir, filename)
            
            try:
                size = os.path.getsize(cache_file)
                total_size += size
                total_entries += 1
                
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                timestamp = cache_data.get('timestamp', 0)
                
                if current_time - timestamp > ttl_seconds:
                    expired_entries += 1
            
            except Exception:
                pass
        
        return {
            'total_entries': total_entries,
            'active_entries': total_entries - expired_entries,
            'expired_entries': expired_entries,
            'total_size_kb': round(total_size / 1024, 2),
            'ttl_hours': self.ttl_hours,
            'cache_dir': self.cache_dir
        }