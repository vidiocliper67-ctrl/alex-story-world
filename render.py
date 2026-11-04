import os
import json
import random
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# ALEX'S STORY WORLD - CARTOON RENDERER V2
# ==========================================

WIDTH = 1280
HEIGHT = 720
FPS = 24

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

# ==========================================
# FONT
# ==========================================

def get_font(size, bold=False):
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    if os.path.exists(path):
        return ImageFont.truetype(path, size)

    return ImageFont.load_default()


# ==========================================
# FFMPEG HELPER
# ==========================================

def run(command):
    subprocess.run(command, check=True)


def get_duration(audio):
    result = subprocess.check_output([
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio)
    ], text=True)

    return float(result.strip()) + 0.5


# ==========================================
# TEXT WRAPPER
# ==========================================

def wrap_text(draw, text, font, max_width):
    words = text.split()

    lines = []
    current = ""

    for word in words:

        test = (current + " " + word).strip()

        width = draw.textbbox(
            (0, 0),
            test,
            font=font
        )[2]

        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


# ==========================================
# BACKGROUND
# ==========================================

def draw_background(draw, scene_type, index):

    sky_top = (120, 190, 235)
    sky_bottom = (225, 242, 247)

    for y in range(HEIGHT):

        ratio = y / HEIGHT

        color = tuple(
            int(sky_top[i] * (1 - ratio) +
                sky_bottom[i] * ratio)
            for i in range(3)
        )

        draw.line(
            (0, y, WIDTH, y),
            fill=color
        )

    # Matahari
    draw.ellipse(
        (1040, 55, 1155, 170),
        fill="#ffdb70"
    )

    # Awan
    for x, y in [(100, 100), (780, 120)]:

        draw.ellipse(
            (x, y + 15, x + 100, y + 60),
            fill="white"
        )

        draw.ellipse(
            (x + 25, y, x + 80, y + 60),
            fill="white"
        )

        draw.ellipse(
            (x + 55, y + 15, x + 125, y + 60),
            fill="white"
        )

    # Tanah
    draw.rectangle(
        (0, 530, WIDTH, HEIGHT),
        fill="#78b978"
    )

    # Bukit
    draw.ellipse(
        (-150, 390, 600, 760),
        fill="#6aaf75"
    )

    draw.ellipse(
        (550, 400, 1450, 780),
        fill="#559e65"
    )

    if scene_type == "river":

        draw.rectangle(
            (0, 430, WIDTH, 570),
            fill="#55b6d5"
        )

        for y in [460, 505, 545]:

            for x in range(30, WIDTH, 160):

                draw.arc(
                    (x, y, x + 90, y + 25),
                    0, 180,
                    fill="#d9f5ff",
                    width=4
                )

        # Sampah jika ada di naskah
        if index % 2 == 0:

            for x, y in [(400, 480), (800, 525)]:

                draw.rectangle(
                    (x, y, x + 38, y + 24),
                    fill="#f3a65a",
                    outline="#6b4934",
                    width=2
                )

    elif scene_type == "library":

        draw.rectangle(
            (110, 190, 1170, 550),
            fill="#a56d45",
            outline="#5a4030",
            width=7
        )

        for y in [285, 390, 495]:

            draw.rectangle(
                (140, y, 1140, y + 15),
                fill="#f1d49b"
            )

            for x in range(170, 1100, 80):

                color = random.choice([
                    "#d86f5d",
                    "#e6bb55",
                    "#6c9cbd",
                    "#8b78bd"
                ])

                draw.rectangle(
                    (x, y - 65, x + 48, y),
                    fill=color,
                    outline="#543c33",
                    width=2
                )

    elif scene_type == "mystery":

        # Kotak misterius
        draw.rounded_rectangle(
            (500, 390, 790, 590),
            radius=20,
            fill="#a96f42",
            outline="#533c2e",
            width=8
        )

        draw.rectangle(
            (620, 390, 670, 590),
            fill="#e4bd65"
        )

        draw.ellipse(
            (625, 465, 665, 505),
            fill="#f9df86",
            outline="#533c2e",
            width=3
        )

    elif scene_type == "bird":

        # Pohon tempat burung
        draw.rectangle(
            (990, 310, 1020, 570),
            fill="#80543c"
        )

        draw.ellipse(
            (900, 250, 1100, 410),
            fill="#3e8c59"
        )

        # Burung
        draw.ellipse(
            (1040, 280, 1100, 330),
            fill="#e6a84c",
            outline="#5a4632",
            width=3
        )

        draw.ellipse(
            (1080, 290, 1090, 300),
            fill="black"
        )

        draw.polygon(
            [(1100, 300), (1125, 310), (1100, 318)],
            fill="#ed8a43"
        )

    else:

        # Rumah desa
        draw_house(
            draw,
            90,
            320,
            "#f1a17e"
        )

        draw_house(
            draw,
            1000,
            340,
            "#f3cf77"
        )


