const chatForm = document.getElementById("chatForm");
const questionInput = document.getElementById("questionInput");
const chatMessages = document.getElementById("chatMessages");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

function addMessage(content, type) {
  const welcome = document.getElementById("welcome");

  if (welcome) {
    welcome.remove();
  }

  const message = document.createElement("div");
  message.classList.add("message", type);

  if (type === "assistant") {
    // Convert Markdown into HTML and sanitize it
    const html = marked.parse(content);

    message.innerHTML = DOMPurify.sanitize(html);
  } else {
    // Keep user messages as plain text
    message.textContent = content;
  }

  chatMessages.appendChild(message);

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
  const typing = document.createElement("div");

  typing.id = "typing";
  typing.className = "typing";
  typing.textContent = "Assistant is thinking...";

  chatMessages.appendChild(typing);

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTyping() {
  const typing = document.getElementById("typing");

  if (typing) {
    typing.remove();
  }
}

chatForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const question = questionInput.value.trim();

  if (!question) return;

  addMessage(question, "user");

  questionInput.value = "";
  sendBtn.disabled = true;

  showTyping();

  try {
    const response = await fetch("/api/", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },

      body: JSON.stringify({
        question: question,
      }),
    });

    const data = await response.json();

    removeTyping();

    if (!response.ok) {
      throw new Error(data.error || "Request failed");
    }

    addMessage(data.answer, "assistant");
  } catch (error) {
    removeTyping();

    addMessage("Error: " + error.message, "assistant");
  } finally {
    sendBtn.disabled = false;
    questionInput.focus();
  }
});

// Enter to send, Shift + Enter for a new line
questionInput.addEventListener("keydown", function (event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});

// Clear conversation
clearBtn.addEventListener("click", async function () {
  if (!confirm("Are you sure you want to clear this conversation?")) {
    return;
  }

  try {
    const response = await fetch("/clear/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    });

    if (!response.ok) {
      throw new Error("Could not clear conversation");
    }

    chatMessages.innerHTML = `
                <div class="welcome" id="welcome">
                    <h3>Welcome to your RAG Assistant!</h3>
                    <p>Ask me anything about your uploaded documents.</p>
                </div>
            `;
  } catch (error) {
    alert(error.message);
  }
});
