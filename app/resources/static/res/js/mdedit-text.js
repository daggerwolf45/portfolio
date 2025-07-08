let tab_size = 4;
let history_len = 1000;

const history = [];
let undo = [];

const fUndo = function(e){
    if (history.length > 1) {
        textarea.value = history.pop()
        undo.push(textarea.value)
    }
}

const fRedo = function(e){
    if (undo.length > 1) {
        textarea.value = undo.pop()
    }
}

const _wrap = function(field, open, close){
    const text = field.value;
    const start = field.selectionStart;
    const end = field.selectionEnd;

    const dist = end - start;

    field.value =
        text.substring(0, start) +
            open +
            text.substring(start, start+dist) +
            close +
        text.substring(end);
}

const wrap = function(field, val){
    return _wrap(field, val, val);
}

const wrapTag = function(field, val){
    const open = `<${val}>`
    const close = `</${val}>`

    return _wrap(field, open, close);
}

const fBold = function(e){
    wrap(textarea, '**');
}

const fItalic = function(e){
    wrap(textarea, '*');
}

const fMono = function(e){
    wrapTag(textarea, 'code');
}

const fTabnate = function(e){
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;

    const tab = " ".repeat(tab_size);

    textarea.value =
        text.substring(0, start) +
        tab +
        text.substring(end);

    textarea.selectionStart =
        textarea.selectionEnd = start + tab_size;
}

textarea.addEventListener('keydown', (e) => {
    // Modifier functions
    if (e.ctrlKey) {
        console.log(e.key)
        switch (e.key){
            case 'KeyZ':
                fUndo(e)
                break;
            case 'KeyY':
                fRedo(e)
                break;
            case 'b':
                e.preventDefault();
                fBold(e)
                break;
            case 'i':
                e.preventDefault();
                fItalic(e)
                break;
            case 'Enter':
                ReloadMarkdown().then()
                break;
            default:
                undo = []
        }
    } else {
        switch (e.key) {
            case 'Tab':
                e.preventDefault();
                fTabnate(e)
                break;
            case 'Escape':
                textarea.blur()
                break;
            default:
                undo = []
        }
    }
})

textarea.addEventListener('onchange', (e) => {
    if(history.length > history_len) {
        history.shift();
    }

    history.push(textarea.value);
})
