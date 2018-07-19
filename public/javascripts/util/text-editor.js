var editor = ace.edit("editor-container");
var Range = require("ace/range").Range;

editor.setOptions({
    useWrapMode: true
})
editor.getSession().setUseWrapMode(true)

var illegal_chars = new Set(["!", ";", ",", "\\", "/", "\"", "'"])

editor.commands.on("exec", function(e) {
    var rowCol = editor.selection.getCursor();
    if(rowCol.row == 0) {
        if(e.args !== "\n" && e.args !== "\r") {
            e.preventDefault();
            e.stopPropagation();
        }
    }
})


document.getElementById('editor-container').style.fontSize='20px';
console.log("In text-editor")
