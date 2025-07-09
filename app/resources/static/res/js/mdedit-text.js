const textarea = document.getElementById('editor_textarea');

let tab_size = 4;
let history_len = 1000;

const history = [];
let undo = [];

const _ProgessHistory = function (clear_undo = false) {
    if (history.length > 0) {
        if (history.at(-1) === textarea.value) {
            return;
        }
    }

    if(history.length > history_len) {
        history.shift();
    }

    history.push(textarea.value);
    console.log('Added to history');

    update_histobar(history.length);
    document.getElementById('btn_undo').disabled = false;

    if (clear_undo) {
        undo = []
    }
}

const update_histobar = function (val) {
    const histobar = document.getElementById('histo_progress');

    histobar.value = val;
    histobar.classList = [];
    if (val < 25) {
        histobar.setAttribute('max', '30');
        histobar.classList.add('progress');
    } else if (val < 45) {
        histobar.setAttribute('max', '50');
        histobar.classList.add('progress', 'is-info');
    } else if (val < 95) {
        histobar.setAttribute('max', '100');
        histobar.classList.add('progress', 'is-link');
    } else if (val < 190) {
        histobar.setAttribute('max', '200');
        histobar.classList.add('progress', 'is-success');
    } else if (val < 490) {
        histobar.setAttribute('max', '500');
        histobar.classList.add('progress', 'is-warning');
    } else {
        histobar.setAttribute('max', '1000');
        histobar.classList.add('progress', 'is-danger');
    }
}

const fUndo = function(){
    if (history.length > 0) {
        const cursor_pos = textarea.selectionStart;

        undo.push(textarea.value)
        textarea.value = history.pop()
        console.log('Backtracked history');

        document.getElementById('btn_redo').disabled = false;

        textarea.selectionStart =
        textarea.selectionEnd = cursor_pos;
    } else {
        document.getElementById('btn_undo').disabled = true;
    }
}

const fRedo = function(e){
    if (undo.length > 0) {
        const cursor_pos = textarea.selectionStart;

        history.push(textarea.value)
        textarea.value = undo.pop()
        console.log('Undid my backtrack');

        textarea.selectionStart =
            textarea.selectionEnd = cursor_pos;
    } else {
        document.getElementById('btn_redo').disabled = true;
    }
}

const _wrap = function(field, open, close){
    const text = field.value;
    const start = field.selectionStart;
    const end = field.selectionEnd;

    const dist = end - start;
    const change_len = open.length + close.length;

    _ProgessHistory(true)

    field.value =
        text.substring(0, start) +
            open +
            text.substring(start, start+dist) +
            close +
        text.substring(end);

    textarea.selectionStart =
        textarea.selectionEnd = start + dist + change_len;
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

    _ProgessHistory()

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
            case 'z':
                e.preventDefault();
                fUndo()
                break;
            case 'y':
                e.preventDefault();
                fRedo()
                break;
            case 'b':
                e.preventDefault();
                fBold()
                break;
            case 'i':
                e.preventDefault();
                fItalic()
                break;
            case 'Enter':
                ReloadMarkdown().then()
                break;
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
        }
    }
})

textarea.addEventListener('change', (e) => {
    _ProgessHistory(true)
})

textarea.addEventListener('click', (e) => {
    _ProgessHistory()
})
textarea.addEventListener('focusout', (e) => {
    e.preventDefault();
})

document.getElementById('editor').addEventListener('click', (e) => {
    textarea.focus();
})


document.getElementById("btn_bold").addEventListener('click', fBold)
document.getElementById("btn_italic").addEventListener('click', fItalic)


document.getElementById("btn_undo").addEventListener('click', fUndo)
document.addEventListener('DOMContentLoaded', function() {
    _ProgessHistory()
})
document.getElementById("btn_redo").addEventListener('click', fRedo)

document.getElementById("btn_clear").addEventListener('click', () => {
    _ProgessHistory()
    textarea.value = ''
    _ProgessHistory()
})
