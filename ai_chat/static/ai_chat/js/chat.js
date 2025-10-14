async function loadChat() {
  const response = await fetch('/chat');
  if (!response.ok) {
    console.error('Failed to load chat:', response.statusText);
    return;
  }
  const data = await response.text();
  document.getElementById('chat').innerHTML = data;
}
await loadChat();

const form = document.getElementById('chat-form');
form.addEventListener('submit', handleSumbit);
scrollToBottom();

const clearForm = document.getElementById('clear-form');
if (clearForm) {
  clearForm.addEventListener('submit', handleClear);
}

async function handleSumbit(event) {
  event.preventDefault();

  const form = event.target;
  const submitButton = form.querySelector('.chat__send');
  submitButton.disabled = true;
  const data = new FormData(form);
  const messagesContainer = document.querySelector('.chat__messages');
  const userMessage = makeMessageElement(data.get('message'), 'user');
  messagesContainer.appendChild(userMessage);
  scrollToBottom();

  form.reset();
  form.querySelectorAll('.errorlist').forEach((element) => {
    element.remove();
  });

  const assistantMessage = makeMessageElement('Thinking...', 'assistant');
  messagesContainer.appendChild(assistantMessage);

  const response = await fetch(form.action, {
    method: 'POST',
    body: data,
    credentials: 'include',
  });

  if (response.ok) {
    const chunks = [];
    const reader = response.body.getReader();
    while (true) {
      const {done, value} = await reader.read();
      if (done) break;
      const text = new TextDecoder().decode(value);
      chunks.push(text);
      assistantMessage.textContent = chunks.join('');
      scrollToBottom();
    }
  } else if (response.status === 400) {
    const text = await response.text();
    const div = document.createElement('div');
    div.innerHTML = text;
    const newForm = div.querySelector(`#${form.id}`);
    userMessage.remove();
    assistantMessage.remove();
    form.replaceWith(newForm);
    newForm.addEventListener('submit', handleSumbit);
  } else {
    assistantMessage.textContent = 'Error: Unable to process your request';
  }
  submitButton.disabled = false;
}

async function handleClear(event) {
  event.preventDefault();

  const form = event.target;
  const data = new FormData(form);

  const response = await fetch(form.action, {
    method: 'POST',
    body: data,
    credentials: 'include',
  });
  if (response.ok) {
    const messagesContainer = document.querySelector('.chat__messages');
    messagesContainer.innerHTML = '';
  } else {
    console.error('Failed to clear chat:', response.statusText);
  }
}

function scrollToBottom() {
  const messagesContainer = document.querySelector('.chat__messages');
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function makeMessageElement(message, type) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('chat__msg', `chat__msg--${type}`);
  messageElement.textContent = message;
  return messageElement;
}

const toggleButton = document.querySelector('.chat__toggle');
toggleButton.addEventListener('click', () => {
  const chat = document.getElementById('chat');
  chat.classList.toggle('chat--open');
});

const closeButton = document.querySelector('.chat__close');
closeButton.addEventListener('click', () => {
  const chat = document.getElementById('chat');
  chat.classList.remove('chat--open');
});
