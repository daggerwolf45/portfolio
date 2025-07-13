import {init as start_ui, editor} from '../ui.js'
import {register as register_keybinds} from "../input.js";
import {draft} from './data.js'

export default function(){
    start_ui()
    register_keybinds()

    // Save draft when editor updates
    editor.textarea.addEventListener('change', draft.save)
}

