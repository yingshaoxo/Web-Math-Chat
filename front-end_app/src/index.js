import './styles.scss';

import $ from "jquery";
import popper from "popper.js";
import bootstrap from "bootstrap";

const Cookies = require('js-cookie')
const io = require('socket.io-client');


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

    no_script(html_code) {
        return html_code.replace("<script>", "&lt;script&gt;").replace("</script>", "&lt;&#47;script&gt;")
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
        return this.no_script(msg_temple);
    }

    scroll_to_bottom() {
        this.msg_list.scrollTop(this.msg_list[0].scrollHeight);
    }
}


let username = Cookies.get('username') 
$("#save-name").on('click', (() => {
    Cookies.set("username", $("#name-box").val().trim(), { expires: 30 })
    $("#myModal").modal("hide")
    username = Cookies.get('username') 
}).bind());


var chat = new chat_control();


let socket = io(location.protocol + '//' + document.domain + ':' + location.port);

socket.on('connect', function() {
    socket.emit('you have total control about this text for identifying tunnel name', {data: 'I\'m connected!'});
});

socket.on('you have total control about this text for identifying tunnel name', (data) => {
    console.log(data)
    const json_obj = JSON.parse(data)
    if (json_obj.length != 0) {
        $('.card').remove()
    }
    json_obj.forEach((msg) => {
        if (username == undefined) {
            chat.receive_msg(msg.username, msg.text)
        } else {
            if (msg.username == username) {
                chat.send_msg('you', msg.text)
            }
            else {
                chat.receive_msg(msg.username, msg.text)
            }
        }
    })
})


chat.receive_msg('yingshaoxo', 'This was made for you! \`2018/(520*1314)\`');

const send_button = $('#send-button') // get jquery element from html table name
const input_box = $('#input-box') // get jquery element from div id

const inputField = input_box.get(0) 
const sendField = send_button.get(0)
const input_box_css = inputField.style.cssText
const send_button_css = sendField.style.cssText
function auto_growing() {
    if (inputField.scrollHeight > inputField.clientHeight) {
        inputField.style.height = inputField.scrollHeight + "px";
        sendField.style.height = inputField.style.height
    } else {
        inputField.style.cssText = "height:auto; bottom:0"
        //sendField.style.cssText = 'height:auto; bottom:0';
    }
    if (input_box.val() == "") {
        inputField.style.cssText = input_box_css;
        sendField.style.cssText = send_button_css;
    }
}

function handle_msg(msg) {
    msg = msg.trim()
    msg = msg.replace(/(?:\r\n|\r|\n)/g, '<br>')
    return msg
}

function send_msg() {
    let msg = handle_msg(input_box.val());
    if (username == undefined) {
        $("#myModal").modal("show")
    }
    else {
        if (msg != '') {
            let msg_dict = {'username': username, 'text': msg}
            socket.emit('message_receiver_on_server', JSON.stringify(msg_dict));

            chat.send_msg('you', msg);
            input_box.val('');

            MathJax.Hub.Queue(["Typeset",MathJax.Hub]);

            auto_growing();
        }
    }
}

$.fn.selectRange = function(start, end) {
    if(end === undefined) {
        end = start;
    }
    return this.each(function() {
        if('selectionStart' in this) {
            this.selectionStart = start;
            this.selectionEnd = end;
        } else if(this.setSelectionRange) {
            this.setSelectionRange(start, end);
        } else if(this.createTextRange) {
            var range = this.createTextRange();
            range.collapse(true);
            range.moveEnd('character', end);
            range.moveStart('character', start);
            range.select();
        }
    });
};

function box_key_pressing(event) { 
    // auto growing
    auto_growing();

    // control + m was pressed
    if ((event.keyCode === 10 || event.keyCode === 77) && event.ctrlKey) {
        input_box.val(String.raw`
$$
\begin{align*}

\end{align*}
$$
        `.trim());
        input_box.focus();
        input_box.selectRange(18);
    }
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


socket.on('message_receiver_on_client', (data) => {
    console.log(data)
    const json_obj = JSON.parse(data)
    chat.receive_msg(json_obj.username, json_obj.text);
    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
})
