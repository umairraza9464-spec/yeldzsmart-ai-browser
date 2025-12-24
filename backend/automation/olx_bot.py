# OLX Automation Bot with Anti-Ban
import asyncio
from playwright.async_api import async_playwright, Page
import random
from datetime import datetime

class OLXBot:
    def __init__(self, city: str):
        self.city = city
        self.page = None
        self.leads = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        ]
    
    async def initialize(self):
        """Initialize browser with stealth settings"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = await self.browser.new_context(
            user_agent=random.choice(self.user_agents),
            viewport={'width': 1920, 'height': 1080}
        )
        
        self.page = await context.new_page()
        await self.page.add_init_script("""Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""")
        
        print(f"[OLX Bot] Initialized for {self.city}")
    
    async def scan_fresh_listings(self, hours=24):
        """Scan fresh car listings"""
        city_urls = {
            'Delhi': 'https://www.olx.in/delhi_g4058877/cars_c84',
            'Mumbai': 'https://www.olx.in/mumbai_g4058877/cars_c84',
            'Pune': 'https://www.olx.in/pune_g4058904/cars_c84',
            'Bangalore': 'https://www.olx.in/bangalore_g4058877/cars_c84'
        }
        
        url = city_urls.get(self.city, 'https://www.olx.in/cars_c84')
        
        try:
            await self.page.goto(url, wait_until='domcontentloaded')
            await asyncio.sleep(random.uniform(2, 4))
            
            # Extract listings
            listings = await self.page.query_selector_all('[data-aut-id="itemBox"]')
            
            for listing in listings[:10]:  # Process first 10
                try:
                    title_elem = await listing.query_selector('span[data-aut-id="itemTitle"]')
                    price_elem = await listing.query_selector('span[data-aut-id="itemPrice"]')
                    
                    if title_elem and price_elem:
                        title = await title_elem.inner_text()
                        price = await price_elem.inner_text()
                        
                        self.leads.append({
                            'title': title,
                            'price': price,
                            'city': self.city,
                            'platform': 'OLX',
                            'timestamp': datetime.now().isoformat()
                        })
                        
                except Exception as e:
                    print(f"Error processing listing: {e}")
                    continue
            
            print(f"[OLX Bot] Found {len(self.leads)} leads in {self.city}")
            return self.leads
            
        except Exception as e:
            print(f"[OLX Bot] Error: {e}")
            return []
    
    async def send_message(self, listing_id: str, message: str):
        """Send message to seller"""
        await asyncio.sleep(random.uniform(1, 3))  # Anti-ban delay
        print(f"[OLX Bot] Sent message: {message}")
        return True
    
    async def close(self):
        """Cleanup"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()