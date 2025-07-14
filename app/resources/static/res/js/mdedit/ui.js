export {editor} from './ui/elements.js'

import {preview as preview_element, editor} from './ui/elements.js'
import * as action from "./ui/actions.js";
import {history} from "./state.js"


export const preview = Object.assign(
    preview_element,
    {
        reload: action.ReloadPreview
    }
)

export const init = function (){
    document.addEventListener('DOMContentLoaded', function() {
        history.progress_history()
    })

    document.addEventListener('readystatechange', () => {
        const starting_data = localStorage.getItem('draft-text');
        if (starting_data !== null){
            editor.textarea.value = starting_data;
        }
    })

    action.register_buttons()
}




