import {editor} from '../ui.js'
import * as op from './op.js'
import {config} from '../state.js'
const textarea = editor.textarea


export const fBold = function(e){
    op.wrap(textarea, '**');
}

export const fItalic = function(e){
    op.wrap(textarea, '*');
}

export const fMono = function(e){
    op.wrapTag(textarea, 'code');
}

export const fGay= function(e){
    op.wrapTag(textarea, 'gay');
}

export const fQuote = function(e){
    op.appendToLineStart(textarea, '>');
}

export const fTabnate = function(e){
    const tab = " ".repeat(config.text.tab.len);
    op.insertAtCursor(textarea, tab);
}