# ==========================================
# HOUSE
# ==========================================

def draw_house(draw, x, y, color):

    draw.rectangle(
        (x, y + 65, x + 170, y + 190),
        fill=color,
        outline="#634b45",
        width=4
    )

    draw.polygon(
        [
            (x - 15, y + 70),
            (x + 85, y),
            (x + 185, y + 70)
        ],
        fill="#8e594d",
        outline="#634b45"
    )

    draw.rectangle(
        (x + 68, y + 115, x + 110, y + 190),
        fill="#80543c",
        outline="#634b45",
        width=3
    )

    draw.rectangle(
        (x + 20, y + 90, x + 55, y + 130),
        fill="#bfe8f4",
        outline="#634b45",
        width=3
    )

    draw.rectangle(
        (x + 125, y + 90, x + 155, y + 130),
        fill="#bfe8f4",
        outline="#634b45",
        width=3
    )


# ==========================================
# CHARACTER DESIGN
# ==========================================

def draw_character(
    draw,
    x,
    y,
    name,
    shirt,
    hair,
    accessory
):

    skin = "#f2c49b"

    # Bayangan
    draw.ellipse(
        (x - 55, y + 174, x + 55, y + 198),
        fill="#52705a"
    )

    # Kaki
    draw.line(
        (x - 20, y + 128, x - 27, y + 180),
        fill="#344054",
        width=17
    )

    draw.line(
        (x + 20, y + 128, x + 27, y + 180),
        fill="#344054",
        width=17
    )

    # Sepatu
    draw.ellipse(
        (x - 48, y + 169, x - 8, y + 190),
        fill="#29364b"
    )

    draw.ellipse(
        (x + 8, y + 169, x + 48, y + 190),
        fill="#29364b"
    )

    # Badan
    draw.rounded_rectangle(
        (x - 54, y + 55, x + 54, y + 145),
        radius=28,
        fill=shirt,
        outline="#29364b",
        width=4
    )

    # Tangan
    draw.line(
        (x - 43, y + 75, x - 76, y + 128),
        fill=shirt,
        width=20
    )

    draw.line(
        (x + 43, y + 75, x + 76, y + 128),
        fill=shirt,
        width=20
    )

    draw.ellipse(
        (x - 85, y + 119, x - 67, y + 137),
        fill=skin
    )

    draw.ellipse(
        (x + 67, y + 119, x + 85, y + 137),
        fill=skin
    )

    # Leher
    draw.rectangle(
        (x - 14, y + 40, x + 14, y + 67),
        fill=skin
    )

    # Kepala
    draw.ellipse(
        (x - 48, y - 20, x + 48, y + 75),
        fill=skin,
        outline="#29364b",
        width=4
    )

    # Rambut
    draw.pieslice(
        (x - 51, y - 30, x + 51, y + 48),
        180,
        360,
        fill=hair,
        outline="#29364b",
        width=3
    )

    draw.ellipse(
        (x - 49, y + 1, x - 26, y + 32),
        fill=hair
    )

    # Alis
    draw.line(
        (x - 27, y + 20, x - 12, y + 17),
        fill="#382b29",
        width=4
    )

    draw.line(
        (x + 12, y + 17, x + 27, y + 20),
        fill="#382b29",
        width=4
    )

    # Mata
    draw.ellipse(
        (x - 24, y + 25, x - 13, y + 39),
        fill="#222222"
    )

    draw.ellipse(
        (x + 13, y + 25, x + 24, y + 39),
        fill="#222222"
    )

    # Senyum
    draw.arc(
        (x - 17, y + 35, x + 17, y + 58),
        5,
        175,
        fill="#9c4e45",
        width=3
    )

    # Aksesori pembeda
    if accessory == "cap":

        draw.arc(
            (x - 45, y - 25, x + 45, y + 28),
            180,
            360,
            fill="#f5d36d",
            width=15
        )

        draw.line(
            (x - 45, y + 2, x + 45, y + 2),
            fill="#f5d36d",
            width=8
        )

    elif accessory == "bow":

        draw.polygon(
            [
                (x - 45, y - 8),
                (x - 68, y - 22),
                (x - 65, y + 4)
            ],
            fill="#f06f9b"
        )

        draw.polygon(
            [
                (x - 45, y - 8),
                (x - 23, y - 22),
                (x - 25, y + 4)
            ],
            fill="#f06f9b"
        )

    # Label nama
    draw.rounded_rectangle(
        (x - 62, y + 202, x + 62, y + 236),
        radius=12,
        fill="#fff7e8",
        outline="#29364b",
        width=2
    )

    label_font = get_font(16, True)

    text_width = draw.textbbox(
        (0, 0),
        name,
        font=label_font
    )[2]

    draw.text(
        (x - text_width / 2, y + 208),
        name,
        font=label_font,
        fill="#263044"
    )


