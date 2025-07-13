export * as style from './text/style.js'

import {clear as clear_op} from './text/op.js'
import {editor} from "./ui.js";

export const clear = function(){
    clear_op(editor.textarea)
}
