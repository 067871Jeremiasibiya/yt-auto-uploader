from pytrends.request import TrendReq
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
from scripts.generate_script import generate_script
from scripts.upload_to_youtube import upload_video
from PIL import Image, ImageDraw, ImageFont
import schedule, time, os

def fetch_trend():
    pytrends = TrendReq()
    trend = pytrends.trending_searches()[0]
    return trend

def generate_audio(text):
    tts = gTTS(text)
    tts.save("output/voice.mp3")

def make_video():
    clip = VideoFileClip("assets/background.mp4").subclip(0, 60)
    audio = AudioFileClip("output/voice.mp3")
    final = clip.set_audio(audio)
    final.write_videofile("output/final.mp4", fps=24)

def make_thumbnail(topic):
    base = Image.new("RGB", (1280, 720), color="black")
    draw = ImageDraw.Draw(base)
    font = ImageFont.load_default()
    draw.text((50, 300), topic, fill="white", font=font)
    base.save("output/thumbnail.jpg")

def main():
    topic = fetch_trend()
    print("Trend:", topic)

    script = generate_script(topic)
    generate_audio(script)
    make_video()
    make_thumbnail(topic)
    upload_video("output/final.mp4", topic, script, "output/thumbnail.jpg")

schedule.every().day.at("09:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60)
