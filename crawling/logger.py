
import logging
import datetime

# Configure the root logger
def setLogOptions():
    now = datetime.datetime.now() # 프로그램 실행 시각 저장
    caller_name = logging.Logger.findCaller(self=debug)[2] # 호출자 정보 추출. (파일 이름, 행 번호, 함수 이름, 스택 정보)의 튜플 형식으로 반환됨.
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=f'.\\log\\{caller_name}_{now.date()}_{now.hour}h_{now.minute}m.log',  # Specify the file name for file-based logging (optional)
    )

    
    # Adding a console handler to display logs on the console as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Set the desired logging level for the console handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Attach the console handler to the root logger
    logging.getLogger('').addHandler(console_handler)

def debug(data):
    setLogOptions()
    logging.debug(data)