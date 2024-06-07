
const ws = new WebSocket("ws://localhost:23335/ws");


ws.onmessage = function(event) {
    const chatBox = document.getElementById('chatBox');
    const data = JSON.parse(event.data);
    const chatlog = data["chatlog"];
    chatBox.innerHTML = `<p>${parseMessage(chatlog)}</p>`;
};

function sendMessage() {
    if (ws.readyState === WebSocket.OPEN) {
        const inputField = document.getElementById('inputField');
        ws.send(inputField.value);
        inputField.value = ''; // Clear input field after sending
    } else {
        console.error("WebSocket is not open.");
        // Optionally try to reconnect or inform the user
    }
}

function  parseMessage(chatlog) {

    parsedChat = '';
    chatlog.forEach(function(message) {
        
        if (message["is_bot"]) {

            parsedChat += `<div class="chat-box left-aligned">
                    ${message["message"]}
                    </div>`;

        }  else {

            parsedChat += `<div class="chat-box right-aligned">
                ${message["message"]}
                </div>`;

        }
       
    });

    return parsedChat;


}

window.onload = function() {
    var chatBox = document.getElementById("chatBox");
    chatBox.scrollTop = chatBox.scrollHeight;
};

const chatBox = document.getElementById('chatBox');

chatBox.innerHTML = `<p>${parseMessage(chatlog["log"])}</p>`;