# ==========================================
# DETECT SCENE FROM STORY
# ==========================================

def detect_scene(text, index):

    text = text.lower()

    if any(word in text for word in [
        "sungai", "air", "sampah", "bersih"
    ]):
        return "river"

    if any(word in text for word in [
        "burung", "sarang", "hewan"
    ]):
        return "bird"

    if any(word in text for word in [
        "kotak", "misteri", "pesan"
    ]):
        return "mystery"

    if any(word in text for word in [
        "perpustakaan", "buku", "peta"
    ]):
        return "library"

    return "village"


# ==========================================
# BUILD SCENE
# ==========================================

def create_scene(
    text,
    index,
    total,
    hero,
    friend
):

    random.seed(index + 100)

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT)
    )

    draw = ImageDraw.Draw(image)

    scene_type = detect_scene(text, index)

    draw_background(
        draw,
        scene_type,
        index
    )

    # Header
    draw.rounded_rectangle(
        (35, 25, 850, 82),
        radius=16,
        fill="#fffaf0",
        outline="#263044",
        width=2
    )

    draw.text(
        (58, 40),
        f"ALEX'S STORY WORLD  |  ADEGAN {index + 1}/{total}",
        font=get_font(23, True),
        fill="#263044"
    )

    # Karakter utama
    draw_character(
        draw,
        470,
        300,
        hero,
        "#ed6b62",
        "#50362f",
        "cap"
    )

    draw_character(
        draw,
        700,
        300,
        friend,
        "#4d85d8",
        "#3d302b",
        "bow"
    )

    # Narasi
    draw.rounded_rectangle(
        (35, 600, 1245, 695),
        radius=20,
        fill="#fffaf0",
        outline="#263044",
        width=2
    )

    lines = wrap_text(
        draw,
        text,
        get_font(22, True),
        1140
    )

    for i, line in enumerate(lines[:2]):

        draw.text(
            (65, 617 + i * 31),
            line,
            font=get_font(22, True),
            fill="#263044"
        )

    # Nomor adegan
    draw.ellipse(
        (1160, 105, 1220, 165),
        fill="#fffaf0",
        outline="#263044",
        width=3
    )

    draw.text(
        (1178, 120),
        str(index + 1),
        font=get_font(25, True),
        fill="#263044"
    )

    return image


# ==========================================
# RENDER ONE SCENE
# ==========================================

