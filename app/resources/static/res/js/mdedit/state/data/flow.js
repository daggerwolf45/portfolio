import {_store} from './history.js';
import {UpdateHistobar} from "../../ui/actions.js";

export function history_change(){
    UpdateHistobar(_store.history.length);
}
