import * as ui from './ui.js'
import {style} from './text.js'
import {history} from './state.js'

export const register = function () {
    ui.editor.textarea.addEventListener('keydown', handle_keydown)
}



let last_key = null
const handle_keydown = function(e) {
    last_key = e.key
    history.queue_autosave()

    // Modifier functions
    if (e.ctrlKey) {
        console.log(e.key)
        switch (e.key){
            case 'z':
                if (!e.shiftKey) {
                    e.preventDefault();
                    history.undo_change()
                    break;
                } // Fallthrough to Ctrl-Y if shift is held
            case 'y':
                e.preventDefault();
                history.restore_history()
                break;
            case 'b':
                e.preventDefault();
                style.fBold()
                break;
            case 'i':
                e.preventDefault();
                style.fItalic()
                break;
            case 'Enter':
                history.progress_history()
                ui.preview.reload().then()
                break;
        }
    } else {
        switch (e.key) {
            case 'Tab':
                e.preventDefault();
                style.fTabnate()
                break;
            case 'Escape':
                ui.editor.textarea.blur()
                break;
            case 'Enter':
                if (last_key !== 'Enter') {
                    history.progress_history()
                }
        }
    }
}
