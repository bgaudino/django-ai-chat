const root = document.getElementById('chat-root');
const shadow = root.attachShadow({mode: 'open'});

let config = {};

shadow.innerHTML = `
  <div class="chat" id="chat"></div>
`;

async function loadChat() {
  const url = root.dataset.url;
  const response = await fetch(url);
  if (!response.ok) {
    console.error('Failed to load chat:', response.statusText);
    return false;
  }
  const data = await response.text();
  shadow.getElementById('chat').innerHTML = data;
  return true;
}

const loaded = await loadChat();

if (loaded) {
  config = JSON.parse(shadow.getElementById('config').textContent);
  const form = shadow.getElementById('chat-form');
  form.addEventListener('submit', handleSumbit);

  const clearForm = shadow.getElementById('clear-form');
  if (clearForm) {
    clearForm.addEventListener('submit', handleClear);
  }

  const toggleButton = shadow.querySelector('.chat__toggle');
  toggleButton.addEventListener('click', () => {
    const chat = shadow.getElementById('chat');
    chat.classList.toggle('chat--open');
    scrollToBottom();
  });

  const closeButton = shadow.querySelector('.chat__close');
  closeButton.addEventListener('click', () => {
    const chat = shadow.getElementById('chat');
    chat.classList.remove('chat--open');
  });

  shadow.getElementById('id_message').addEventListener('input', resize);
  shadow.addEventListener('keypress', function (e) {
    if (e.target.id === 'id_message' && e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      shadow.querySelector('.chat__send').click();
    }
  });

  scrollToBottom();
}

async function handleSumbit(event) {
  event.preventDefault();

  const form = event.target;
  const submitButton = form.querySelector('.chat__send');
  submitButton.disabled = true;
  const data = new FormData(form);
  const messagesContainer = shadow.querySelector('.chat__messages');
  const userMessage = makeMessageElement(data.get('message'), 'user');
  messagesContainer.appendChild(userMessage);
  scrollToBottom();

  form.reset();
  resize.call(shadow.getElementById('id_message'));
  clearErrors(form);

  const assistantMessage = makeMessageElement('Thinking...', 'assistant');
  assistantMessage.setAttribute('aria-busy', 'true');
  messagesContainer.appendChild(assistantMessage);
  scrollToBottom();

  const response = await fetch(form.action, {
    method: 'POST',
    body: data,
    credentials: 'include',
  });

  if (response.ok) {
    const reader = response.body.getReader();
    assistantMessage.removeAttribute('aria-busy');
    while (true) {
      const {done, value} = await reader.read();
      if (done) break;
      const text = new TextDecoder().decode(value);
      if (config.RENDER_MARKDOWN) {
        assistantMessage.innerHTML = text;
      } else {
        assistantMessage.textContent = text;
      }
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
    newForm.querySelector('#id_message').addEventListener('input', resize);
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
    const messagesContainer = shadow.querySelector('.chat__messages');
    messagesContainer.innerHTML = '';
    clearErrors(shadow.getElementById('chat-form'));
  } else {
    console.error('Failed to clear chat:', response.statusText);
  }
}

function clearErrors(form) {
  form.querySelectorAll('.errorlist').forEach((element) => {
    element.remove();
  });
  form.querySelectorAll('.form-error').forEach((element) => {
    element.remove();
  });
  form.querySelectorAll('[aria-invalid]').forEach((element) => {
    element.removeAttribute('aria-invalid');
  });
}

function scrollToBottom() {
  const messagesContainer = shadow.querySelector('.chat__messages');
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function resize() {
  this.style.height = 'auto';
  if (this.scrollHeight > 180) {
    this.style.height = '180px';
  } else {
    // Prevent small resize on initial input
    const offset = 2;
    this.style.height = `${this.scrollHeight + offset}px`;
  }
  scrollToBottom();
}

function makeMessageElement(message, type) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('chat__msg', `chat__msg--${type}`);
  messageElement.textContent = message;
  return messageElement;
}
