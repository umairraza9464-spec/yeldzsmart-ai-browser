const { app, BrowserWindow, ipcMain, session } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonServer;
const campaigns = new Map();

function startBackend() {
    const pythonPath = process.platform === 'win32' ? 'python' : 'python3';
    const serverPath = path.join(__dirname, '..', 'backend', 'server.py');
    
    pythonServer = spawn(pythonPath, [serverPath], {
        cwd: path.join(__dirname, '..'),
        stdio: 'pipe'
    });
    
    pythonServer.stdout.on('data', (data) => {
        console.log(`[Backend] ${data}`);
    });
    
    pythonServer.stderr.on('data', (data) => {
        console.error(`[Backend Error] ${data}`);
    });
    
    pythonServer.on('error', (error) => {
        console.error('Failed to start backend:', error);
    });
}

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1920,
        height: 1080,
        minWidth: 1280,
        minHeight: 720,
        backgroundColor: '#0a0e27',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            webviewTag: true,
            enableRemoteModule: true,
            partition: 'persist:main'
        },
        icon: path.join(__dirname, 'icon.png'),
        title: 'YeldzSmart AI Browser v9.0 [HYPER-FUNCTIONAL]',
        frame: true,
        autoHideMenuBar: true
    });
    
    mainWindow.loadFile(path.join(__dirname, 'ui', 'index.html'));
    mainWindow.maximize();
    
    // Enable DevTools in dev mode
    if (process.argv.includes('--dev') || process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }
    
    // Setup sessions for each city
    setupCitySessions();
    
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

function setupCitySessions() {
    const cities = ['Delhi', 'Mumbai', 'Pune', 'Bangalore', 'Lucknow', 'Jaipur', 'Indore', 'Patna'];
    
    cities.forEach(city => {
        const ses = session.fromPartition(`persist:${city}`);
        
        // Set user agent
        ses.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
        
        // Anti-detection headers
        ses.webRequest.onBeforeSendHeaders((details, callback) => {
            details.requestHeaders['Accept-Language'] = 'en-US,en;q=0.9';
            details.requestHeaders['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8';
            callback({ requestHeaders: details.requestHeaders });
        });
    });
}

// IPC Handlers
ipcMain.handle('start-campaign', async (event, config) => {
    const campaignId = `${config.platform}_${config.city}_${Date.now()}`;
    
    campaigns.set(campaignId, {
        city: config.city,
        platform: config.platform,
        mode: config.mode,
        status: 'running',
        startTime: Date.now(),
        leads: 0
    });
    
    console.log(`[Campaign] Started: ${campaignId}`);
    
    return { success: true, campaignId };
});

ipcMain.handle('stop-campaign', async (event, campaignId) => {
    if (campaigns.has(campaignId)) {
        campaigns.delete(campaignId);
        console.log(`[Campaign] Stopped: ${campaignId}`);
        return { success: true };
    }
    return { success: false, error: 'Campaign not found' };
});

ipcMain.handle('get-campaigns', async () => {
    return Array.from(campaigns.entries()).map(([id, data]) => ({
        id,
        ...data
    }));
});

// App lifecycle
app.whenReady().then(() => {
    console.log('[YeldzSmart] Starting application...');
    
    // Start backend server
    startBackend();
    
    // Wait 2 seconds for backend to initialize
    setTimeout(() => {
        createWindow();
        console.log('[YeldzSmart] Window created');
    }, 2000);
    
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (pythonServer) {
        pythonServer.kill();
    }
    app.quit();
});

app.on('before-quit', () => {
    console.log('[YeldzSmart] Shutting down...');
    if (pythonServer) {
        pythonServer.kill();
    }
});

app.on('will-quit', () => {
    // Cleanup
    campaigns.clear();
});