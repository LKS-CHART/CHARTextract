var editor = ace.edit("editor-container");
editor.setOptions({
    useWrapMode: true
})
editor.getSession().setUseWrapMode(true)

var illegal_chars = new Set(["!", ";", ",", "\\", "/", "\"", "'"])

editor.commands.on("exec", function(e) {
    var rowCol = editor.selection.getCursor();
    if(rowCol.row == 0) {
        if(rowCol.column === 0) {
            e.preventDefault();
            e.stopPropagation();
        }

        if(rowCol.column === 1) {
            console.log(e.args);
            if(e.args === undefined || e.args === "\n" || e.args === "\r" || illegal_chars.has(e.args)) {
                e.preventDefault();
                e.stopPropagation();
            }
        }

        if(illegal_chars.has(e.args)) {
            e.preventDefault();
            e.stopPropagation();
        }
    }
})

document.getElementById('editor-container').style.fontSize='20px';
console.log("In text-editor")
