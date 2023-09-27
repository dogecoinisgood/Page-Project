# 使用python-embed版時要加這2行
import sys, os, time, re
sys.path.append(os.path.dirname(__file__))

from pytube import YouTube
from pydub import AudioSegment
from pydub.utils import get_array_type
import numpy as np
import io, datetime, whisper, os
from db import *


# base_path= "/content/drive/Mydrive/.../page-Project/crawler"
base_path= os.path.abspath(os.path.dirname(__file__))



# pytube無法解析串流解決補釘
import mock
from pytube.cipher import get_throttling_function_code
def patched_throttling_plan(js: str):
    """Patch throttling plan, from https://github.com/pytube/pytube/issues/1498"""
    raw_code = get_throttling_function_code(js)

    transform_start = r"try{"
    plan_regex = re.compile(transform_start)
    match = plan_regex.search(raw_code)

    #transform_plan_raw = find_object_from_startpoint(raw_code, match.span()[1] - 1)
    transform_plan_raw = js

    # Steps are either c[x](c[y]) or c[x](c[y],c[z])
    step_start = r"c\[(\d+)\]\(c\[(\d+)\](,c(\[(\d+)\]))?\)"
    step_regex = re.compile(step_start)
    matches = step_regex.findall(transform_plan_raw)
    transform_steps = []
    for match in matches:
        if match[4] != '':
            transform_steps.append((match[0],match[1],match[4]))
        else:
            transform_steps.append((match[0],match[1]))
    return transform_steps



def getTextFromYtUrl(url):
    # 計算時間用1
    startTime= datetime.datetime.now()
    
    # pytube無法解析串流解決方案(套用前面的補釘function)
    with mock.patch("pytube.cipher.get_throttling_plan", patched_throttling_plan):
        youtube= YouTube(url)
        audio= youtube.streams.filter(only_audio=True).first()

    # 下載成檔案(測試用)
    # out_file= audio.download()
    # fileName= os.path.splitext(out_file)
    # os.rename(out_file, "audio.mp3")

    # 將下載的串流轉為bytes物件
    bufferObj= io.BytesIO()
    audio.stream_to_buffer(bufferObj)
    # 將讀取記憶體的指標設回到可供讀取的預設位置(因為pytube的stream_to_buffer沒有寫上這個應該要有的功能，在此補上)
    bufferObj.seek(0)

    # 計算時間用2
    downloadTime= datetime.datetime.now()

    # 新增pydub要用的ffmpeg的路徑
    os.environ['PATH'] += ';'+os.path.abspath(os.path.dirname(__file__)+'/data/ffmpeg/')

    audio = AudioSegment.from_file(bufferObj)

    # 從下載下來的檔案讀取(測試用)
    # audio = AudioSegment.from_file("audio.wav")

    # 16-bit(2bytes) pytube下載下來的貌似原本就是16bit的格式，可以省略
    # audio = audio.set_sample_width(2)
    # resampling 重設取樣率，whisper預設是以16000進行辨識
    audio = audio.set_frame_rate(16000)
    # 設定聲音為單聲道，避免雙聲道時，模型將雙聲道的編碼誤認為是一個雙倍長度的單聲道編碼
    audio= audio.set_channels(1)

    dtype = get_array_type(audio.sample_width * 8)
    # 轉換成np_array
    audio = np.frombuffer(audio.raw_data, dtype=dtype).astype(np.float32) / 32768.0

    # 將現在的音檔匯出成mp3(測試用)
    # audio.export("audio2.mp3", format="mp3")

    model = whisper.load_model('tiny', download_root=base_path+'/data/whisper_model') #, device="cuda")
    # result = model.transcribe(audio, language='zh', initial_prompt='請以專業美妝部落客的身分，給我繁體中文的語音辨識')
    result = model.transcribe(audio, language='zh', initial_prompt='請給我繁體中文的語音辨識 海綿寶寶 派大星 章魚哥 野海熊 海犀牛')

    print("下載轉檔: ", (downloadTime-startTime).seconds, "秒\t文字轉換: ", (datetime.datetime.now()-downloadTime).seconds, "秒")
    return result["text"]





# data= getData("youtube", "SELECT id,link,videoContent FROM youtube")
# for row in data:
#     row_id,link,videoContent= row
#     if not videoContent:
#         print(row_id, link)
#         updateData("youtube", {"videoContent":getTextFromYtUrl(link)}, row_id)

print(getTextFromYtUrl("https://www.youtube.com/watch?v=aL9odRg3hyA"))