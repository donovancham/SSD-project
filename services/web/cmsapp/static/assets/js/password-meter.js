'use strict';

class PasswordMeter {
    constructor(selector) {
        this.wrappers = document.querySelectorAll(selector);
        if(this.wrappers.length > 0) {
            this.init(this.wrappers);
        }
    }
    init(wrappers) {
        wrappers.forEach(wrapper => {
            let bar = wrapper.querySelector('.password-meter-bar');
            let input = wrapper.previousElementSibling;

            input.addEventListener('keyup', () => {
                let value = input.value;
                bar.classList.remove('level0', 'level1', 'level2', 'level3', 'level4');
                let result = zxcvbn(value);
                let cls = `level${result.score}`;
                bar.classList.add(cls);
            }, false);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const passwordMeter = new PasswordMeter('.password-meter-wrap');
}, false);