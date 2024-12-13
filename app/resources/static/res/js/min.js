//Basic UI Helpers

//Hamburger Menu in Navbar
document.addEventListener('DOMContentLoaded', () => {
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
        el.addEventListener('click', () => {

            // Get the target from the "data-target" attribute
            const target = el.dataset.target;
            const $target = document.getElementById(target);

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');

        });
    });

    //Start text ticker
    let elements = document.getElementsByClassName('txt-flip');
    start_ticker(elements)
});



// Messing with animations
const TxtFlip = function (el, content, period) {
    this.content = content;
    this.el = el;
    this.loopNum = 0;
    this.period = parseInt(period, 10) || 2000;
    this.txt = '';
    this.tick();
    this.isDeleting = false;

    this.writeSpeed = 100    // Increases base speed
    this.newWordPause = 300  // Pause length at start of each word
    this.randomBias = 50     // Strength of speed irregularity for realism
    this.deletionBias = 1.4

    this.skipPrefix = false;
};

TxtFlip.prototype.tick = function() {
    //Text index
    const i = this.loopNum % this.content.length;
    const next = (i + 1) % this.content.length;

    //Text at index
    const prefix = this.content[i].pre;
    const preText = prefix + ' '

    const text = this.content[i].text;
    const fullTxt = preText + text

    if (this.isDeleting) {  // Deleting text
        this.txt = fullTxt.substring(0, this.txt.length - 1);
    } else {                // Writing Text
        this.txt = fullTxt.substring(0, this.txt.length + 1);
    }

    // Update text box
    this.el.innerHTML = '<span class="wrap">'+this.txt+'</span>';

    const that = this;
    let delta = this.writeSpeed - (Math.random() * this.randomBias)

    // If deleting, halve the delta
    if (this.isDeleting) { delta /= this.deletionBias; }

    // If not deleting, but all text is writen
    if (!this.isDeleting && this.txt === fullTxt) { // End of string
        this.skipPrefix = this.content[next].pre === prefix;

        delta = this.period;
        this.isDeleting = true;

    } else if (this.isDeleting) {
        const finished = (
            this.skipPrefix ? this.txt === preText : this.txt === '')

        if (finished) {
            this.isDeleting = false;
            this.loopNum++;
            delta = this.newWordPause;
        }
    }

    setTimeout(function() {
        that.tick();
    }, delta);
};

start_ticker = function(elements) {
    for (let i=0; i<elements.length; i++) {
        const content= elements[i].getAttribute('data-content');
        const period = elements[i].getAttribute('data-period');
        if (content) {
            new TxtFlip(elements[i], JSON.parse(content), period);
        }
    }
}

