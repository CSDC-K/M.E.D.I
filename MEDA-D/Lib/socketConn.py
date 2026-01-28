import socket

class TryConn:
    def __init__(self) -> None:
        pass
    def connS(self) -> str:
        self.sock = None
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(2)
            self.sock.connect(("google.com", 80))
            return "Aktif"
        except Exception as e:
            print(f"Error: {e}")
            return "Kapalı"
        finally:
            if self.sock:
                self.sock.close()