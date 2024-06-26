const ws = new WebSocket("ws://localhost:23335/ws");

ws.onopen = function(event) {
    console.log("WebSocket is open now.");
};

ws.onclose = function(event) {
    console.log("WebSocket is closed now.");
};

ws.onerror = function(event) {
    console.error("WebSocket error observed:", event);
};

ws.onmessage = function(event) {
    console.log("Called");
    const chatBox = document.getElementById('chatBox');
    const data = JSON.parse(event.data);
    const chatlog = data["chatlog"];
    chatBox.innerHTML = `<p>${parseMessage(chatlog)}</p>`;
    
    // Use setTimeout to ensure the DOM is updated before scrolling
    setTimeout(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
        console.log("Scrolled");
    }, 30);
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

function parseMessage(chatlog) {
    let parsedChat = '';
    chatlog.forEach(function(message) {
        if (message["role"]=='system') {
            parsedChat += `<div class="chat-box left-aligned">
                ${message["message"]}
            </div>`;
        } else {
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
