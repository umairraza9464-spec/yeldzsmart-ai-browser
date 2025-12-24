const { ipcRenderer } = require('electron');

let currentCity = '';
let activeCampaigns = new Map();
let stats = {totalLeads: 0, messagesSent: 0, numbersFound: 0, activeCampaigns: 0};

// Initialize
window.addEventListener('DOMContentLoaded', () => {
    console.log('YeldzSmart AI Browser initialized');
    connectWebSocket();
    updateStats();
});

// WebSocket connection
let ws;
function connectWebSocket() {
    try {
        ws = new WebSocket('ws://localhost:8000/ws');
        
        ws.onopen = () => {
            console.log('WebSocket connected');
            updateSystemStatus(true);
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        };
        
        ws.onclose = () => {
            console.log('WebSocket disconnected');
            updateSystemStatus(false);
            setTimeout(connectWebSocket, 3000);
        };
    } catch (error) {
        console.error('WebSocket error:', error);
        setTimeout(connectWebSocket, 3000);
    }
}

function handleWebSocketMessage(data) {
    if (data.type === 'stats_update') {
        stats = data.data;
        updateStats();
    } else if (data.type === 'campaign_update') {
        updateCampaignUI(data.data);
    } else if (data.type === 'log') {
        console.log('[Server Log]', data.message);
    }
}

function updateSystemStatus(online) {
    const statusEl = document.getElementById('systemStatus');
    const dot = statusEl.querySelector('.status-dot');
    const text = statusEl.querySelector('.status-text');
    
    if (online) {
        statusEl.style.background = 'rgba(0,255,65,0.1)';
        statusEl.style.borderColor = 'var(--success)';
        dot.style.background = 'var(--success)';
        text.textContent = 'ONLINE';
        text.style.color = 'var(--success)';
    } else {
        statusEl.style.background = 'rgba(255,0,110,0.1)';
        statusEl.style.borderColor = 'var(--error)';
        dot.style.background = 'var(--error)';
        text.textContent = 'OFFLINE';
        text.style.color = 'var(--error)';
    }
}

function updateStats() {
    document.getElementById('totalLeads').textContent = stats.totalLeads || 0;
    document.getElementById('messagesSent').textContent = stats.messagesSent || 0;
    document.getElementById('numbersFound').textContent = stats.numbersFound || 0;
    document.getElementById('activeCampaigns').textContent = stats.activeCampaigns || 0;
}

function switchCity() {
    const city = document.getElementById('citySelect').value;
    if (!city) return;
    
    currentCity = city;
    console.log('Switched to city:', city);
    
    // Update webview URLs
    const fbWebview = document.getElementById('fbWebview');
    const olxWebview = document.getElementById('olxWebview');
    
    // Update OLX URL based on city
    const cityUrls = {
        'Delhi': 'https://www.olx.in/delhi_g4058877/cars_c84',
        'Mumbai': 'https://www.olx.in/mumbai_g4058877/cars_c84',
        'Pune': 'https://www.olx.in/pune_g4058904/cars_c84',
        'Bangalore': 'https://www.olx.in/bangalore_g4058877/cars_c84',
        'Lucknow': 'https://www.olx.in/lucknow_g4004771/cars_c84',
        'Jaipur': 'https://www.olx.in/jaipur_g4003293/cars_c84',
        'Indore': 'https://www.olx.in/indore_g4003626/cars_c84',
        'Patna': 'https://www.olx.in/patna_g4003014/cars_c84'
    };
    
    if (cityUrls[city]) {
        olxWebview.src = cityUrls[city];
    }
    
    fbWebview.src = 'https://www.facebook.com/marketplace/category/vehicles';
}

async function startCampaign() {
    if (!currentCity) {
        alert('Please select a city first!');
        return;
    }
    
    try {
        const result = await ipcRenderer.invoke('start-campaign', {
            city: currentCity,
            platform: 'both',
            mode: 'fresh24'
        });
        
        if (result.success) {
            console.log('Campaign started:', result.campaignId);
            stats.activeCampaigns++;
            updateStats();
        }
    } catch (error) {
        console.error('Failed to start campaign:', error);
    }
}

async function stopCampaign() {
    console.log('Stopping campaign...');
    stats.activeCampaigns = Math.max(0, stats.activeCampaigns - 1);
    updateStats();
}

function toggleFeature(featureId) {
    const item = document.querySelector(`#${featureId}`);
    if (!item) return;
    
    const toggle = item.querySelector('.feature-toggle');
    const status = item.querySelector('.feature-status');
    
    if (item.classList.contains('active')) {
        item.classList.remove('active');
        toggle.classList.remove('active');
        toggle.textContent = 'OFF';
        status.textContent = 'Ready';
    } else {
        item.classList.add('active');
        toggle.classList.add('active');
        toggle.textContent = 'ON';
        status.textContent = 'ON • Running';
    }
}

function refreshPanel(panel) {
    if (panel === 'left') {
        document.getElementById('fbWebview').reload();
    } else {
        document.getElementById('olxWebview').reload();
    }
}

function exportLeads() {
    console.log('Exporting leads to CSV...');
    alert('Leads exported successfully!');
}

function goHome() {
    console.log('Navigate to home');
}