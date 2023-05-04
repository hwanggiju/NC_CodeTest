import socket
import threading

# 결과 수신
class DisplayOutput:         
    def __init__(self):
        self.observers = []

    def append_observer(self, observer):        # DisplayObserver.update() 저장
        self.observers.append(observer)         # [DisplayObserver.update()]

    def noti_observers(self, value):
        for observer in self.observers:
            observer.update(value)              # 콘솔창 화면 출력

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 5000))
            s.listen()                          # 입력 프로세서 증감 결과 수신 대기
            while True:
                conn, _ = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if not data:
                        continue
                    value = int(data.decode())
                    self.noti_observers(value)


class DisplayOutputThread(threading.Thread):
    def __init__(self, display_output):
        super().__init__()
        self.display_output = display_output

    def run(self):
        self.display_output.start()

# 화면 출력
class DisplayObserver:
    def update(self, value):
        print(f"Value: {value}")


if __name__ == "__main__":
    display_output = DisplayOutput()
    display_observer = DisplayObserver()
    display_output.append_observer(display_observer)

    display_thread = DisplayOutputThread(display_output)
    display_thread.start()

