# 🚀 Quick Start Guide

Get your AI Doppelgänger Engine running in minutes!

## Prerequisites

- Python 3.9 or higher
- OpenAI API key (or compatible LLM)
- Discord/Gmail/Reddit API keys (optional)

## Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd mirrorme-engine
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Configure your API keys**
   ```bash
   # Edit the .env file with your keys
   nano .env
   ```

   At minimum, you need:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## First Run

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open the dashboard**
   - Go to: http://localhost:8000
   - You'll see the main dashboard interface

3. **Train your AI twin**
   - Upload your Discord exports, emails, or social media data
   - The system will analyze your personality and communication style
   - This creates your digital twin's personality profile

## Basic Usage

### Training Your AI Twin

1. **Prepare your data**
   - Discord: Export your message history
   - Email: Export your emails
   - Social media: Export your posts/comments

2. **Upload and train**
   - Use the dashboard to upload your data
   - The system will analyze your personality traits
   - Training typically takes 5-10 minutes

### Testing Responses

1. **Use the test interface**
   - Go to the "Test Response Generator" section
   - Type a message you'd like to test
   - See how your AI twin would respond

2. **Adjust settings**
   - Change mood: Default, Energetic, Savage, Unhinged, etc.
   - Toggle auto-reply on/off
   - Set safety levels

### Safety Features

- **Redlines**: Configure topics your AI should never discuss
- **Consent management**: Control who your AI can interact with
- **Override controls**: Review responses before they're sent
- **Safety monitoring**: Track and review all AI interactions

## Configuration Options

### Mood Settings
- **Default**: Your normal personality
- **Energetic**: More enthusiastic and high-energy
- **Savage**: Sarcastic and witty responses
- **Unhinged**: Chaotic and unpredictable
- **Professional**: Formal and business-like
- **Casual**: Relaxed and informal

### Safety Modes
- **Strict**: Maximum safety, many responses require approval
- **Moderate**: Balanced safety and autonomy
- **Lenient**: Minimal safety restrictions

### Auto-Reply Settings
- **Enabled**: AI responds automatically
- **Disabled**: All responses require manual approval
- **Override Required**: AI generates responses but you must approve each one

## Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
pip install -r requirements.txt
```

**"OpenAI API key not found"**
- Check your .env file has the correct API key
- Ensure the key is valid and has credits

**"Dashboard not loading"**
- Check if the server is running on port 8000
- Try refreshing the page
- Check browser console for errors

**"Training failed"**
- Ensure your data files are in the correct format
- Check that files aren't corrupted
- Verify you have enough disk space

### Getting Help

- Check the logs in the `logs/` directory
- Review the full README.md for detailed documentation
- Check the API documentation at http://localhost:8000/docs

## Next Steps

Once you're comfortable with the basics:

1. **Connect platforms**: Set up Discord bot, Gmail integration, etc.
2. **Fine-tune personality**: Adjust your AI twin's traits and preferences
3. **Monitor performance**: Review response history and safety events
4. **Expand capabilities**: Add more data sources and platforms

## Safety Reminder

⚠️ **Important**: This tool is for educational and personal use. You are responsible for:
- Obtaining consent from contacts before AI interaction
- Ensuring compliance with platform terms of service
- Maintaining ethical boundaries in AI communications
- Taking responsibility for AI-generated content

---

*Happy doppelgänger-ing! 🧠✨* 