const roomName = "{{ other_user.id }}";  // Or use combined ids for uniqueness
const username = "{{ request.user.username }}";

const chatSocket = new WebSocket(
  'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div><strong>${data.username}:</strong> ${data.message}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
};

chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

document.getElementById("chat-form").onsubmit = function(e) {
  e.preventDefault();
  const messageInput = document.getElementById("chat-message-input");
  const message = messageInput.value;

  chatSocket.send(JSON.stringify({
    message: message,
    username: username
  }));

  messageInput.value = "";
};
