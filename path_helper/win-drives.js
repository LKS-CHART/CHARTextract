const childProcess = require('child_process');
const tableParser = require('table-parser');

const command = 'wmic logicaldisk get caption';

function removeUsedLetters(usedLetters) {
    const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    for (let i = 0; i < usedLetters.length; i++) {
        letters.splice(letters.indexOf(usedLetters[i]), letters.indexOf(":"));
    }

    return letters;
}

function letters() {
    return new Promise((resolve, reject) => {
        childProcess.exec(command, (err, stdout) => {
            if (err) {
                return reject(err);
            }

            const letters = tableParser.parse(stdout).map((caption) => {
                return caption.Caption[0];
            });

            resolve(removeUsedLetters(letters));
        });
    });
}

module.exports.letters = letters;

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