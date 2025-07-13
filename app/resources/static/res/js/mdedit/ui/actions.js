import {style, clear} from '../text.js'
import {preview, editor} from "./elements.js";
import {history} from '../state.js'

export const register_buttons = function() {
    register_toolbar()
    preview.block.querySelector('#btn_reload_preview').addEventListener('click', ReloadPreview)
}

const register_toolbar = function() {
    // Basic Styles
    document.getElementById("btn_bold").addEventListener('click', style.fBold)
    document.getElementById("btn_italic").addEventListener('click', style.fItalic)

    // Style Menu
    document.getElementById("style_sel_code").addEventListener('click', style.fMono)
    document.getElementById('style_sel_gay').addEventListener('click', style.fGay)

    // Features
    document.getElementById('btn_quote').addEventListener('click', style.fQuote)

    // History
    document.getElementById("btn_undo").addEventListener('click', history.undo_change)
    document.getElementById("btn_redo").addEventListener('click', history.restore_history)

    // File
    document.getElementById("btn_clear").addEventListener('click', clear)
}


export const ReloadPreview = async function(){
    const frame = preview.frame;

    const resp = await fetch('/admin/view/isoblog', {
        method: 'POST',
        body: editor.textarea.value
    });

    if (resp.ok) {
        frame.contentWindow.document.open();
        frame.contentWindow.document.write(await resp.text());
        frame.contentWindow.document.close();
    }
}
