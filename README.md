# 🤖 AI Excuse Generator

An AI-powered application that generates realistic excuses for various scenarios with fake proofs, emergency alerts, and smart ranking system.

## ✨ Features

1. **AI-Generated Excuses** - Context-based excuse suggestions (work, school, social, family)
2. **Scenario-Based Customization** - Refine excuses based on urgency and believability
3. **Proof Generator** - Generate fake documents, chat screenshots, and location logs
4. **Emergency Call & Text System** - Auto-trigger fake emergency messages
5. **AI Guilt-Tripping Apology Generator** - Create professional or emotional apologies
6. **Voice & Text Integration** - Excuses in written and speech format
7. **Excuse History & Favorites** - Save frequently used excuses
8. **Auto-Scheduling** - AI predicts when you might need an excuse
9. **Multi-Language Support** - Excuses in different languages
10. **Smart Excuse Ranking** - Rank excuses by effectiveness

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Ollama (for local LLM)

### Setup

1. Clone the repository
2. Install Ollama from https://ollama.com
3. Pull the models:
   \\\ash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   \\\
4. Install Python packages:
   \\\ash
   pip install openai python-dotenv scikit-learn numpy gtts
   \\\
5. Run the app:
   \\\ash
   python app.py
   \\\

## 📋 Usage

Run \python app.py\ and select from 10 different features.

## 🛠️ Tech Stack

- **Local LLM**: Ollama with Llama 3.2
- **Embeddings**: nomic-embed-text for RAG
- **Database**: SQLite for history and ranking
- **Voice**: gTTS for text-to-speech

## 📄 License

MIT

## ⚠️ Disclaimer

This tool is for entertainment purposes only. Use responsibly.
