const path = require("path");
const appDir = require('electron').app.getAppPath();
const isDev = path.basename(process.execPath).startsWith("electron");

function getAppRoot() {
    if (isDev){
        console.log("Development Environment");
        return path.join(__dirname, "..");
    } else {
        if ( process.platform === 'win32' ) {
            return path.join( appDir, '/../../' );
        }  else {
            return path.join( appDir, '/../../../' );
        }
    }
}

module.exports.getAppRoot = getAppRoot;