# 🗡️ Tanjiro AI — Your Demon Slayer Coding Sensei

A terminal-based AI chatbot powered by **Groq** and **LLaMA 3.1**, where Tanjiro Kamado from Demon Slayer guides you through programming with warmth, determination, and Total Concentration.

---

## ✨ Features

- 🧠 **Persistent Memory** — Remembers conversations across sessions via `memory.json`
- 🗜️ **Auto Compression** — Summarizes every 30 messages so memory stays tiny forever
- 🎭 **In-Character Responses** — Tanjiro's personality woven into every reply
- ⚡ **Fast Responses** — Powered by Groq's ultra-fast LLaMA 3.1 8B inference
- 🔒 **Private** — API keys and chat history never leave your machine

---

## 📁 Project Structure

```
CHATBOT/
├── Tanjiro.py          # Main chatbot script
├── memory.json      # Auto-generated chat history (gitignored)
├── .env             # Your API key (gitignored)
├── .gitignore       # Excludes memory.json and .env
└── README.md
```

---

## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/Divansh06/CHATBOT.git
cd CHATBOT
```

### 2. Install dependencies
```bash
pip install groq python-dotenv
```

### 3. Get your Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Create a free account and generate an API key

### 4. Create your `.env` file
```bash
GROQ_API_KEY=your_api_key_here
```

### 5. Run it
```bash
python Tanjiro.py
```

---

## 💬 Usage

```
Me: what is a for loop?
Tanjiro: A for loop repeats a block of code a set number of times...
         ...Like repeating a Breathing Form until it's perfect!

Me: reset        # clears all memory
Me: quit         # saves and exits
```

---

## 🧠 How Memory Works

```
Every conversation turn:
  → appended to history list
  → saved to memory.json

Every 30 messages:
  → Groq summarizes everything into 1 compact paragraph
  → Old messages wiped, summary kept
  → File stays small forever

On next launch:
  → memory.json loaded → conversation resumes
```

This means after a year of daily use, your memory file stays around **~20 MB max** instead of growing endlessly.

---

## 🔒 .gitignore

```
memory.json
.env
```

Never commit your API key or private conversations.

---

## 🛠️ Configuration

In `Tanjiro.py` you can tweak:

| Variable | Default | Description |
|---|---|---|
| `SUMMARY_TRIGGER` | `30` | Messages before auto-summarize |
| `max_tokens` | `1024` | Max response length |
| `temperature` | `0.7` | Creativity (0 = focused, 1 = creative) |
| `model` | `llama-3.1-8b-instant` | Groq model to use |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `groq` | Groq API client |
| `python-dotenv` | Load `.env` variables |

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — Blazing fast LLM inference
- [Demon Slayer](https://kimetsu.com) — For Tanjiro's inspiration
- Meta — LLaMA 3.1 model

---

*"No matter how difficult the path, I will never give up — and neither will this chatbot!"* — Tanjiro Kamado
