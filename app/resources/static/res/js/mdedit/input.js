import * as ui from './ui.js'
import {style} from './text.js'
import {history} from './state.js'

export const register = function () {
    ui.editor.textarea.addEventListener('keydown', handle_keydown)
}

const handle_keydown = function(e) {
    // Modifier functions
    if (e.ctrlKey) {
        console.log(e.key)
        switch (e.key){
            case 'z':
                e.preventDefault();
                history.undo_change()
                break;
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
        }
    }
}
