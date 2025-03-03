const { app, BrowserWindow } = require('electron');

function createWindow() {
    let win = new BrowserWindow({
        width: 1000,
        height: 700,
        webPreferences: {
            nodeIntegration: true
        }
    });

    win.loadURL('http://localhost:5000');  // Load Flask UI
}

app.whenReady().then(createWindow);
