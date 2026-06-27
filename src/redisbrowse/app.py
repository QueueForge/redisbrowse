import argparse
import sys
import redis
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label, Log
from textual.containers import Horizontal, Vertical

class RedisTUI(App):
    """A simple TUI to view Redis keys and queue messages."""
    
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

    def __init__(self, redis_client: redis.Redis, **kwargs):
        """Initialize the app with the pre-configured Redis client."""
        super().__init__(**kwargs)
        self.r = redis_client

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
            keys = self.r.keys("*")
            if not keys:
                list_view.append(ListItem(Label("[No keys found]")))
            for key in sorted(keys):
                # Create the item without an ID...
                item = ListItem(Label(key))
                # ...and store the raw key name directly as an object attribute!
                item.redis_key = key
                list_view.append(item)
        except redis.exceptions.ConnectionError:
            list_view.append(ListItem(Label("[Connection Error to Redis]")))

    def on_list_view_selected(self, message: ListView.Selected) -> None:
        """Triggered when a key is selected from the list."""
        log = self.query_one("#message-log", Log)
        log.clear()
        
        selected_item = message.item
        # Check if the item exists and contains our custom key attribute
        if not selected_item or not hasattr(selected_item, "redis_key"):
            return
        
        # Read the key name directly from the attribute
        key_name = selected_item.redis_key
        
        try:
            key_type = self.r.type(key_name)
            log.write_line(f"Key: {key_name}")
            log.write_line(f"Type: {key_type.upper()}")
            log.write_line("-" * 30)
            
            # 1. LISTS (Standard Queues)
            if key_type == "list":
                messages = self.r.lrange(key_name, 0, -1)
                log.write_line(f"Total messages: {len(messages)}")
                log.write_line("")
                for idx, msg in enumerate(messages):
                    log.write_line(f"[{idx}] {msg}")
            
            # 2. STREAMS (Append-only Logs)
            elif key_type == "stream":
                stream_entries = self.r.xrange(key_name, min='-', max='+', count=100)
                log.write_line(f"Last {len(stream_entries)} stream entries:")
                log.write_line("")
                for entry_id, entry_data in stream_entries:
                    data_str = ", ".join([f"{k}: {v}" for k, v in entry_data.items()])
                    log.write_line(f"[{entry_id}] {data_str}")

            # 3. STRINGS
            elif key_type == "string":
                val = self.r.get(key_name)
                log.write_line(str(val))
                
            # 4. SETS
            elif key_type == "set":
                members = self.r.smembers(key_name)
                log.write_line(f"Total members: {len(members)}")
                log.write_line("")
                for member in members:
                    log.write_line(f"- {member}")
            
            # 5. HASHES
            elif key_type == "hash":
                fields = self.r.hgetall(key_name)
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
    """CLI entry point accepting Redis connection arguments."""
    parser = argparse.ArgumentParser(
        description="redisbrowse - A simple TUI to browse Redis keys and queues."
    )
    parser.add_argument("-n", "--host", default="localhost", help="Redis server hostname (default: localhost)")
    parser.add_argument("-p", "--port", type=int, default=6379, help="Redis server port (default: 6379)")
    parser.add_argument("-d", "--db", type=int, default=0, help="Redis database number (default: 0)")
    parser.add_argument("-a", "--password", default=None, help="Redis server password (optional)")

    args = parser.parse_args()

    # Create the Redis client based on CLI arguments
    try:
        client = redis.Redis(
            host=args.host,
            port=args.port,
            db=args.db,
            password=args.password,
            decode_responses=True
        )
        # Fast test connection check before opening the TUI
        client.ping()
    except Exception as e:
        print(f"Error: Could not connect to Redis at {args.host}:{args.port} -> {e}", file=sys.stderr)
        sys.exit(1)

    # Boot up the app and pass the running client
    app = RedisTUI(redis_client=client)
    app.run()

if __name__ == "__main__":
    main()