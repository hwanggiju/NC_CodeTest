import keyboard
import socket
import threading

# 키보드 입력 수신 클래스
class KeyboardInput:
    def __init__(self, keyboard_cal) :
        self.keyboard_cal = keyboard_cal

    def start(self):
        while True:
            event = keyboard.read_event()                       # 키보드 입력 수신
            self.keyboard_cal.cal(event)
          
# 증감 계산 클래스
class keyboardCal:
    def __init__(self, result_send) :
        self.val = 0                        
        self.result_send = result_send
        
    def cal(self, event):                        
        if event.name == "up":
            if event.event_type == "down" :
                self.val += 1
                self.result_send.noti_observers(self.val)       # 변경 사항 소켓에 알림
                
        elif event.name == "down":
            if event.event_type == "down" :
                self.val -= 1
                self.result_send.noti_observers(self.val)       # 변경 사항 소켓에 알림

        else :                                                  # 나머지 키보드 입력은 무시
            pass

# 결과 전달 클래스
class resultSend:
    def __init__(self) :
        self.observers = [] 

    def append_observer(self, observer):    
        self.observers.append(observer)                         # 소켓 저장
    
    def noti_observers(self, v):            
        for observer in self.observers:
            observer.update(v)                                  # 소켓에 변경 사항 넣어 display로 전달  

# 정보 전달 옵저버
class KeyboardObserver:
    def update(self, value):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 5000))                      
            s.sendall(str(value).encode())                      
            
# 쓰레드 구성
class KeyboardInputThread(threading.Thread):
    def __init__(self, keyboard_input):
        super().__init__()
        self.keyboard_input = keyboard_input

    def run(self):
        self.keyboard_input.start()                             # keyboard_input.start() while 문 실행하면서 다른 프로세스 동시 실행

# 동작
if __name__ == "__main__":
    result_send = resultSend()                                  # 결과 전달
    keyboard_cal = keyboardCal(result_send)                     # 증감 계산
    keyboard_input = KeyboardInput(keyboard_cal)                # 키보드 입력 수신
    
    keyboard_observer = KeyboardObserver()                      # 옵저버
    result_send.append_observer(keyboard_observer)              # tcp 소켓 저장          

    keyboard_thread = KeyboardInputThread(keyboard_input)       # 쓰레드
    keyboard_thread.start()