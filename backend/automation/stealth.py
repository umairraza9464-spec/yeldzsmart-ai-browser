# Anti-Ban Stealth System
import random
import asyncio
from fake_useragent import UserAgent

class StealthSystem:
    """Anti-detection and anti-ban utilities"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.request_count = 0
        self.last_request_time = None
    
    def get_random_user_agent(self):
        """Get random user agent"""
        return self.ua.random
    
    async def human_delay(self, min_sec=1, max_sec=3):
        """Simulate human delay"""
        delay = random.uniform(min_sec, max_sec)
        await asyncio.sleep(delay)
    
    async def random_mouse_movement(self, page):
        """Simulate random mouse movements"""
        try:
            width = 1920
            height = 1080
            
            for _ in range(random.randint(2, 5)):
                x = random.randint(0, width)
                y = random.randint(0, height)
                await page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.1, 0.3))
        except:
            pass
    
    async def random_scroll(self, page):
        """Random scrolling behavior"""
        try:
            for _ in range(random.randint(2, 4)):
                await page.evaluate(f'window.scrollBy(0, {random.randint(100, 500)})')
                await asyncio.sleep(random.uniform(0.5, 1.5))
        except:
            pass
    
    def should_rate_limit(self, max_requests_per_min=20):
        """Check if should rate limit"""
        self.request_count += 1
        
        if self.request_count >= max_requests_per_min:
            return True
        
        return False
    
    async def apply_stealth_to_page(self, page):
        """Apply stealth scripts to page"""
        await page.add_init_script("""
            // Remove webdriver
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            
            // Override plugins
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            
            // Chrome detection
            window.chrome = {runtime: {}};
            
            // Permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({state: Notification.permission}) :
                originalQuery(parameters)
            );
        """)
        
        print("[Stealth] Applied anti-detection scripts")
    
    def get_random_viewport(self):
        """Get random viewport size"""
        viewports = [
            {'width': 1920, 'height': 1080},
            {'width': 1366, 'height': 768},
            {'width': 1536, 'height': 864},
            {'width': 1440, 'height': 900}
        ]
        return random.choice(viewports)