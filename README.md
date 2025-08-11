# 🧠 AI Doppelgänger Engine (MirrorMe)

> *"Your digital twin that lives on the internet while you nap in a hoodie"*

## 🎯 Project Overview

The AI Doppelgänger Engine is a full-stack AI system that learns from your digital footprint and autonomously manages your digital interactions with eerie, hyper-personal accuracy. It's not just another chatbot - it's your synthetic consciousness that can:

- Respond to DMs, emails, and messages in your exact style
- Post on social media with your signature tone and humor
- Hold conversations that sound indistinguishable from you
- Make decisions you would likely make
- Manage your digital "you-ness" while you're offline

## 🚀 Features

### Core Capabilities
- **Personality Cloning**: Learns your writing style, humor, and communication patterns
- **Multi-Platform Integration**: Discord, Gmail, Twitter, Slack, and more
- **Autonomous Decision Making**: Responds to messages based on your historical patterns
- **Style Transfer**: Maintains your unique voice across all interactions
- **Safety Controls**: Built-in safeguards to prevent relationship-ruining responses

### Advanced Features
- **Live Preview Dashboard**: See what your AI twin is doing in real-time
- **Override Controls**: Approve or deny AI decisions before they're sent
- **Mood Selector**: Adjust response style (default, energetic, savage, unhinged)
- **Shadow Mode**: Test responses before enabling autonomous mode
- **Digital Will**: Create auto-responses for post-death scenarios

## 🏗️ Architecture

```
/mirrorme-engine/
├── /data_ingestion/          # Data collection and processing
├── /personality_core/        # AI personality modeling
├── /response_engine/         # Message generation and routing
├── /dashboard/              # Web interface
├── /api/                    # Platform integrations
├── /safety/                 # Ethics and safety modules
└── /config/                 # Configuration files
```

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenAI API key (or compatible LLM)
- Platform API keys (Discord, Gmail, etc.)

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd mirrorme-engine

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the development server
python app.py
```

## 📊 Data Sources

The engine learns from:
- **Email exports** (Gmail/Outlook)
- **Discord DMs & Servers**
- **Social media posts** (Twitter, Reddit, Instagram)
- **Chat logs** (Messenger, WhatsApp, Telegram)
- **Voice transcripts** (optional)
- **Long-form writing** (blogs, essays, documents)

## 🔐 Safety & Ethics

- **Consent-aware**: Flags new contacts, doesn't impersonate without permission
- **Redlines**: Configurable boundaries for sensitive topics
- **Override controls**: Human oversight for all AI decisions
- **Audit trails**: Complete logs of all interactions

## 🎮 Usage

1. **Data Ingestion**: Upload your digital footprint
2. **Personality Training**: Let the AI learn your style
3. **Configuration**: Set up platform integrations
4. **Deployment**: Enable autonomous mode with safety controls
5. **Monitoring**: Use the dashboard to oversee your digital twin

## ⚠️ Disclaimer

This tool is for educational and personal use. Users are responsible for:
- Obtaining consent from contacts before AI interaction
- Ensuring compliance with platform terms of service
- Maintaining ethical boundaries in AI communications
- Taking responsibility for AI-generated content

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines and code of conduct.

## 📄 License

MIT License - see LICENSE file for details.

---

*Built with ❤️ and a healthy dose of existential dread* 