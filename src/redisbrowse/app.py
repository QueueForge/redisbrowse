import redis
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label, Log
from textual.containers import Horizontal, Vertical

# Verbindung zum lokalen Redis-Server (Standardports)
try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
except Exception as e:
    print(f"Could not connect to Redis: {e}")

class RedisTUI(App):
    """A simple English TUI to view Redis keys and queue messages."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    Horizontal {
        height: 1fr;
    }
    Vertical {
        width: 40%;
        border-right: solid $accent;
    }
    #details-panel {
        width: 60%;
        padding: 1;
    }
    ListItem {
        padding: 1;
    }
    Label {
        margin-bottom: 1;
        text-style: bold;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh Keys")
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical():
                yield Label("🔑 Redis Keys / Queues:")
                yield ListView(id="keys-list")
            with Vertical(id="details-panel"):
                yield Label("📜 Content / Messages:")
                yield Log(id="message-log")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app starts."""
        self.title = "Redis Simple Queue Viewer"
        self.refresh_keys()

    def refresh_keys(self) -> None:
            """Fetch all keys from Redis and populate the list."""
            list_view = self.query_one("#keys-list", ListView)
            list_view.clear()
            
            try:
                keys = r.keys("*")
                if not keys:
                    list_view.append(ListItem(Label("[No keys found]")))
                for key in sorted(keys):
                    # Wir erstellen das Item OHNE ID...
                    item = ListItem(Label(key))
                    # ...und speichern den echten Key-Namen einfach direkt im Objekt!
                    item.redis_key = key
                    list_view.append(item)
            except redis.exceptions.ConnectionError:
                list_view.append(ListItem(Label("[Connection Error to Redis]")))

    def on_list_view_selected(self, message: ListView.Selected) -> None:
        """Triggered when a key is selected from the list."""
        log = self.query_one("#message-log", Log)
        log.clear()
        
        selected_item = message.item
        # Prüfen, ob das Item existiert und ob unser selbstgebautes Attribut da ist
        if not selected_item or not hasattr(selected_item, "redis_key"):
            return
        
        # Direkt den Namen aus dem Attribut lesen (kein .replace() mehr nötig)
        key_name = selected_item.redis_key
        
        try:
            key_type = r.type(key_name)
            log.write_line(f"Key: {key_name}")
            log.write_line(f"Type: {key_type.upper()}")
            log.write_line("-" * 30)
            
            # 1. LISTS (Standard Queues)
            if key_type == "list":
                messages = r.lrange(key_name, 0, -1)
                log.write_line(f"Total messages: {len(messages)}")
                log.write_line("")
                for idx, msg in enumerate(messages):
                    log.write_line(f"[{idx}] {msg}")
            
            # 2. STREAMS (Append-only Logs)
            elif key_type == "stream":
                stream_entries = r.xrange(key_name, min='-', max='+', count=100)
                log.write_line(f"Last {len(stream_entries)} stream entries:")
                log.write_line("")
                for entry_id, entry_data in stream_entries:
                    data_str = ", ".join([f"{k}: {v}" for k, v in entry_data.items()])
                    log.write_line(f"[{entry_id}] {data_str}")

            # 3. STRINGS
            elif key_type == "string":
                val = r.get(key_name)
                log.write_line(str(val))
                
            # 4. SETS
            elif key_type == "set":
                members = r.smembers(key_name)
                log.write_line(f"Total members: {len(members)}")
                log.write_line("")
                for member in members:
                    log.write_line(f"- {member}")
            
            # 5. HASHES
            elif key_type == "hash":
                fields = r.hgetall(key_name)
                log.write_line(f"Total fields: {len(fields)}")
                log.write_line("")
                for field, val in fields.items():
                    log.write_line(f"{field}: {val}")
                    
            else:
                log.write_line(f"[Unsupported type '{key_type}' for preview]")
                
        except Exception as e:
            log.write_line(f"Error fetching data: {e}")
    def action_refresh(self) -> None:
        """Action for the 'r' key binding."""
        self.refresh_keys()


def main():
    """Einstiegspunkt für das Konsolen-Kommando."""
    app = RedisTUI()
    app.run()

if __name__ == "__main__":
    main()