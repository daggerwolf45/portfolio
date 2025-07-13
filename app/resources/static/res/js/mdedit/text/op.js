import {editor} from "../ui.js";
import {history} from '../state.js'

const _wrap = function(field, open, close){
    const text = field.value;
    const start = field.selectionStart;
    const end = field.selectionEnd;

    const dist = end - start;

    history.progress_history()

    field.value =
        text.substring(0, start) +
        open +
        text.substring(start, start+dist) +
        close +
        text.substring(end);

    field.selectionStart =
    field.selectionEnd = start + dist + open.length;
}

export const wrap = function(field, val){
    return _wrap(field, val, val);
}

export const wrapTag = function(field, val){
    const open = `<${val}>`
    const close = `</${val}>`

    return _wrap(field, open, close);
}

export const appendToLineStart = function(field, val){
    const text = field.value.toString();
    const start = field.selectionStart;
    const end = field.selectionEnd;

    const delimiter_code = 10 // /n newline

    let pos = start
    while (pos >= 0) {
        if (text.charCodeAt(pos) === delimiter_code) {
            break;
        } else {
            pos = pos - 1;
        }
    }

    field.value = [
        text.substring(0, pos),
        '\n> ',
        text.substring(pos + 1),
    ].join('');
}

export const insertAtCursor = function(field, val){
    const start = field.selectionStart;
    const end = field.selectionEnd;
    const text = field.value;

    history.progress_history()

    field.value =
        text.substring(0, start) +
        val +
        text.substring(end);

    field.selectionStart =
    field.selectionEnd = start + val.length;
}

export const clear = function(field){
    history.progress_history()
    field.value = ''
    history.progress_history()
}
