const path = require("path");
let appDir = __dirname;
let isDev = null;
if (require('electron').app === undefined) {
    console.log("Node Server Development Environment");
    isDev = true;
} else {
    isDev = path.basename(process.execPath).startsWith("electron");

    if (isDev){
        console.log("Electron Development Environment");
    } else {
        appDir = require('electron').app.getAppPath();
    }
}

function getAppRoot() {
    if (isDev){
        return path.join( appDir, "..");
    } else {
        if ( process.platform === 'win32' ) {
            return path.join( appDir, '/../../' );
        }  else {
            return path.join( appDir, '/../../../' );
        }
    }
}

module.exports.getAppRoot = getAppRoot;