def render_clip(
    image_path,
    audio_path,
    output_path,
    duration,
    index
):

    frames = max(
        FPS,
        int(duration * FPS)
    )

    if index % 2 == 0:
        zoom = "min(zoom+0.00045,1.055)"
    else:
        zoom = "min(zoom+0.00035,1.045)"

    video_filter = (
        "scale=1408:792,"
        f"zoompan=z='{zoom}':"
        f"d={frames}:"
        "x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)':"
        f"s={WIDTH}x{HEIGHT}:"
        f"fps={FPS},"
        "format=yuv420p"
    )

    run([
        "ffmpeg",
        "-y",
        "-loglevel", "error",

        "-loop", "1",
        "-i", str(image_path),

        "-i", str(audio_path),

        "-vf", video_filter,

        "-t", str(duration),
        "-r", str(FPS),

        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "21",

        "-c:a", "aac",
        "-b:a", "128k",

        "-shortest",

        str(output_path)
    ])


# ==========================================
# MAIN RENDER ENGINE
# ==========================================

def main():

    story_file = OUTPUT / "story.json"

    if not story_file.exists():
        raise FileNotFoundError(
            "output/story.json tidak ditemukan. Jalankan story_engine.py dahulu."
        )

    with open(
        story_file,
        "r",
        encoding="utf-8"
    ) as file:

        story = json.load(file)

    paragraphs = story.get("paragraphs", [])

    if not paragraphs:
        raise ValueError(
            "Naskah tidak memiliki bagian paragraphs."
        )

    hero = story.get("hero", "Alex")
    friend = story.get("friend", "Luna")

    title = story.get(
        "title",
        "Petualangan ALEX'S STORY WORLD"
    )

    clips = []
    storyboard = []

    total = len(paragraphs)

    for index, paragraph in enumerate(paragraphs):

        print(
            f"Membuat adegan {index + 1}/{total}"
        )

        image_file = OUTPUT / f"scene_{index:02d}.png"
        audio_file = OUTPUT / f"voice_{index:02d}.wav"
        clip_file = OUTPUT / f"clip_{index:02d}.mp4"

        # Buat ilustrasi adegan
        image = create_scene(
            paragraph,
            index,
            total,
            hero,
            friend
        )

        image.save(image_file)

        # Buat narasi lokal
        run([
            "espeak-ng",
            "-v", "id",
            "-s", "138",
            "-p", "48",
            "-a", "165",
            "-w", str(audio_file),
            paragraph
        ])

        duration = get_duration(audio_file)

        # Render adegan dengan FFmpeg
        render_clip(
            image_file,
            audio_file,
            clip_file,
            duration,
            index
        )

        clips.append(clip_file)

        storyboard.append(
            f"ADEGAN {index + 1:02d}\n"
            f"NARASI: {paragraph}\n"
            f"VISUAL: {detect_scene(paragraph, index)}\n"
        )

    # Simpan storyboard
    with open(
        OUTPUT / "storyboard.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(title + "\n\n")

        file.write(
            "\n".join(storyboard)
        )

    # Gabungkan seluruh adegan
    concat_file = OUTPUT / "concat.txt"

    with open(
        concat_file,
        "w",
        encoding="utf-8"
    ) as file:

        for clip in clips:

            file.write(
                f"file '{clip.name}'\n"
            )

    full_video = OUTPUT / "alex_story_world_full.mp4"

    run([
        "ffmpeg",
        "-y",
        "-loglevel", "error",

        "-f", "concat",
        "-safe", "0",

        "-i", str(concat_file),

        "-c", "copy",

        str(full_video)
    ])

    # Buat video vertikal Shorts 25 detik
    shorts_video = OUTPUT / "alex_story_world_shorts.mp4"

    run([
        "ffmpeg",
        "-y",
        "-loglevel", "error",

        "-i", str(full_video),

        "-t", "25",

        "-vf",
        "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",

        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",

        "-c:a", "aac",
        "-b:a", "128k",

        str(shorts_video)
    ])

    print("================================")
    print("PRODUKSI VIDEO SELESAI")
    print("Video utama:", full_video)
    print("Video Shorts:", shorts_video)
    print("================================")


if __name__ == "__main__":
    main()
