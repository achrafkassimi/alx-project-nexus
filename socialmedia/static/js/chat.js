const otherUserId = "{{ other_user.id }}";
const username = "{{ request.user.username }}";
const chatBox = document.getElementById("chat-box");

// إنشاء WebSocket للغرفة (يمكن تعديل المفتاح حسب تصميمك)
const chatSocket = new WebSocket(
  'ws://' + window.location.host + '/ws/chat/' + otherUserId + '/'
);

// استقبال الرسائل عبر WebSocket وعرضها
chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div><strong>${data.username}:</strong> ${data.message}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
};

chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

// جلب الرسائل من GraphQL عند تحميل الصفحة
function fetchMessages() {
  fetch('/graphql/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // لو كتستخدم JWT علق السطر تحت و فعله مع تخزين التوكن
      // 'Authorization': 'JWT ' + localStorage.getItem('token'),
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify({
      query: `
        query {
          messages(otherUserId: ${otherUserId}) {
            id
            content
            sender {
              username
            }
            timestamp
          }
        }
      `
    }),
  })
  .then(res => res.json())
  .then(res => {
    chatBox.innerHTML = '';
    res.data.messages.forEach(msg => {
      chatBox.innerHTML += `<div><strong>${msg.sender.username}:</strong> ${msg.content}</div>`;
    });
    chatBox.scrollTop = chatBox.scrollHeight;
  });
}

fetchMessages();

// إرسال رسالة عبر GraphQL mutation ثم WebSocket
document.getElementById("chat-form").onsubmit = function(e) {
  e.preventDefault();
  const messageInput = document.getElementById("chat-message-input");
  const message = messageInput.value.trim();
  if (!message) return;

  fetch('/graphql/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // لو كتستخدم JWT علق السطر تحت و فعله مع تخزين التوكن
      // 'Authorization': 'JWT ' + localStorage.getItem('token'),
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify({
      query: `
        mutation {
          sendMessage(receiverId: ${otherUserId}, content: "${message.replace(/"/g, '\\"')}") {
            message {
              id
              content
              sender {
                username
              }
            }
          }
        }
      `
    }),
  })
  .then(res => res.json())
  .then(() => {
    chatSocket.send(JSON.stringify({
      message: message,
      username: username
    }));
    messageInput.value = "";
  })
  .catch(err => console.error('Error sending message:', err));
};

function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="))
    .split("=")[1];
}
