# 🚀 redisbrowse

An elegant, minimalist Terminal User Interface (TUI) for quick Redis database inspection. With `redisbrowse`, you can instantly browse your keys and inspect the contents of Lists, Streams, Strings, Sets, and Hashes right from your terminal.

Built with Python, [Textual](https://github.com/Textualize/textual), and [redis-py](https://github.com/redis/redis-py).

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)

---

## ✨ Features

*   **⚡ Live Key Overview:** A clean list of all keys in your Redis instance on the left panel.
*   **📦 Smart Data Type Detection:** Automatic formatting and preview based on the Redis type:
    *   `LIST`: Displays all elements/messages with their index (perfect for standard queues).
    *   `STREAM`: Shows the last 100 entries including entry IDs and key-value pairs.
    *   `STRING`: Direct plain text value preview.
    *   `SET` & `HASH`: Structured breakdown of all members, fields, and values.
*   **🔄 Instant Refresh:** Refresh the key list at any time with a single keystroke.
*   **🎨 Modern Interface:** Full mouse support, smooth scrolling, and keyboard shortcuts powered by Textual.

---

## 🛠️ Installation

### Install Locally for Development
Clone the repository (or navigate to your project directory) and install the package in editable mode:

```bash
git clone [https://github.com/QueueForge/redisbrowse.git](https://github.com/QueueForge/redisbrowse.git)
cd redisbrowse
pip install -e .