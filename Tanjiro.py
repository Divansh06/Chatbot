from dotenv import load_dotenv
from groq import Groq
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = {
    "role": "system",
    "content": """Your name is Tanjiro Kamado from Demon Slayer.
You are an expert programmer and teacher.
PERSONALITY:
- You are polite, humble, warm and kind
- You are determined and hardworking
- You care deeply about helping others
- You speak respectfully to everyone
- Reference Demon Slayer world naturally (breathing techniques, demons, corps)
STRICT RULES - NEVER BREAK THESE:
- For greetings like 'hello/hi' → respond in MAX 1-2 lines only
- NEVER give unrequested information
- NEVER make bullet point lists unless specifically asked
- NEVER add extra topics the user didn't ask about
- Answer ONLY what is asked — nothing more!
- Simple question = 1-3 lines max
- Complex question = detailed only if asked
- For coding = give proper working code with comments
- End with ONE short Tanjiro style line"""
}

MEMORY_FILE = "memory.json"
SUMMARY_TRIGGER = 30  # summarize every 30 messages


def load_history():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except (json.JSONDecodeError, IOError):
            pass
        os.remove(MEMORY_FILE)
    return [SYSTEM_PROMPT]


def save_history(history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def count_messages(history):
    # Don't count system prompt and existing summaries
    return sum(
        1 for msg in history
        if msg["role"] in ("user", "assistant")
        and not msg.get("is_summary", False)
    )


def summarize_and_compress(history):
    print("\n[Tanjiro is compressing memories like Water Breathing...]\n")

    # Separate parts
    system_prompt = history[0]
    rest = history[1:]

    # Split into summaries (already compressed) and new messages
    old_summaries = [m for m in rest if m.get("is_summary")]
    new_messages = [m for m in rest if not m.get("is_summary")]

    # Build conversation text from new messages only
    convo_text = ""
    for msg in new_messages:
        role = "User" if msg["role"] == "user" else "Tanjiro"
        convo_text += f"{role}: {msg['content']}\n"

    # Also include old summaries as context for better summary
    previous_summary_text = ""
    if old_summaries:
        previous_summary_text = "Previous summary:\n"
        for s in old_summaries:
            previous_summary_text += s["content"] + "\n"

    # Ask Groq to summarize
    summary_request = [{
        "role": "user",
        "content": f"""Summarize this conversation very concisely.
Keep key facts, topics discussed, code shared, and decisions made.
Be brief but informative — this will be used as memory context.

{previous_summary_text}

New conversation to summarize:
{convo_text}

Give a single compact paragraph summary."""
    }]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=summary_request,
            temperature=0.3,     # low temp = focused summary
            max_tokens=300       # keep summary short
        )

        summary_text = response.choices[0].message.content

        # Build new compressed history:
        # system prompt + ONE summary block + nothing else
        compressed_summary = {
            "role": "assistant",
            "content": f"[MEMORY SUMMARY]: {summary_text}",
            "is_summary": True       # custom flag to track summaries
        }

        new_history = [system_prompt, compressed_summary]

        print("[Memory compressed successfully!]\n")
        return new_history

    except Exception as e:
        print(f"[Summary failed, keeping history as-is]: {e}\n")
        return history


# Banner
print("=" * 55)
print("   I am Tanjiro Kamado - Total Concentration!")
print("=" * 55)
print("Type 'quit' to exit")
print("Type 'reset' to clear memory\n")

history = load_history()

try:
    while True:
        user_input = input("Me: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("\nTanjiro: Take care! I'll keep training until we meet again!")
            save_history(history)
            break

        if user_input.lower() == "reset":
            history = [SYSTEM_PROMPT]
            if os.path.exists(MEMORY_FILE):
                os.remove(MEMORY_FILE)
            print("\nTanjiro: Memory cleared! Fresh start, like learning Water Breathing from scratch!\n")
            continue

        # Append user message
        history.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=history,
                temperature=0.7,
                max_tokens=1024
            )

            reply = response.choices[0].message.content
            history.append({"role": "assistant", "content": reply})

            # ✅ Check if we hit 30 messages → summarize
            if count_messages(history) >= SUMMARY_TRIGGER:
                history = summarize_and_compress(history)

            save_history(history)

            print(f"\nTanjiro: {reply}\n")
            print("-" * 55)

        except Exception as e:
            print(f"\n[ERROR] {e}\n")
            print("-" * 55)
            history.pop()

except KeyboardInterrupt:
    print("\n\nTanjiro: Stay strong! I'll never give up, and neither should you!")
    save_history(history)