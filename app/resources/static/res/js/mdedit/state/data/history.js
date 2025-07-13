import {config as conf} from '../../state.js'
import {editor} from '../../ui.js'

const _history = []
let _undo = []


export function push (update){
    // Not empty
    if (_history.length > 0) {
        // Don't commit identical history
        if (_history.at(-1) === update) {
            return;
        }
    }

    // Pop start if history is 'full'
    if(_history.length > conf.history.size) {
       _history.shift();
    }

    _history.push(update);
}
export function pop () {
    if (_history.length > 0) {
        return _history.pop();
    } else return '';
}


// Take step forwards
export function progress_history() {
    _undo = [];

    push(editor.textarea.value);
}

// Undo
export function undo_change() {
    _undo.push(editor.textarea.value);

    editor.textarea.value = pop();
}

// Redo
export function restore_history() {
    // Push current to history
    push(editor.textarea.value);
    // pop undo as new
    if (_undo.length > 0) {
        editor.textarea.value = _undo.pop();
    }
}


export const _store = {
    history: _history,
    undo: _undo,
}
