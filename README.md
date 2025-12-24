# 🚀 YeldzSmart AI Browser v9.0

**The Ultimate AI-Powered Automation Browser for Lead Generation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Production Ready](https://img.shields.io/badge/status-production-green.svg)]()

---

## ✨ Features

### 🌐 **Multi-City Campaign Manager**
- **8 Cities Parallel**: Delhi, Mumbai, Pune, Bangalore, Lucknow, Jaipur, Indore, Patna
- **Split-Screen Automation**: FB Marketplace (left) + OLX (right) simultaneously
- **Per-City Isolation**: Separate sessions, cookies, and profiles

### 🤖 **AI-Powered Automation (Comet AI Style)**
- **Perplexity AI Integration**: Smart chat for lead qualification
- **Auto-Baiting System**: Intelligent message responses
- **Photo OCR**: Extract phone numbers from images
- **Anti-Ban Technology**: Human-like behavior simulation

### 🛡️ **Anti-Detection Features**
- Randomized user agents per city
- Cookie rotation and session management
- Human-like mouse movements and typing
- Proxy support (optional)
- Fingerprint randomization

### 📊 **Real-Time Dashboard**
- Live statistics (leads, messages, phone numbers)
- WebSocket-powered updates
- Campaign progress tracking
- Export leads to CSV/Google Sheets

### 🔌 **Extension Support**
- Chrome extension compatible
- Custom automation extensions included
- Per-campaign extension loading

---

## 📦 Installation

### **Method 1: One-Click Setup (Recommended)**

#### Windows:
```bash
# Download and extract ZIP
# Double-click: INSTALL_AND_RUN.bat
```

#### Mac/Linux:
```bash
# Download and extract ZIP
chmod +x install.sh
./install.sh
```

### **Method 2: Manual Setup**

1. **Clone Repository**
```bash
git clone https://github.com/umairraza9464-spec/yeldzsmart-ai-browser.git
cd yeldzsmart-ai-browser
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
playwright install chromium
```

3. **Run Application**
```bash
python start.py
```

---

## 🚀 Quick Start

### **Starting the Browser**

```bash
# Option 1: Simple start
python start.py

# Option 2: With specific city
python start.py --city Delhi

# Option 3: Multi-city mode (8 cities parallel)
python start.py --multi-city

# Option 4: Debug mode
python start.py --debug
```

### **Using the Dashboard**

1. Open browser at: `http://localhost:8000`
2. Select city from dropdown
3. Click "Start Campaign" for OLX or Facebook
4. Watch automation in split-screen mode
5. Export leads when done

---

## 📁 Project Structure

```
yeldzsmart-ai-browser/
│
├── start.py                 # Main entry point
├── requirements.txt         # Python dependencies
├── INSTALL_AND_RUN.bat     # Windows one-click installer
├── install.sh              # Mac/Linux installer
│
├── backend/
│   ├── main.py             # FastAPI server
│   ├── automation/
│   │   ├── olx_bot.py      # OLX automation
│   │   ├── fb_bot.py       # Facebook automation
│   │   ├── stealth.py      # Anti-ban utilities
│   │   └── ai_agent.py     # AI automation controller
│   ├── database/
│   │   └── models.py       # Database models
│   └── config/
│       └── settings.py     # Configuration
│
├── frontend/
│   ├── index.html          # Main dashboard
│   ├── assets/
│   │   ├── css/           # Stylesheets
│   │   └── js/            # JavaScript
│   └── components/         # UI components
│
├── extensions/
│   ├── perplexity-ai/     # Perplexity AI extension
│   ├── auto-baiting/      # Auto-response system
│   └── photo-ocr/         # OCR for phone numbers
│
├── data/
│   ├── leads.db           # SQLite database
│   └── exports/           # CSV exports
│
├── cookies/               # Session cookies per city
├── logs/                  # Application logs
└── screenshots/           # Debug screenshots
```

---

## 🎯 Usage Examples

### **Example 1: Single City Campaign**

```python
from backend.automation import OLXBot

bot = OLXBot(city="Delhi")
await bot.initialize()

# Scan fresh 24H listings
leads = await bot.scan_fresh_listings(hours=24)

# Auto-message all leads
for lead in leads:
    await bot.send_message(lead['id'], "Hi! Is this car still available?")

print(f"Found {len(leads)} leads")
```

### **Example 2: Multi-City Parallel**

```python
import asyncio
from backend.automation import MultiCityManager

manager = MultiCityManager()
cities = ["Delhi", "Mumbai", "Pune", "Bangalore"]

# Run all cities in parallel
results = await manager.run_parallel(cities, platform="olx")

for city, leads in results.items():
    print(f"{city}: {len(leads)} leads found")
```

### **Example 3: AI-Powered Chat**

```python
from backend.automation import AIAgent

agent = AIAgent()

# Auto-respond to seller queries
response = await agent.generate_response(
    seller_message="Yes, car is available. What's your budget?",
    context={"car_price": 500000, "our_budget": 450000}
)

print(response)  # "My budget is around 4.5 lakhs. Can we negotiate?"
```

---

## ⚙️ Configuration

### **Environment Variables (.env)**

```bash
# Backend Settings
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Anti-Ban Settings
USE_PROXIES=True
PROXY_API_KEY=your_proxy_key_here
HEADLESS=False
RATE_LIMIT_OLX=20
RATE_LIMIT_FB=10

# Google Sheets Integration
GOOGLE_SHEETS_WEBHOOK=https://script.google.com/macros/s/YOUR_ID/exec
GOOGLE_SHEET_ID=your_sheet_id

# AI Settings (Optional)
GEMINI_API_KEY=your_gemini_key
LLAMA_API_KEY=your_llama_key
PERPLEXITY_API_KEY=your_perplexity_key

# OCR Settings
TESSERACT_PATH=/usr/bin/tesseract  # Windows: C:\\Program Files\\Tesseract-OCR\\tesseract.exe
```

---

## 🛡️ Anti-Ban Best Practices

1. **Rate Limiting**: Maximum 20 requests/min for OLX, 10 for Facebook
2. **Session Rotation**: Auto-rotate cookies every 2 hours
3. **Human Behavior**: Random delays (2-5 seconds) between actions
4. **Proxy Usage**: Recommended for heavy usage
5. **Headless Mode**: OFF for better stealth (can use visible browser)

---

## 📊 Dashboard Preview

### Main Interface:
- **Left Sidebar**: Automation panels, city selector, features toggle
- **Center**: Split-screen browser (FB + OLX)
- **Right Panel**: Real-time logs, stats, lead preview
- **Top Bar**: Navigation tabs, campaign controls

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

---

## ⚠️ Disclaimer

This tool is for **educational and personal use only**. Users are responsible for:
- Complying with platform Terms of Service
- Following local laws and regulations
- Not using for spam or harassment
- Respecting rate limits and anti-scraping measures

The authors are not liable for misuse.

---

## 🆘 Support

### Issues?
- Create GitHub issue: [Issues Page](https://github.com/umairraza9464-spec/yeldzsmart-ai-browser/issues)
- Check [Wiki](https://github.com/umairraza9464-spec/yeldzsmart-ai-browser/wiki) for guides

### Need Help?
- **Discord**: [Join Community](#)
- **Email**: support@yeldzsmart.com

---

## 🎉 Acknowledgments

- Inspired by **Comet AI Browser**
- Built with **Playwright**, **FastAPI**, **React**
- Special thanks to open-source community

---

## 📈 Roadmap

### v9.1 (Coming Soon)
- [ ] Cars24, Spinny automation support
- [ ] Instagram DM automation
- [ ] WhatsApp integration
- [ ] Cloud deployment support
- [ ] Mobile app (iOS/Android)

### v10.0 (Future)
- [ ] Multi-language support
- [ ] Advanced AI models (GPT-4, Claude)
- [ ] Team collaboration features
- [ ] Enterprise dashboard

---

**Made with ❤️ by YeldzSmart Team**

⭐ **Star this repo if you found it helpful!**