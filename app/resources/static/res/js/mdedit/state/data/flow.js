import {_store, progress_history, traversing} from './history.js';
import {UpdateHistobar} from "../../ui/actions.js";
import {config} from '../../state.js'

export function history_change(){
    UpdateHistobar(_store.history.length);
}


let auto_save_id = null;
function _autosave(save_id){
    if (!traversing()){
        progress_history()
    }
    save_id = null
}
export function queue_autosave(){
    if (auto_save_id !== null) clearTimeout(auto_save_id);

    auto_save_id = setTimeout(_autosave.bind(), config.history.autosave_interval * 1000, auto_save_id)
}
