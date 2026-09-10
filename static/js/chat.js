/**
 * DIP Diet RAG Agent — Chat Interface JavaScript
 * Handles message sending, streaming display, file uploads,
 * and session info updates.
 */

(function () {
  'use strict';

  // ── DOM refs ──────────────────────────────────────────────────────────────
  const chatForm        = document.getElementById('chatForm');
  const chatInput       = document.getElementById('chatInput');
  const chatMessages    = document.getElementById('chatMessages');
  const sendBtn         = document.getElementById('sendBtn');
  const typingIndicator = document.getElementById('typingIndicator');
  const welcomeScreen   = document.getElementById('welcomeScreen');
  const charCount       = document.getElementById('charCount');
  const msgCountEl      = document.getElementById('msgCount');
  const kbDocsEl        = document.getElementById('kbDocs');
  const modelInfoEl     = document.getElementById('modelInfo');
  const agentStatusEl   = document.getElementById('agentStatus');

  let messageCount = 0;
  let lastModelUsed = '—';

  // ── Configure marked.js ───────────────────────────────────────────────────
  if (typeof marked !== 'undefined') {
    marked.setOptions({ breaks: true, gfm: true });
  }

  // ── Char counter ──────────────────────────────────────────────────────────
  chatInput.addEventListener('input', () => {
    const len = chatInput.value.length;
    charCount.textContent = `${len} / 2000`;
    charCount.style.color = len > 1800 ? '#ef4444' : '';
  });

  // ── Enter to send (Shift+Enter for new line) ──────────────────────────────
  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (chatInput.value.trim()) chatForm.dispatchEvent(new Event('submit'));
    }
  });

  // ── Quick prompt buttons ──────────────────────────────────────────────────
  document.querySelectorAll('.quick-prompt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      chatInput.value = btn.dataset.prompt;
      chatInput.focus();
      chatForm.dispatchEvent(new Event('submit'));
    });
  });

  // ── Form submit ───────────────────────────────────────────────────────────
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    // Hide welcome screen
    if (welcomeScreen) welcomeScreen.classList.add('d-none');

    // Append user bubble
    appendUserMessage(message);
    chatInput.value = '';
    charCount.textContent = '0 / 2000';
    sendBtn.disabled = true;
    showTyping(true);
    updateAgentStatus('Thinking…', 'text-warning');

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      const data = await res.json();

      if (!res.ok || data.error) {
        appendAgentMessage(`⚠️ **Error:** ${data.error || 'Unknown error. Please try again.'}`, [], '');
      } else {
        appendAgentMessage(data.response, data.sources || [], data.model_used || '');
        lastModelUsed = data.model_used || lastModelUsed;
        if (modelInfoEl) modelInfoEl.textContent = lastModelUsed;
      }
    } catch (err) {
      appendAgentMessage('⚠️ **Connection error.** Please check your connection and try again.', [], '');
    } finally {
      sendBtn.disabled = false;
      showTyping(false);
      updateAgentStatus('Ready · IBM WatsonX AI', 'text-success');
      messageCount++;
      if (msgCountEl) msgCountEl.textContent = messageCount;
      chatInput.focus();
    }
  });

  // ── Append user message ───────────────────────────────────────────────────
  function appendUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'chat-bubble user-bubble mb-3 d-flex justify-content-end';
    div.innerHTML = `<div class="bubble-content user-content">${escapeHtml(text)}</div>`;
    chatMessages.insertBefore(div, typingIndicator);
    scrollToBottom();
  }

  // ── Append agent message ──────────────────────────────────────────────────
  function appendAgentMessage(rawText, sources, modelUsed) {
    const div = document.createElement('div');
    div.className = 'chat-bubble agent-bubble mb-3 d-flex align-items-start gap-2';

    const rendered = typeof marked !== 'undefined' ? marked.parse(rawText) : escapeHtml(rawText);

    let sourcesHtml = '';
    if (sources && sources.length > 0) {
      const badges = sources.slice(0, 4).map(s =>
        `<span class="badge bg-light text-muted border me-1 source-badge" title="Relevance: ${s.score || ''}">
           <i class="bi bi-book me-1"></i>${truncate(s.source || '', 28)}
         </span>`
      ).join('');
      sourcesHtml = `<div class="source-tags mt-1">${badges}</div>`;
    }

    let modelHtml = '';
    if (modelUsed) {
      modelHtml = `<div class="small text-muted mt-1"><i class="bi bi-cpu me-1"></i>${escapeHtml(modelUsed)}</div>`;
    }

    div.innerHTML = `
      <div class="bubble-avatar flex-shrink-0">🥗</div>
      <div>
        <div class="bubble-content agent-content markdown-body">${rendered}</div>
        ${sourcesHtml}
        ${modelHtml}
      </div>
    `;
    chatMessages.insertBefore(div, typingIndicator);
    scrollToBottom();
  }

  // ── Typing indicator ──────────────────────────────────────────────────────
  function showTyping(show) {
    typingIndicator.classList.toggle('d-none', !show);
    typingIndicator.style.display = show ? 'flex' : 'none';
    if (show) scrollToBottom();
  }

  // ── Agent status ──────────────────────────────────────────────────────────
  function updateAgentStatus(text, colorClass) {
    if (!agentStatusEl) return;
    agentStatusEl.textContent = text;
    agentStatusEl.className = `small d-flex align-items-center gap-1 ${colorClass}`;
  }

  // ── Scroll to bottom ──────────────────────────────────────────────────────
  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // ── Clear chat ────────────────────────────────────────────────────────────
  const clearBtn = document.getElementById('btnClearChat');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      if (!confirm('Clear the entire chat history?')) return;
      fetch('/api/chat/clear', { method: 'POST' })
        .then(() => {
          chatMessages.querySelectorAll('.chat-bubble').forEach(b => b.remove());
          if (welcomeScreen) welcomeScreen.classList.remove('d-none');
          messageCount = 0;
          if (msgCountEl) msgCountEl.textContent = 0;
        });
    });
  }

  // ── Load agent stats ──────────────────────────────────────────────────────
  fetch('/api/agent-stats')
    .then(r => r.json())
    .then(data => {
      if (kbDocsEl) kbDocsEl.textContent = `${data.total_documents || 0} docs indexed`;
      if (modelInfoEl) modelInfoEl.textContent = data.watsonx_available
        ? 'IBM WatsonX AI' : 'Structured Fallback';
    })
    .catch(() => {
      if (kbDocsEl) kbDocsEl.textContent = 'Knowledge base ready';
    });

  // ── File upload ───────────────────────────────────────────────────────────
  const fileInput  = document.getElementById('fileInput');
  const uploadBtn  = document.getElementById('uploadBtn');
  const dropZone   = document.getElementById('dropZone');
  const uploadStatus  = document.getElementById('uploadStatus');
  const uploadResult  = document.getElementById('uploadResult');
  const uploadMsg     = document.getElementById('uploadMsg');

  if (fileInput) {
    fileInput.addEventListener('change', () => {
      uploadBtn.disabled = !fileInput.files.length;
    });
  }

  if (dropZone) {
    dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
    dropZone.addEventListener('drop', e => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');
      if (e.dataTransfer.files.length && fileInput) {
        fileInput.files = e.dataTransfer.files;
        uploadBtn.disabled = false;
      }
    });
  }

  if (uploadBtn) {
    uploadBtn.addEventListener('click', async () => {
      if (!fileInput || !fileInput.files.length) return;
      const formData = new FormData();
      formData.append('file', fileInput.files[0]);

      uploadStatus.classList.remove('d-none');
      uploadResult.classList.add('d-none');
      uploadBtn.disabled = true;
      if (uploadMsg) uploadMsg.textContent = 'Uploading and indexing…';

      try {
        const res  = await fetch('/api/upload-knowledge', { method: 'POST', body: formData });
        const data = await res.json();
        uploadStatus.classList.add('d-none');
        uploadResult.classList.remove('d-none');
        if (data.error) {
          uploadResult.className = 'alert alert-danger py-2';
          uploadResult.textContent = `❌ ${data.error}`;
        } else {
          uploadResult.className = 'alert alert-success py-2';
          uploadResult.textContent = `✅ ${data.message}`;
          if (kbDocsEl) kbDocsEl.textContent = 'Knowledge base updated';
        }
      } catch (err) {
        uploadStatus.classList.add('d-none');
        uploadResult.classList.remove('d-none');
        uploadResult.className = 'alert alert-danger py-2';
        uploadResult.textContent = '❌ Upload failed. Please try again.';
      } finally {
        uploadBtn.disabled = false;
      }
    });
  }

  // ── Count existing history messages ──────────────────────────────────────
  messageCount = Math.floor(chatMessages.querySelectorAll('.user-bubble').length);
  if (msgCountEl) msgCountEl.textContent = messageCount;

  // ── Scroll to bottom on load ──────────────────────────────────────────────
  scrollToBottom();

  // ── Helpers ───────────────────────────────────────────────────────────────
  function escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function truncate(str, maxLen) {
    return str.length > maxLen ? str.slice(0, maxLen) + '…' : str;
  }

})();
