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
    //console.log("Called");
    const data = JSON.parse(event.data);

    if (data.type === "message") {
        handleChatMessage(data);
    } else if (data.type === "question") {
        handleQuestionResponse(data);
    } else if (data.type === "explanation") {
        handleExplanationResponse(data);
    }
};

function handleChatMessage(data) {
    const chatBox = document.getElementById('chatBoxInner');
    const chatlog = data["chatlog"];
    chatBox.innerHTML = `<p>${parseMessage(chatlog)}</p>`;

    // Use setTimeout to ensure the DOM is updated before scrolling
    setTimeout(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
        //console.log("Scrolled");
    }, 30);
}

function handleQuestionResponse(data) {
    const questionBox = document.getElementById('questionBoxInner');
    const answer = data["answer"];
    questionBox.innerHTML = `<p class="readable-text">${(answer)}</p>`;
}

function handleExplanationResponse(data) {
    const explanationBox = document.getElementById('explanationBoxInner');
    const explanation = data["explanation"];
    explanationBox.innerHTML = `<p class="readable-text">${(explanation)}</p>`;
}


function sendMessageWrapper(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    showLoadingSpinner();
    sendMessage(); // Call the sendMessage function
}

function sendMessage() {
    if (ws.readyState === WebSocket.OPEN) {
        const inputField = document.getElementById('inputField');
        const messageData = {
            type: 'message',
            content: inputField.value
        };
        ws.send(JSON.stringify(messageData));
        inputField.value = ''; // Clear input field after sending

        // Simulate the response delay for demonstration purposes
        setTimeout(() => hideLoadingSpinner('loadingSpinner'), 2000);
    } else {
        console.error("WebSocket is not open.");
        hideLoadingSpinner('loadingSpinner');
        // Optionally try to reconnect or inform the user
    }
}

function submitQuestionWrapper(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    showLoadingSpinner('questionLoadingSpinner');
    submitQuestion(); // Call the submitQuestion function
}

function submitQuestion() {
    if (ws.readyState === WebSocket.OPEN) {
        const questionField = document.getElementById('questionField');
        const questionData = {
            type: 'question',
            content: questionField.value
        };
        ws.send(JSON.stringify(questionData));
        questionField.value = ''; // Clear input field after sending

        // Simulate the response delay for demonstration purposes
        setTimeout(() => hideLoadingSpinner('questionLoadingSpinner'), 2000);
    } else {
        console.error("WebSocket is not open.");
        hideLoadingSpinner('questionLoadingSpinner');
        // Optionally try to reconnect or inform the user
    }
}

function showLoadingSpinner() {
    const spinner = document.getElementById('loadingSpinner');
    spinner.style.display = 'inline-block';
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('loadingSpinner');
    spinner.style.display = 'none';
}

function parseMessage(chatlog) {
    let parsedChat = '';
    chatlog.forEach(function(message, index) {
        let roleClass = message["role"] === 'system' ? 'left-aligned' : 'right-aligned';
        parsedChat += `<div class="chat-box ${roleClass}" data-role="${message["role"]}" data-message="${message["message"]}">
            ${message["message"]}
        </div>`;
    });
    return parsedChat;
}

function parseMessage(chatlog) {
    let parsedChat = '';
    chatlog.forEach(function(message, index) {
        console.log(message);
        let roleClass = message["role"] === 'system' ? 'left-aligned' : 'right-aligned';
        parsedChat += `<div class="chat-box ${roleClass}" data-role="${message["role"]}" data-message="${message["message"]}" data-index="${index}" onclick="handleMessageClick(event)">
            ${message["message"]}
        </div>`;
    });
    return parsedChat;
}

// Function to handle message click
function handleMessageClick(event) {
    const chatBox = event.currentTarget;
    const role = chatBox.getAttribute('data-role');
    const message = chatBox.getAttribute('data-message');
    const messageData = {
        type: 'explain',
        content: { role, message }
    };

    if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(messageData));
    } else {
        console.error("WebSocket is not open.");
        // Optionally try to reconnect or inform the user
    }
}

async function resetChat() {
    try {
        const response = await fetch('/reset-chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            window.location.href = '/';
        } else {
            alert('Failed to reset chat');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while resetting the chat');
    }
}


window.onload = function() {
    var chatBox = document.getElementById("chatBoxInner");
    chatBox.scrollTop = chatBox.scrollHeight;
};


const chatBox = document.getElementById('chatBoxInner');

chatBox.innerHTML = `<p>${parseMessage(chatlog["log"])}</p>`;
