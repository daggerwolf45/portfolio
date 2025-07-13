export {editor} from './ui/elements.js'

import {preview as preview_element} from './ui/elements.js'
import * as action from "./ui/actions.js";


export const preview = Object.assign(
    preview_element,
    {
        reload: action.ReloadPreview
    }
)
export const init = function (){
    action.register_buttons()
}




