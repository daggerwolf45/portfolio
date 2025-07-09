const editor_textarea = document.getElementById('editor_textarea');
const previewFrame = document.getElementById('preview_frame');

document.addEventListener('readystatechange', () => {
    const starting_data = localStorage.getItem('draft-text');
    if (starting_data !== null){
        editor_textarea.value = starting_data;
    }
})

editor_textarea.addEventListener('change', async function() {
    localStorage.setItem('draft-text', editor_textarea.value);
})


const ReloadMarkdown = async function () {
    const resp = await fetch('/admin/view/isoblog', {
        method: 'POST',
        body: editor_textarea.value
    });

    if (resp.ok) {
        previewFrame.contentWindow.document.open();
        previewFrame.contentWindow.document.write(await resp.text());
        previewFrame.contentWindow.document.close();
    }
}
