const textarea = document.getElementById('editor_textarea');
const previewFrame = document.getElementById('preview_frame');

import('/static/res/js/mdedit-text.js');

document.addEventListener('DOMContentLoaded', () => {
    const starting_data = localStorage.getItem('draft-text');
    if (starting_data !== null){
        textarea.value = starting_data;
    }
})

textarea.addEventListener('change', async function() {
    localStorage.setItem('draft-text', textarea.value);
})


const ReloadMarkdown = async function () {
    const resp = await fetch('/admin/view/isoblog', {
        method: 'POST',
        body: textarea.value
    });

    if (resp.ok) {
        previewFrame.contentWindow.document.open();
        previewFrame.contentWindow.document.write(await resp.text());
        previewFrame.contentWindow.document.close();
    }
}
