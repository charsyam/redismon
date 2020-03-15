// Modules to control application life and create native browser window
const {app, BrowserWindow, ipcMain} = require('electron')
const path = require('path')
const notifier = require('node-notifier')
const redis = require("redis")

const redisHost = "192.168.123.103"
//const redisClient = redis.createClient(6379, redisHost);

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      allowRunningInsecureContent: true,
      nodeIntegration: true
    }
  })

  // and load the index.html of the app.
  mainWindow.loadFile('index.html')
  notifier.notify ({
    appName: "com.myapp.id",
    title: "Electron Notifer",
    message: "Hello, World!"
  })
  // Open the DevTools.
//  mainWindow.webContents.openDevTools()
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') app.quit()
})
console.log("test")
app.on('activate', function () {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

ipcMain.on('form-submission', function(event, redisAddress) {
  console.log("this is the redis Address from the form -> " + redisAddress)
  event.sender.send('form-reply', redisAddress );

  notifier.notify ({
    appName: "com.myapp.id",
    title: "Electron Notifer",
    message: redisAddress
  })
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

//redisClient.on("error", function(error) {
//  console.error(error)
//});

//redisClient.set("foo", "bar");
//redisClient.set(["hello", "world"]);