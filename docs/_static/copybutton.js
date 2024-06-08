document.addEventListener("DOMContentLoaded", function() {
    function addCopyButtons(clipboard) {
        const codeBlocks = document.querySelectorAll('div.highlight pre');
        codeBlocks.forEach(function(codeBlock) {
            const button = document.createElement('button');
            button.className = 'copy-button';
            button.type = 'button';
            button.innerText = 'Copy';

            button.addEventListener('click', function() {
                clipboard.writeText(codeBlock.innerText).then(function() {
                    button.blur();
                    button.innerText = 'Copied!';
                    setTimeout(function() {
                        button.innerText = 'Copy';
                    }, 2000);
                }, function(error) {
                    button.innerText = 'Error';
                });
            });

            const pre = codeBlock.parentNode;
            pre.parentNode.insertBefore(button, pre);
        });
    }

    if (navigator && navigator.clipboard) {
        addCopyButtons(navigator.clipboard);
    } else {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.6/clipboard.min.js';
        script.integrity = 'sha384-Ot5FZC7Ep5Vh1d9zN1hC2n0D6b0Q1U4J6+w7QyFvS3z5V1Z1In/F8bywS5G7Q4q9';
        script.crossOrigin = 'anonymous';
        script.onload = function() {
            const clipboard = new ClipboardJS('.copy-button', {
                target: function(trigger) {
                    return trigger.nextElementSibling;
                }
            });
            addCopyButtons(clipboard);
        };
        document.body.appendChild(script);
    }
});