var editor = ace.edit("editor-container");
editor.setOptions({
    useWrapMode: true
})
editor.getSession().setUseWrapMode(true)

document.getElementById('editor-container').style.fontSize='20px';
console.log("In text-editor")