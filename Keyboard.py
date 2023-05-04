import keyboard
import socket
import threading

# 키보드 입력 수신 클래스
class KeyboardInput:             
    def __init__(self):
        self.val = 0                # 내부 값
        self.observers = []

    def append_observer(self, observer):    # KeyboardObserver.update() 저장
        self.observers.append(observer)     # [KeyboardObserver.update()] 

    def noti_observers(self):               # 결과 전달 함수
        for observer in self.observers:
            observer.update(self.val)       # 출력 프로세서로 전달
            
    def start(self):                # 증감 계산 실행
        while True:
            event = keyboard.read_event()
            if event.name == "up":
                if event.event_type == "down" :
                    self.val += 1
            elif event.name == "down":
                if event.event_type == "down" :
                    self.val -= 1
            else :
                continue
            
            self.noti_observers()
            
# 키보드 입력 수신 스레드 
class KeyboardInputThread(threading.Thread):
    def __init__(self, keyboard_input):
        super().__init__()
        self.keyboard_input = keyboard_input

    def run(self):
        self.keyboard_input.start()

# 옵저버 소켓 통신
class KeyboardObserver:
    def update(self, value):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 5000))
            s.sendall(str(value).encode())


if __name__ == "__main__":
    keyboard_input = KeyboardInput()
    keyboard_observer = KeyboardObserver()
    keyboard_input.append_observer(keyboard_observer)   

    keyboard_thread = KeyboardInputThread(keyboard_input)   
    keyboard_thread.start()