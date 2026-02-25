// Chat Bot Functionality
class ChatBot {
    constructor() {
        this.chatInput = document.getElementById('chatInput');
        this.chatForm = document.getElementById('chatForm');
        this.chatMessages = document.getElementById('chatMessages');
        this.quickActions = document.getElementById('quickActions');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.init();
    }

    init() {
        this.chatForm.addEventListener('submit', (e) => this.handleSendMessage(e));
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage(this.chatInput.value);
            }
        });

        // Focus on input
        this.chatInput.focus();
    }

    handleSendMessage(event) {
        event.preventDefault();
        const message = this.chatInput.value.trim();
        if (message) {
            this.sendMessage(message);
        }
    }

    sendMessage(message) {
        if (!message.trim()) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.chatInput.value = '';
        this.chatInput.focus();

        // Hide quick actions after first message
        if (this.quickActions.style.display !== 'none') {
            this.quickActions.style.display = 'none';
        }

        // Show typing indicator
        this.showTypingIndicator();

        // Call server QA endpoint for answers (fallback to local KB)
        fetch('/api/qa', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: message })
        })
        .then(res => res.json())
        .then(data => {
            this.hideTypingIndicator();
            if (data && data.success && data.answer) {
                this.addMessage(data.answer, 'bot');
            } else if (data && data.error) {
                // fallback to canned response if server returned an error
                const fallback = this.getBotResponse(message);
                this.addMessage(data.error || fallback, 'bot');
            } else {
                const fallback = this.getBotResponse(message);
                this.addMessage(fallback, 'bot');
            }
        })
        .catch(err => {
            this.hideTypingIndicator();
            const fallback = this.getBotResponse(message);
            this.addMessage('Sorry, I could not reach the server. ' + fallback, 'bot');
        });
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        let avatar = sender === 'user' ? '👤' : '🤖';
        let content = text;

        // Add formatting for bot messages
        if (sender === 'bot') {
            content = this.formatBotMessage(text);
        }

        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">${content}</div>
            <div class="message-time">${this.getCurrentTime()}</div>
        `;

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatBotMessage(text) {
        // Add formatting to bot messages
        let formatted = `<p>${text}</p>`;

        // Check for specific topics and provide formatted responses
        if (text.includes('steps:') || text.includes('features:')) {
            formatted = `<div class="bot-formatted">
                <p>${text}</p>
            </div>`;
        }

        return formatted;
    }

    getBotResponse(userMessage) {
        const message = userMessage.toLowerCase().trim();

        // Knowledge base for the chatbot
        const responses = {
            // Upload related
            'how do i upload a pdf': `Here are the steps to upload a PDF:
1. Click on the "📤 Upload File" tab at the top
2. Drag and drop your PDF file into the upload box OR click to browse
3. Select the PDF file from your computer
4. Choose processing options (extract text, metadata, tables, images)
5. Click "Process Files" and wait for completion
6. Download your results!

We support files up to 100 MB. Multiple files can be uploaded at once.`,

            'what can you do': `I can help you with PDF processing tasks:

📄 Extract Text - Get all text content from PDFs
📋 Extract Metadata - View document information
📊 Extract Tables - Get structured data from tables
🖼️ Extract Images - Save images from PDFs
🔗 Merge PDFs - Combine multiple files into one
✂️ Split PDFs - Break a document into separate pages
🔄 Rotate Pages - Adjust page orientation

Just upload your PDF files and select what you need!`,

            'how do i merge pdfs': `To merge PDF files:
Steps:
1. Go to "Upload File" tab
2. Upload multiple PDF files
3. The order matters! Upload them in the order you want them merged
4. Select any processing options you need
5. Submit and your merged PDF will be ready
6. Download the combined file

📌 Tip: Upload files in the exact order you want them merged!`,

            'how do i extract text': `To extract text from a PDF:
Steps:
1. Go to "Upload File" tab
2. Upload your PDF file
3. Check the "Extract Text" option ✓
4. Click "Process Files"
5. The extracted text will appear in the results
6. You can copy or download the text

💡 Tip: Works with most PDFs, including scanned documents!`,

            'how do i split a pdf': `To split a PDF into separate pages:
Steps:
1. Go to "Upload File" tab
2. Upload your PDF file
3. The file will show options for splitting
4. Process the file
5. You'll get individual page files
6. Download the pages you need

📌 Tip: Perfect for extracting specific pages from large documents!`,

            'how do i rotate pages': `To rotate PDF pages:
Steps:
1. Go to "Upload File" tab
2. Upload your PDF file
3. Choose rotation option (90°, 180°, or 270°)
4. Process the file
5. Download your rotated PDF

Common rotations:
• 90° - Rotate right
• 180° - Flip upside down
• 270° - Rotate left`,

            'extract images': `To extract images from a PDF:
Steps:
1. Go to "Upload File" tab
2. Upload your PDF file
3. Check the "Extract Images" option ✓
4. Click "Process Files"
5. All images will be extracted
6. Download them as image files

🖼️ Supported formats: PNG, JPG, and other common image formats`,

            'hello': `Hello! 👋 Welcome to PDF Processor! How can I help you today?

Popular topics:
• How do I upload a PDF?
• What features are available?
• How do I merge PDFs?
• How do I extract text?`,

            'hi': `Hi there! 👋 I'm here to help you with your PDF processing needs. What would you like to do?`,

            'help': `I can assist you with:
📤 Uploading PDFs
📄 Text extraction
📋 Metadata retrieval
📊 Table extraction
🖼️ Image extraction
🔗 Merging files
✂️ Splitting documents
🔄 Rotating pages

Feel free to ask about any of these features!`,

            'thank you': `You're welcome! 😊 Is there anything else I can help you with?`,

            'thanks': `Happy to help! 🎉 Let me know if you need anything else!`,

            'default': `That's a great question! Here's what I can help you with:

Available Features:
✓ Extract text from PDFs
✓ Get document metadata
✓ Extract tables and data
✓ Extract images
✓ Merge multiple PDFs
✓ Split PDF pages
✓ Rotate pages

Which feature would you like to learn more about? Just ask me anything related to PDF processing!`
        };

        // Find matching response
        for (const [key, response] of Object.entries(responses)) {
            if (message.includes(key)) {
                return response;
            }
        }

        // Default response for unknown queries
        return responses['default'];
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
    }
}

// Helper function for quick action buttons
function sendMessage(message) {
    window.chatBot.sendMessage(message);
}

// Initialize chat bot when page loads
let chatBot;
document.addEventListener('DOMContentLoaded', () => {
    chatBot = new ChatBot();
});

// Minimize chat function (optional)
document.addEventListener('DOMContentLoaded', () => {
    const minimizeBtn = document.getElementById('minimizeChat');
    const chatWrapper = document.querySelector('.chat-wrapper');
    if (minimizeBtn) {
        minimizeBtn.addEventListener('click', function() {
            chatWrapper.classList.toggle('minimized');
            this.textContent = chatWrapper.classList.contains('minimized') ? '▢' : '−';
        });
    }
});
