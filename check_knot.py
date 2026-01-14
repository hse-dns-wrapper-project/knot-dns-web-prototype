
import os
import sys
import libknot
from libknot.control import KnotCtl

# Путь к сокету, который мы пробросили через Volume
#libknot.Knot("/usr/lib/x86_64-linux-gnu/libknot.so.15")
socket_path = os.environ.get("KNOT_SOCKET", "/app/storage/knot.sock")

def test_connection():
    ctl = KnotCtl()
    try:
        # 1. Пытаемся подключиться к сокету
        ctl.connect(socket_path)
        
        # 2. Отправляем простую команду статуса
        # Команда status возвращает блок данных
        #ctl.send_block(cmd="status")
        #resp = ctl.receive_block()
        
        print("✅ Соединение успешно!")
        #print(f"Ответ сервера: {resp}")
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        sys.exit(1)
    finally:
        ctl.close()

if __name__ == "__main__":
    test_connection()