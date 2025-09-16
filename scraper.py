#!/usr/bin/env python3
"""
Reddit Image Scraper
Main script to scrape Reddit posts with images from a specified subreddit
"""

import json
import time
import requests
from typing import List, Dict, Optional
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RedditScraper:
    """
    A class to scrape Reddit posts with images from specified subreddits
    """
    
    def __init__(self, subreddit: str, user_agent: str = None):
        """
        Initialize the Reddit scraper
        
        Args:
            subreddit: Name of the subreddit to scrape (without r/)
            user_agent: Custom user agent for requests
        """
        self.subreddit = subreddit
        self.base_url = f"https://www.reddit.com/r/{subreddit}"
        self.headers = {
            'User-Agent': user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.posts_with_images = []
        
    def fetch_page(self, after: Optional[str] = None, limit: int = 25) -> Dict:
        """
        Fetch a single page of posts from Reddit
        
        Args:
            after: The 'after' parameter for pagination
            limit: Number of posts per page
            
        Returns:
            JSON response from Reddit API
        """
        params = {
            'limit': limit,
            'raw_json': 1
        }
        if after:
            params['after'] = after
            
        url = f"{self.base_url}.json"
        
        try:
            logger.info(f"Fetching page with after={after}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            # Add delay to be respectful to Reddit's servers
            time.sleep(2)
            
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching page: {e}")
            return None
    
    def extract_image_url(self, post_data: Dict) -> Optional[str]:
        """
        Extract image URL from a Reddit post
        
        Args:
            post_data: The post data dictionary
            
        Returns:
            Image URL if found, None otherwise
        """
        # Check for direct image URL
        if 'url' in post_data:
            url = post_data['url']
            # Common image extensions
            if any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                return url
        
        # Check for Reddit hosted images
        if 'preview' in post_data and 'images' in post_data['preview']:
            images = post_data['preview']['images']
            if images and len(images) > 0:
                # Get the source image URL
                if 'source' in images[0]:
                    image_url = images[0]['source']['url']
                    # Reddit encodes URLs, we need to decode them
                    image_url = image_url.replace('&amp;', '&')
                    return image_url
        
        # Check for gallery data (multiple images)
        if 'gallery_data' in post_data and 'media_metadata' in post_data:
            media = post_data['media_metadata']
            if media:
                # Get the first image from gallery
                first_media_id = list(media.keys())[0]
                if 's' in media[first_media_id]:
                    image_url = media[first_media_id]['s']['u']
                    image_url = image_url.replace('&amp;', '&')
                    return image_url
        
        return None
    
    def process_posts(self, posts_data: Dict) -> List[Dict]:
        """
        Process posts and extract those with images
        
        Args:
            posts_data: Raw posts data from Reddit API
            
        Returns:
            List of posts with images
        """
        posts_with_images = []
        
        if not posts_data or 'data' not in posts_data:
            return posts_with_images
        
        children = posts_data['data'].get('children', [])
        
        for child in children:
            if child['kind'] != 't3':  # t3 is for posts
                continue
                
            post = child['data']
            image_url = self.extract_image_url(post)
            
            if image_url:
                post_info = {
                    'post_title': post.get('title', 'No Title'),
                    'image_url': image_url,
                    'post_url': f"https://www.reddit.com{post.get('permalink', '')}",
                    'author': post.get('author', 'Unknown'),
                    'score': post.get('score', 0),
                    'created_utc': post.get('created_utc', 0),
                    'num_comments': post.get('num_comments', 0),
                    'subreddit': post.get('subreddit', '')
                }
                posts_with_images.append(post_info)
                logger.info(f"Found image post: {post_info['post_title'][:50]}...")
        
        return posts_with_images
    
    def scrape(self, num_pages: int = 10) -> List[Dict]:
        """
        Scrape multiple pages from the subreddit
        
        Args:
            num_pages: Number of pages to scrape
            
        Returns:
            List of all posts with images
        """
        logger.info(f"Starting to scrape r/{self.subreddit} for {num_pages} pages")
        
        after = None
        pages_scraped = 0
        
        while pages_scraped < num_pages:
            page_data = self.fetch_page(after=after)
            
            if not page_data:
                logger.warning("Failed to fetch page, stopping")
                break
            
            posts = self.process_posts(page_data)
            self.posts_with_images.extend(posts)
            
            # Get the 'after' parameter for next page
            after = page_data['data'].get('after')
            pages_scraped += 1
            
            logger.info(f"Scraped page {pages_scraped}/{num_pages}, found {len(posts)} posts with images")
            
            if not after:
                logger.info("No more pages available")
                break
        
        logger.info(f"Scraping complete! Total posts with images: {len(self.posts_with_images)}")
        return self.posts_with_images
    
    def save_to_json(self, filename: str = None) -> str:
        """
        Save scraped posts to JSON file
        
        Args:
            filename: Output filename (default: reddit_posts_{timestamp}.json)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"reddit_posts_{timestamp}.json"
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        filepath = os.path.join('output', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.posts_with_images, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data saved to {filepath}")
        return filepath


def main():
    """
    Main function to run the scraper
    """
    # Configuration
    SUBREDDIT = 'malaysia'  # Change this to your preferred subreddit
    NUM_PAGES = 10
    
    # Create scraper instance
    scraper = RedditScraper(subreddit=SUBREDDIT)
    
    # Scrape posts
    posts = scraper.scrape(num_pages=NUM_PAGES)
    
    # Save to JSON
    output_file = scraper.save_to_json(f'{SUBREDDIT}_posts.json')
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Scraping Summary")
    print(f"{'='*50}")
    print(f"Subreddit: r/{SUBREDDIT}")
    print(f"Pages scraped: {NUM_PAGES}")
    print(f"Posts with images found: {len(posts)}")
    print(f"Output saved to: {output_file}")
    print(f"{'='*50}\n")
    
    # Show sample of scraped data
    if posts:
        print("Sample of scraped posts:")
        for i, post in enumerate(posts[:3], 1):
            print(f"\n{i}. Title: {post['post_title'][:60]}...")
            print(f"   Image: {post['image_url'][:60]}...")
            print(f"   Score: {post['score']} | Comments: {post['num_comments']}")


if __name__ == "__main__":
    main()
