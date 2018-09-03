//jquery need to be load after document been loaded
//$ = require("jquery")
window.$ = require("jquery")

$(document).ready( () => {

    class chat_control {
        constructor() {
            this.msg_list = $('.msg-group');
        }

        send_msg(name, msg) {
            this.msg_list.append(this.get_msg_html(name, msg, 'right'));
            this.scroll_to_bottom(); 
        }

        receive_msg(name, msg) {
            this.msg_list.append(this.get_msg_html(name, msg, 'left'));
            this.scroll_to_bottom(); 
        }

        get_msg_html(name, msg, side) {
            var msg_temple = `
                <div class="card">
                     <div class="card-body">
                         <h6 class="card-subtitle mb-2 text-muted text-${side}">${name}</h6>
                         <p class="card-text float-${side}">${msg}</p>
                     </div>
                </div>
                `;
            return msg_temple;
        }

        scroll_to_bottom() {
            this.msg_list.scrollTop(this.msg_list[0].scrollHeight);
        }
    }


    var chat = new chat_control();
    chat.receive_msg('yingshaoxo', 'This was made for you! \`2017/(520*1314)\`');

    send_button = $('button') // get jquery element from html table name
    input_box = $('#input-box') // get jquery element from div id
    // also you could get it by $('.form-control') or $('textarea')

    function handle_msg(msg) {
        msg = msg.trim()
        msg = msg.replace(/(?:\r\n|\r|\n)/g, '<br>')
        return msg
    }

    function send_msg() {
        msg = handle_msg(input_box.val());
        if (msg != '') {
            chat.send_msg('you', msg);
            input_box.val('');

            setTimeout(function(){ chat.receive_msg('yingshaoxo', 'I can hear you.'); }, 1000);
            MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
        }
    }

    function box_key_pressing(event) {
        // control + enter was pressed
        if ((event.keyCode === 10 || event.keyCode === 13) && event.ctrlKey) {
            send_msg();
        }
        // esc was pressed
        if (event.keyCode === 27) {
            input_box.blur();
        }
    }

    send_button.on('click', send_msg.bind());
    input_box.on('keyup', box_key_pressing.bind());

})
