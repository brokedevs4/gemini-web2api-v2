# Gemini Web UI Models Specification

This document details the reverse-engineered model catalog corresponding to Google Gemini Web's interface (November 2026 update).

---

## 1. UI Model Overview

In the Gemini Web model selector dropdown, Google presents four primary tiers alongside a configurable **Thinking level**:

| UI Label | UI Subtitle | Badge | Primary Model ID | Internal Mode Category | Default Think Mode |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Everyday help** | **4 Hydrogen** | `[New]` | `gemini-4-hydrogen` | `1` (Fast/Everyday) | `4` (Auto) |
| **Code & analysis** | **4 Argon** | — | `gemini-4-argon` | `2` (Reasoning/Code) | `0` (Deep) |
| **Detailed research** | **3.1 Pro** | — | `gemini-3.1-pro` | `3` (Pro / Advanced) | `4` (Auto) |
| **Quick answers** | **3.5 Flash-Lite** | — | `gemini-3.5-flash-lite` | `6` (Flash-Lite) | `4` (Auto) |

---

## 2. Detailed Model Specifications

### 2.1 Everyday Help: `gemini-4-hydrogen`
- **Role:** General-purpose daily driver, fast tool use, interactive chat, multi-turn conversations.
- **Backbone:** Google Gemini 4 Hydrogen architecture (1M token context, high-speed decode).
- **Aliases:** `gemini-4-hydrogen`, `gemini-hydrogen`, `gemini-4-everyday`, `gemini-everyday`.
- **Default:** This is the default model (`default_model: "gemini-4-hydrogen"`).
- **Thinking Support:** Supports adjustable thinking levels (`@think=0..4` or `reasoning_effort`).

### 2.2 Code & Analysis: `gemini-4-argon`
- **Role:** Complex programming, multi-file code architectures, mathematics, logic reasoning, and frontier analysis.
- **Backbone:** Google Gemini 4 Argon architecture (deep reasoning, long-horizon chain-of-thought).
- **Aliases:** `gemini-4-argon`, `gemini-argon`, `gemini-4-code`, `gemini-code`.
- **Default Thinking:** Operates with deep thinking (`think=0`) enabled by default (~20,000+ output tokens).
- **Thinking Support:** Highly responsive to thinking levels (`low`, `medium`, `high`).

### 2.3 Detailed Research: `gemini-3.1-pro`
- **Role:** In-depth multi-source document research, comprehensive report drafting, long-form synthesis.
- **Backbone:** Gemini 3.1 Pro tier.
- **Aliases:** `gemini-3.1-pro`, `gemini-pro`, `gemini-research`.
- **Requirement:** Authenticated routing requires a Google account with **Gemini Advanced** subscription cookies (`cookie.txt`). Without an Advanced cookie, Gemini Web automatically falls back to the Flash tier.

### 2.4 Quick Answers: `gemini-3.5-flash-lite`
- **Role:** Instant fact lookups, simple translations, low-latency summarization, lightweight API tasks.
- **Backbone:** Gemini 3.5 Flash-Lite.
- **Aliases:** `gemini-3.5-flash-lite`, `gemini-flash-lite`, `gemini-quick`.
- **Latency:** Lowest time-to-first-token (TTFT).

---

## 3. Thinking Level Configuration

The dropdown features a **"Thinking level >"** flyout submenu. In the reverse-engineered wire protocol, thinking depth is passed in payload element `inner[17] = [[think_mode]]`.

### Numerical Values
- **`0` (Deep / High):** Maximum reasoning depth, extended chain-of-thought, longest generation output.
- **`2` (Medium):** Balanced reasoning for moderate complexity tasks.
- **`4` (Low / Auto):** Default adaptive level determined automatically by Gemini upstream.

### Methods of Specifying Thinking Level

#### Method A: Model Suffix (`@think=N`)
Append `@think=N` directly to any model identifier:
```bash
# Argon with medium thinking
"model": "gemini-4-argon@think=2"

# Hydrogen with maximum deep thinking
"model": "gemini-4-hydrogen@think=0"
```

#### Method B: OpenAI Standard `reasoning_effort` Parameter
Pass the standard OpenAI parameter in your `/v1/chat/completions` request body:
```json
{
  "model": "gemini-4-argon",
  "reasoning_effort": "high",
  "messages": [{"role": "user", "content": "Write a distributed Raft consensus implementation in Rust"}]
}
```
Mapping:
- `"high"` $\rightarrow$ `think=0`
- `"medium"` $\rightarrow$ `think=2`
- `"low"` $\rightarrow$ `think=4`

---

## 4. Backward Compatibility Aliases

The API retains full backwards compatibility with legacy client identifiers:
- `gemini-3.7-flash`
- `gemini-3.6-flash`
- `gemini-3.5-flash`
- `gemini-3.5-flash-thinking`
- `gemini-3.5-flash-thinking-lite`
- `gemini-auto`
