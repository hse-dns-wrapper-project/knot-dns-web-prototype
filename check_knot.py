
import os
import sys
import libknot
from libknot.control import KnotCtl

socket_path = os.environ.get("KNOT_SOCKET", "/run/knot/knot.sock")
print(socket_path)

def test_connection():
    ctl = KnotCtl()
    try:
        ctl.connect(socket_path)
        print("✅ Соединение успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        sys.exit(1)
    finally:
        ctl.close()

if __name__ == "__main__":
    test_connection()