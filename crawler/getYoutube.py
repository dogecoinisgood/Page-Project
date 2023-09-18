from pytube import YouTube
from pydub import AudioSegment
from pydub.utils import get_array_type
import numpy as np
import io, datetime, whisper, os





# 計算時間用1
startTime= datetime.datetime.now()

url= "https://www.youtube.com/watch?v=aL9odRg3hyA"
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

model = whisper.load_model('tiny', download_root='data/whisper_model', device="cuda")
result = model.transcribe(audio, language='zh', initial_prompt='請給我繁體中文的語音辨識')



print(result["text"])

print("下載轉檔: ", (downloadTime-startTime).seconds, "秒\t文字轉換: ", (datetime.datetime.now()-downloadTime).seconds, "秒")
