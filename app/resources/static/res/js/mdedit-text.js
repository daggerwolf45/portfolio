let tab_size = 4;
let history_len = 1000;

const history = [];
let undo = [];

textarea.addEventListener('keydown', (e) => {
    switch (e.key){
        case 'Tab':
            e.preventDefault();
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
            break;
        case 'KeyZ':
            if (e.ctrlKey) {
                if (history.length > 1) {
                    textarea.value = history.pop()
                    undo.push(textarea.value)
                }
            }
            break;
        case 'KeyY':
            if (e.ctrlKey) {
                if (undo.length > 1) {
                    textarea.value = undo.pop()
                }
            }
            break;
        default:
            undo = []
    }
})

textarea.addEventListener('onchange', (e) => {
    if(history.length > history_len) {
        history.shift();
    }

    history.push(textarea.value);
})
