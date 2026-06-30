# 🚀 redisbrowse

An elegant, minimalist Terminal User Interface (TUI) for quick Redis database inspection. With `redisbrowse`, you can instantly browse your keys, inspect connection configurations, and view the contents of Lists, Streams, Strings, Sets, and Hashes directly from your terminal.

Built with Python, [Textual](https://github.com/Textualize/textual), and [redis-py](https://github.com/redis/redis-py).

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)

## About

**RedisBrowse** is an open-source project developed and maintained by **QueueForge**. It is designed to provide a modern, simple, and intuitive terminal user interface for browsing Redis data and message queues. Learn more about QueueForge at [**https://queueforge.dev**](https://queueforge.dev?utm_source=README&utm_campaign=RedisBrowse).

---

## ✨ Features

* **⚡ Live Key Overview:** A clean list of all keys in your Redis instance on the left panel.
* **🔌 Flexible CLI Configuration:** Instantly connect to remote hosts, distinct database IDs, or password-protected servers using built-in argument parsing.
* **📦 Smart Data Type Detection:** Automatic formatting and preview based on the Redis type:
    * `LIST`: Displays all elements/messages with their index (perfect for standard queues).
    * `STREAM`: Shows the last 100 entries including entry IDs and key-value pairs.
    * `STRING`: Direct plain text value preview.
    * `SET` & `HASH`: Structured breakdown of all members, fields, and values.
* **🔄 Instant Refresh:** Refresh the key list at any time with a single keystroke.
* **🎨 Modern Interface:** Full mouse support, smooth scrolling, and keyboard shortcuts powered by Textual.

---

## 🛠️ Installation

### Install Locally for Development
Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/QueueForge/redisbrowse.git
cd redisbrowse
pip install -e .
```

---

## 🚀 Usage

Once installed, the `redisbrowse` command is available globally in your terminal.

### Connect to a local Redis instance (default)
```bash
redisbrowse
```

### Connect to a remote host
```bash
redisbrowse --host 192.168.1.100 --port 6379
```

### Connect to a specific database with a password
```bash
redisbrowse --host my-redis-server.com --db 3 --password mysecretpassword
```

---

## ⚙️ CLI Options

| Flag | Short | Default | Description |
|---|---|---|---|
| `--host` | `-n` | `localhost` | Redis server hostname or IP address |
| `--port` | `-p` | `6379` | Redis server port |
| `--db` | `-d` | `0` | Redis database number to connect to |
| `--password` | `-a` | `None` | Password for authentication (optional) |

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|---|---|
| `r` | Refresh the key list |
| `q` | Quit the application |

---

## 📦 Dependencies

* [Python 3.11+](https://www.python.org/)
* [Textual](https://github.com/Textualize/textual) — TUI framework
* [redis-py](https://github.com/redis/redis-py) — Redis client for Python

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.