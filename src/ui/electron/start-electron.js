import { app, BrowserWindow } from 'electron/main'
import path from 'path'

function createWindow() {
    const win = new BrowserWindow({
        width: 1400,
        height: 750,
        autoHideMenuBar: true,
        webPreferences: {
            // preload: path.join(__dirname, 'preload.js'),
        },
    })

    win.loadFile('vue-dist/index.html')
}

app.whenReady().then(() => {
    createWindow()

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow()
        }
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})
