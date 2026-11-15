# Project Notes: gemini-web2api v2

A technical reference guide and architecture overview for `gemini-web2api-v2`.

---

## 1. What This Repository Does

`gemini-web2api-v2` acts as a local proxy that transforms Google Gemini's web interface (`gemini.google.com`) into an OpenAI-compatible REST/SSE API (`http://localhost:8081/v1`). 

It provides free access to Google's latest Gemini models (including **Gemini 4 Hydrogen** and **Gemini 4 Argon**) and can be plugged directly into Cursor, ChatBox, Cherry Studio, NextChat, or the OpenAI Python SDK.

---

## 2. Repository Structure

```
gemini-web2api-v2/
├── .gitignore                   # Excludes cookie.txt, config.json, and secrets
├── README.md                    # Quickstart guide & setup instructions
├── MODELS.md                    # Detailed model directory & reasoning specifications
├── REVERSE_ENGINEERING.md       # Deep dive into Google's StreamGenerate RPC
├── NOTES.md                     # This documentation file
├── config.example.json          # Example configuration file
├── pyproject.toml               # Python package configuration
├── requirements.txt             # Minimal dependencies (httpx, Pillow)
├── gemini_web2api.py            # Standalone single-file runner
├── gemini_web2api/              # Modular Python package
│   ├── __init__.py              # Exports MODELS, resolve_model, CONFIG
│   ├── __main__.py              # Entry point: python -m gemini_web2api
│   ├── config.py                # Configuration defaults and JSON loader
│   ├── models.py                # Model mappings, aliases, and think resolver
│   ├── gemini.py                # StreamGenerate RPC caller & cookie parser
│   ├── server.py                # HTTP server (OpenAI, Gemini CLI & UI routes)
│   ├── tools.py                 # OpenAI function calling & tool conversions
│   ├── multimodal.py            # Image upload and multimodal formatting
│   └── ui.html                  # Apple-designed web setup dashboard
└── tests/
    └── test_models.py           # Automated unit test suite
```

---

## 3. Reverse-Engineered Models Catalog

The model registry matches Google's Gemini Web UI:

| Model ID | UI Label | Wire Category (`inner[79]`) | Default Thinking (`inner[17]`) | Primary Role |
| :--- | :--- | :---: | :---: | :--- |
| **`gemini-4-hydrogen`** | Everyday help | `1` | `4` (Auto) | Fast general assistance, daily coding *(Default)* |
| **`gemini-4-argon`** | Code & analysis | `2` | `0` (Deep) | Frontier reasoning, math, multi-file code |
| **`gemini-3.1-pro`** | Detailed research | `3` | `4` (Auto) | Long-form analysis (requires Advanced cookie) |
| **`gemini-3.5-flash-lite`**| Quick answers | `6` | `4` (Auto) | Instant fact lookups, lowest latency |

### Thinking Level Control
Gemini Web controls thinking depth using payload slot `inner[17] = [[think_mode]]`:
- `0`: Deep thinking (~20k+ character reasoning output)
- `2`: Medium thinking
- `4`: Auto / shallow thinking

**How to adjust:**
1. Append `@think=N` to the model name (e.g. `gemini-4-argon@think=2`).
2. Pass OpenAI's standard parameter: `reasoning_effort: "high" | "medium" | "low"`.

---

## 4. How the Gateway Connects to Gemini

### The Wire Protocol
1. **Endpoint:** `POST https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate`
2. **Body:** Double-JSON encoded 102-element array passed in the form parameter `f.req`:
   - `inner[0]`: User prompt and optional file references
   - `inner[1]`: Language (`["en"]`)
   - `inner[10]`: Google Search grounding flag (`1`)
   - `inner[17]`: Thinking mode (`[[0]]` or `[[4]]`)
   - `inner[41]`: History persistence (`[1]` temporary, `[2]` standard)
   - `inner[59]`: Client session UUID
   - `inner[79]`: Model category enum
   - `at`: Page XSRF token (`SNlM0e`)
3. **Response Parsing:** Gemini Web returns batched streams marked with `wrb.fr`. The server extracts the text candidates from `inner[4][...][1]`, strips internal card metadata, and streams standard OpenAI SSE chunks.

---

## 5. Authentication & The `HTTP 400` Fix

* **Anonymous Mode (No Cookies):** 
  Google allows unauthenticated requests for `gemini-4-hydrogen` and `gemini-4-argon` with standard rate limits.
* **Authenticated Mode (Cookies):** 
  Needed for **Gemini Advanced (3.1 Pro)** routing.
  * **The Gotcha:** If you send cookies without Google's CSRF token (**`SNlM0e`**), Google rejects the request with `HTTP Error 400: Bad Request`.
  * **The Solution:** The server accepts both your cookie string and the `SNlM0e` token (extracted in DevTools Console via `copy(WIZ_global_data.SNlM0e)`), and saves them to `cookie.txt`.

---

## 6. Persistence Architecture

1. **Browser LocalStorage:** 
   The web dashboard at `http://localhost:8081/` caches your cookie string and XSRF token in your browser's private `localStorage`. Refreshing the page will not wipe your inputs or connection status.
2. **Server Disk (`cookie.txt`):** 
   Credentials are saved as JSON in `cookie.txt`. On startup, the server automatically detects and reloads `cookie.txt` without requiring any CLI flags.
3. **Git Protection (`.gitignore`):** 
   `cookie.txt`, `config.json`, and `.env` files are explicitly excluded by `.gitignore` to guarantee credentials are never uploaded to GitHub.

---

## 7. Multi-Device Network Access

The server binds to `0.0.0.0:8081`, so any device on your local Wi-Fi can connect:

* **This PC (Local):** `http://localhost:8081/v1`
* **Other Laptop / Mobile (Wi-Fi):** `http://192.168.100.59:8081/v1`
* **Web UI from any device:** `http://192.168.100.59:8081/`

---

## 8. Quick Commands

```bash
# Start server using package
python -m gemini_web2api

# Start server using single-file runner
python gemini_web2api.py

# Run test suite
python -m unittest discover tests

# Check API status
curl http://localhost:8081/api/status

# Test model listing
curl http://localhost:8081/v1/models
```
