import keyboard
import socket
import threading

# 키보드 입력 수신
class KeyboardInput:             
    def __init__(self):
        self.observers = []

    def append_observer(self, observer):    # KeyboardObserver 저장
        self.observers.append(observer)     # [KeyboardObserver] 

    def noti_observers(self, v):               # 결과 전달 함수
        for observer in self.observers:
            observer.update(v)       # 출력 프로세서로 전달
            
# 증감 계산 클래스
class ValueCal:
    def __init__(self, keyboard_input) :
        self.val = 0                # 내부 값
        self.keyboard_input = keyboard_input
        
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
            self.keyboard_input.noti_observers(self.val)

# 결과 전달 클래스
class KeyboardObserver:
    def update(self, value):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 5000))
            s.sendall(str(value).encode())
            
# 
class KeyboardInputThread(threading.Thread):
    def __init__(self, value_cal):
        super().__init__()
        self.value_cal = value_cal

    def run(self):
        self.value_cal.start()

if __name__ == "__main__":
    keyboard_input = KeyboardInput()
    keyboard_observer = KeyboardObserver()
    value_cal = ValueCal(keyboard_input)
    
    keyboard_input.append_observer(keyboard_observer)   

    keyboard_thread = KeyboardInputThread(value_cal)   
    keyboard_thread.start()