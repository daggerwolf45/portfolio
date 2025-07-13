import {init as start_ui} from '../ui.js'
import {register as register_keybinds} from "../input.js";

export default function(){
    start_ui()
    register_keybinds()
}

