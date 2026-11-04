
import os
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
OUT = "output"
os.makedirs(OUT, exist_ok=True)

def run(cmd):
    subprocess.run(cmd, check=True)

def get_font(size, bold=False):
    path = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
    return ImageFont.truetype(path, size)

def draw_scene(index, total, text, hero, friend):
    colors = [
        ("#91d7f2", "#74bd69"),
        ("#a6c8ff", "#6cbf84"),
        ("#f5c6aa", "#86c5a5"),
        ("#b9a7e8", "#6cae75"),
        ("#8ed1c6", "#7ab66d")
    ]

    sky, grass = colors[index % len(colors)]

    img = Image.new("RGB", (W, H), sky)
    d = ImageDraw.Draw(img)

    # Matahari
    d.ellipse((1010, 55, 1135, 180), fill="#ffe08a")

    # Awan
    for x, y in [(130, 110), (430, 75), (800, 145)]:
        d.ellipse((x, y, x+120, y+48), fill="white")
        d.ellipse((x+35, y-22, x+100, y+50), fill="white")

    # Bukit dan tanah
    d.ellipse((-180, 390, 620, 850), fill=grass)
    d.ellipse((430, 370, 1320, 850), fill="#5eaa69")
    d.rectangle((0, 560, W, H), fill="#e7c78d")

    # Rumah
    for x, col in [(80, "#f28b75"), (1020, "#f4a261")]:
        d.rectangle((x, 390, x+190, 565), fill=col)
        d.polygon(
            [(x-20, 395), (x+95, 300), (x+210, 395)],
            fill="#8d5544"
        )
        d.rectangle((x+72, 465, x+120, 565), fill="#704c3b")

    # Pohon
    for x in [260, 900]:
        d.rectangle((x, 390, x+25, 555), fill="#805438")
        d.ellipse((x-50, 320, x+75, 440), fill="#398b55")

    # Karakter kartun
    def character(cx, cy, shirt, name):
        # Kepala
        d.ellipse(
            (cx-43, cy-110, cx+43, cy-24),
            fill="#f2c49b",
            outline="#4c3b32",
            width=4
        )

        # Mata
        d.ellipse((cx-18, cy-78, cx-9, cy-68), fill="black")
        d.ellipse((cx+9, cy-78, cx+18, cy-68), fill="black")

        # Senyum
        d.arc(
            (cx-20, cy-76, cx+20, cy-42),
            10, 170,
            fill="#5a352c",
            width=4
        )

        # Badan
        d.rounded_rectangle(
            (cx-48, cy-25, cx+48, cy+105),
            radius=22,
            fill=shirt,
            outline="#4c3b32",
            width=4
        )

        # Kaki
        d.line(
            (cx-28, cy+105, cx-38, cy+165),
            fill="#394b59",
            width=15
        )
        d.line(
            (cx+28, cy+105, cx+38, cy+165),
            fill="#394b59",
            width=15
        )

        # Tangan
        d.line(
            (cx-45, cy+8, cx-82, cy+58),
            fill="#f2c49b",
            width=13
        )
        d.line(
            (cx+45, cy+8, cx+82, cy+58),
            fill="#f2c49b",
            width=13
        )

        d.text(
            (cx-45, cy+175),
            name,
            font=get_font(22, True),
            fill="#24323a"
        )

    character(520, 430, "#ef6a6a", hero)
    character(700, 430, "#477bd1", friend)

    # Label adegan
    d.rounded_rectangle(
        (55, 35, 650, 95),
        radius=18,
        fill="white"
    )

    d.text(
        (78, 50),
        f"ALEX'S STORY WORLD | ADEGAN {index+1}/{total}",
        font=get_font(23, True),
        fill="#263238"
    )

    # Kotak narasi
    d.rounded_rectangle(
        (55, 590, 1225, 690),
        radius=22,
        fill="white"
    )

    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = (line + " " + word).strip()

        if d.textbbox((0, 0), test, font=get_font(24))[2] > 1110:
            lines.append(line)
            line = word
        else:
            line = test

    if line:
        lines.append(line)

    y = 607

    for ln in lines[:3]:
        d.text(
            (82, y),
            ln,
            font=get_font(23),
            fill="#263238"
        )
        y += 30

    return img


def make_audio(text, path):
    run([
        "espeak-ng",
        "-v", "id",
        "-s", "145",
        "-a", "165",
        "-w", path,
        text
    ])


def main():
    with open("output/story.json", encoding="utf-8") as f:
        story = json.load(f)

    paragraphs = story["paragraphs"]

    # Storyboard
    with open("output/storyboard.txt", "w", encoding="utf-8") as f:
        f.write(story["title"] + "\n\n")

        for i, paragraph in enumerate(paragraphs, 1):
            f.write(f"ADEGAN {i:02d}\n")
            f.write(paragraph + "\n\n")

    clips = []

    for i, paragraph in enumerate(paragraphs):
        print(f"Membuat adegan {i+1}/{len(paragraphs)}")

        img = draw_scene(
            i,
            len(paragraphs),
            paragraph,
            story["hero"],
            story["friend"]
        )

        image_path = f"output/scene_{i:02d}.png"
        audio_path = f"output/voice_{i:02d}.wav"
        clip_path = f"output/clip_{i:02d}.mp4"

        img.save(image_path)
        make_audio(paragraph, audio_path)

        duration = float(subprocess.check_output([
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ], text=True).strip()) + 0.35

        frames = max(1, int(duration * 24))

        video_filter = (
            f"scale=1360:765,"
            f"zoompan=z='min(zoom+0.0005,1.06)':"
            f"d={frames}:s=1280x720:fps=24,"
            f"format=yuv420p"
        )

        run([
            "ffmpeg", "-y",
            "-loglevel", "error",
            "-loop", "1",
            "-i", image_path,
            "-i", audio_path,
            "-vf", video_filter,
            "-t", str(duration),
            "-r", "24",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "28",
            "-c:a", "aac",
            "-b:a", "96k",
            "-shortest",
            clip_path
        ])

        clips.append(clip_path)

    # Gabungkan semua adegan
    with open("output/concat.txt", "w") as f:
        for clip in clips:
            f.write(f"file '{os.path.basename(clip)}'\n")

    run([
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-f", "concat",
        "-safe", "0",
        "-i", "output/concat.txt",
        "-c", "copy",
        "output/alex_story_world_full.mp4"
    ])

    # Shorts vertikal 25 detik dari video utama
    run([
        "ffmpeg", "-y",
        "-loglevel", "error",
        "-ss", "0",
        "-i", "output/alex_story_world_full.mp4",
        "-t", "25",
        "-vf",
        "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "28",
        "-c:a", "aac",
        "-b:a", "96k",
        "output/alex_story_world_shorts.mp4"
    ])

    print("SEMUA VIDEO BERHASIL DIBUAT!")


if __name__ == "__main__":
    main()
