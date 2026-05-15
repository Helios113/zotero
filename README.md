# Zotero — Self-Hosted TTS Fork

This is a fork of [Zotero](https://www.zotero.org/) that adds a **Self-Hosted** Read Aloud tier, allowing you to use a local [Kokoro TTS](https://github.com/hexgrad/kokoro) server instead of Zotero's cloud voices. No account, no internet, no cost.

The companion server package is [zotero-kokoro-server](https://github.com/helios113/zotero-kokoro-server) (`pip install zotero-kokoro-server`).

---

## Building from Source (macOS)

### Prerequisites

- **Node.js** 18+ — install via [nodejs.org](https://nodejs.org/) or `brew install node`
- **Python 3** — comes with macOS, or `brew install python`
- **Git** with submodule support

### 1. Clone the repo

```bash
git clone --recurse-submodules https://github.com/Helios113/zotero.git
cd zotero
```

If you already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

### 2. Install dependencies

```bash
npm install
cd reader && npm install && cd ..
```

### 3. Build

```bash
npm run build-app
```

This does everything in one shot:
- Compiles the reader (webpack)
- Transpiles JS/JSX and compiles SCSS
- Packages it all into `app/staging/Zotero.app`

First build takes ~2–3 minutes. Subsequent builds are faster.

### 4. Run

```bash
npm run run-app
```

Or double-click `app/staging/Zotero.app`.

---

## Setting Up the Kokoro TTS Server

### 1. Install

```bash
pip install zotero-kokoro-server
```

Requires Python 3.10–3.12.

### 2. Start the server

```bash
zotero-kokoro-server
```

The first run downloads the Kokoro model weights (~300 MB) from Hugging Face. After that it works fully offline.

Open **http://localhost:8880** in your browser to access the voice playground and settings UI.

### 3. Configure Zotero

In the built Zotero app, open **Edit → Preferences → General** and scroll to **Read Aloud — Self-Hosted Server**. The URL defaults to `http://127.0.0.1:8880` — leave it as-is if you're running the server locally.

Then open any PDF in the Reader, click the **Read Aloud** button, expand the options panel, and select **Self-Hosted** from the Voice Mode dropdown.

---

## Rebuilding after changes

```bash
npm run build-app && npm run run-app
```

If you only changed non-reader JS/CSS (i.e. nothing inside `reader/src/`), you can skip the reader webpack step for a faster build — but `build-app` is always safe to run in full.

---

[![CI](https://github.com/zotero/zotero/actions/workflows/ci.yml/badge.svg)](https://github.com/zotero/zotero/actions/workflows/ci.yml)
