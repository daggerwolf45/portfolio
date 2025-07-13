export * as history from './data/history.js'

import {editor} from '../ui.js'


const save_state_to_browser = function(){
    localStorage.setItem('draft-text', editor.textarea.value)
}

export const draft = {
    save: save_state_to_browser
}

