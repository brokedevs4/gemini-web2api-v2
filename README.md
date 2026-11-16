# gemini-web2api v2

<p align="center">
  <img src="logo.png" width="180" alt="gemini-web2api logo">
</p>

Convert Google Gemini's web interface into an OpenAI-compatible and Google Gemini CLI-compatible API.

This updated version reverse engineers the latest **Gemini Web UI** (including **Gemini 4 Hydrogen**, **Gemini 4 Argon**, **Gemini 3.1 Pro**, **Gemini 3.5 Flash-Lite**, and configurable **Thinking levels**).

---

## 📸 Gemini Web UI Models

Based directly on the Gemini Web model selector:

| UI Label | UI Subtitle | Badge | Model Identifier | Best For | Default Think Level |
| :--- | :--- | :---: | :--- | :--- | :---: |
| **Everyday help** | **4 Hydrogen** | `[New]` | `gemini-4-hydrogen` *(default)* | Fast daily assistance, agentic tasks, general coding | `4` (Auto) |
| **Code & analysis** | **4 Argon** | — | `gemini-4-argon` | Deep reasoning, complex algorithms, mathematical logic | `0` (Deep) |
| **Detailed research** | **3.1 Pro** | — | `gemini-3.1-pro` | Multi-source research, complex documents (needs cookie) | `4` (Auto) |
| **Quick answers** | **3.5 Flash-Lite** | — | `gemini-3.5-flash-lite` | Lowest latency, instant facts, rapid lookups | `4` (Auto) |

*(See [MODELS.md](MODELS.md) for full descriptions, aliases, and mode mappings).*  
*(See [REVERSE_ENGINEERING.md](REVERSE_ENGINEERING.md) for wire protocol, payload formats, and RPC analysis).*

---

## 🧠 Thinking Levels

The UI **"Thinking level >"** submenu is directly controllable in your requests:

### Method 1: Model Suffix (`@think=N`)
- `gemini-4-argon@think=0` (Deep thinking / high reasoning)
- `gemini-4-hydrogen@think=2` (Medium thinking)
- `gemini-4-hydrogen@think=4` (Auto / shallow)

### Method 2: OpenAI `reasoning_effort` Parameter
Pass `reasoning_effort` in standard `/v1/chat/completions` calls:
```json
{
  "model": "gemini-4-argon",
  "reasoning_effort": "high",
  "messages": [{"role": "user", "content": "Analyze and optimize this code"}]
}
```

---

## 🚀 Quick Start

### 1. Installation
```bash
pip install httpx Pillow
```

### 2. Start the Server

**Using the package:**
```bash
python -m gemini_web2api
```

**Or using the single-file runner:**
```bash
python gemini_web2api.py
```

The server starts at `http://localhost:8081/v1`.

---

## 🛠️ Usage Examples

### cURL (OpenAI Chat Completions)
```bash
curl http://localhost:8081/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-4-hydrogen",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### OpenAI Python SDK
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8081/v1", api_key="sk-gemini")

response = client.chat.completions.create(
    model="gemini-4-argon",
    reasoning_effort="high",
    messages=[{"role": "user", "content": "Explain quantum error correction"}]
)

print(response.choices[0].message.content)
```

### Gemini CLI Compatibility
```bash
export GEMINI_API_KEY=none
export GOOGLE_GEMINI_BASE_URL=http://localhost:8081
gemini
```
Supports native endpoints:
- `GET /v1beta/models`
- `POST /v1beta/models/{model}:generateContent`
- `POST /v1beta/models/{model}:streamGenerateContent`

---

## 🍪 Optional: Cookie Configuration (For Pro Routing)

Anonymous mode works out-of-the-box for Hydrogen, Argon, and Flash-Lite. To route to **3.1 Pro** without fallback to Flash, supply your Gemini Advanced cookies in `cookie.txt` or `config.json`:

```bash
python -m gemini_web2api --cookie-file cookie.txt
```

Format of `cookie.txt`:
```
SID=...; HSID=...; SSID=...; APISID=...; SAPISID=...; __Secure-1PSID=...
```

---

## 📂 Documentation

- [**MODELS.md**](MODELS.md): In-depth model descriptions, aliases, thinking modes.
- [**REVERSE_ENGINEERING.md**](REVERSE_ENGINEERING.md): Detailed reverse engineering breakdown of Google Gemini Web's `StreamGenerate` RPC, payload slot indices, and token authentication.
