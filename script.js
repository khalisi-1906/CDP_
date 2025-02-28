const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const loadingIndicator = document.getElementById('loading');


sendButton.addEventListener('click', () => {
    const question = userInput.value.trim();
    if (question) {
        addMessageToChat('user', question);
        sendQuestionToBackend(question);
        userInput.value = '';
    }
});

function addMessageToChat(sender, message, sources = null) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = message;

    if (sources && sources.length > 0) {
        const sourceDiv = document.createElement('div');
        sourceDiv.classList.add('source');
        sources.forEach((source) => {
            const link = document.createElement('a');
            link.href = source.url;
            link.textContent = `[Source]`;
            link.target = "_blank";
            sourceDiv.appendChild(link);
        });
        messageDiv.appendChild(sourceDiv);
    }
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}


function sendQuestionToBackend(question) {
     loadingIndicator.classList.add('show');

    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question }),
    })
        .then((response) => {
             loadingIndicator.classList.remove('show');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
             console.log(data);
             if (data && data.answers) {
                const answers = data.answers;
                let message = "";
                let sources = [];
                for (let i = 0; i < answers.length; i++) {
                    message += answers[i] + "\n\n";
                 // Source extraction would need to be more complex with the string returned.
                 // sources.push({"url":answers[i].url});
                }
                 addMessageToChat('bot', message, sources);

            } else if(data && data.message){
                  addMessageToChat('bot', data.message);
            } else{
                  addMessageToChat('bot', "Unexpected response from the server")
            }

        })
        .catch((error) => {
          loadingIndicator.classList.remove('show');
            addMessageToChat('bot', `Error communicating with server: ${error.message}`);
             console.error('Error:', error);
        });
}