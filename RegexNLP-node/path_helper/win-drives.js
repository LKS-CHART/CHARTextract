const childProcess = require('child_process');
const tableParser = require('table-parser');
const path = require('path');
const command = 'wmic logicaldisk get caption';

function usedLetters() {
    return new Promise((resolve, reject) => {
        childProcess.exec(command, (err, stdout) => {
            if (err) {
                return reject(err);
            }

            const letters = tableParser.parse(stdout).map((caption) => {
                return caption.Caption[0];
            });

            resolve(letters);
        });
    });
}

module.exports.usedLetters = usedLetters;

function usedLettersSync() {
    const stdout = childProcess.execSync(command);
    return tableParser.parse(stdout.toString()).map((caption) => {
        return caption.Caption[0];
    });
}

module.exports.usedLettersSync = usedLettersSync;