
import random
import json
import os
from datetime import datetime

os.makedirs("output", exist_ok=True)

def make_story():
    rng = random.Random()
    hero = rng.choice(["Alex", "Milo", "Nara", "Bima"])
    friend = rng.choice(["Luna", "Raka", "Tara", "Dino"])

    situations = [
        ("menemukan sebuah kotak misterius di taman",
         "kotak itu ternyata berisi pesan penting untuk warga desa"),
        ("melihat sungai yang dipenuhi sampah",
         "mereka sadar sungai itu adalah sumber air bagi banyak hewan"),
        ("mendengar tangisan dari balik semak",
         "mereka menemukan seekor anak burung yang terjatuh"),
        ("menemukan peta tua di perpustakaan",
         "peta itu menunjukkan jalan menuju pohon harapan"),
        ("melihat rumah warga yang rusak karena hujan",
         "mereka menyadari bahwa warga tersebut membutuhkan bantuan")
    ]

    problem, reveal = rng.choice(situations)

    lessons = [
        "Kebaikan kecil dapat membawa perubahan besar.",
        "Keberanian bukan berarti tidak merasa takut, tetapi tetap melakukan hal yang benar.",
        "Persahabatan menjadi kuat ketika kita saling membantu.",
        "Masalah akan terasa lebih ringan jika diselesaikan bersama.",
        "Jangan pernah meremehkan kekuatan sebuah kebaikan."
    ]

    title = rng.choice([
        "Petualangan Kecil Alex",
        "Rahasia di Desa Ceria",
        "Misi Persahabatan",
        "Keajaiban Sebuah Kebaikan",
        "Petualangan yang Tak Terlupakan"
    ])

    paragraphs = [
        f"Di sebuah desa yang indah, hiduplah seorang anak bernama {hero}. Ia adalah anak yang penuh rasa ingin tahu dan selalu ingin membantu orang lain. Setiap hari, {hero} menghabiskan waktunya menjelajahi lingkungan sekitar bersama teman baiknya, {friend}.",

        f"Pada suatu pagi, ketika mereka sedang berjalan di taman, tiba-tiba mereka {problem}. Mereka merasa penasaran dan memutuskan untuk mencari tahu apa yang sebenarnya sedang terjadi.",

        f"{friend} sempat merasa takut. Ia tidak tahu apakah mereka harus melanjutkan perjalanan atau kembali pulang. Namun {hero} mengingatkan bahwa mereka harus tetap tenang dan tidak mengambil keputusan secara terburu-buru.",

        f"Mereka mulai mengamati keadaan sekitar. Mereka melihat beberapa petunjuk yang sebelumnya tidak terlihat. Dari situ, mereka menyadari bahwa kejadian tersebut bukanlah sesuatu yang bisa diabaikan begitu saja.",

        f"{hero} kemudian mengajak {friend} untuk mencari bantuan. Mereka tahu bahwa menyelesaikan masalah tidak harus dilakukan sendirian. Terkadang, meminta bantuan merupakan keputusan yang paling bijaksana.",

        f"Mereka bertemu dengan seorang warga desa yang bernama Pak Danu. Pak Danu mendengarkan cerita mereka dengan penuh perhatian. Setelah memahami situasinya, ia memberikan beberapa saran agar masalah tersebut bisa diselesaikan dengan aman.",

        f"Awalnya, mereka mengalami kesulitan. Rencana pertama ternyata tidak berjalan sesuai harapan. {friend} mulai merasa kecewa, tetapi {hero} mengajaknya untuk tidak menyerah. Mereka mencoba memikirkan cara lain.",

        f"Setelah berdiskusi, mereka akhirnya menemukan solusi. Mereka bekerja sama dengan warga sekitar. Ada yang membantu menyiapkan perlengkapan, ada yang memberikan arahan, dan ada yang ikut menyelesaikan masalah tersebut.",

        f"Perlahan, keadaan mulai berubah. {reveal.capitalize()}. Semua orang merasa senang karena usaha mereka akhirnya membuahkan hasil.",

        f"Pak Danu tersenyum melihat apa yang telah dilakukan kedua anak itu. Ia mengatakan bahwa keberhasilan tersebut bukan hanya karena satu orang, tetapi karena semua orang mau bekerja sama.",

        f"{hero} dan {friend} merasa sangat bahagia. Mereka menyadari bahwa tindakan sederhana yang dilakukan dengan niat baik ternyata bisa memberikan dampak besar bagi orang lain.",

        f"Sebelum pulang, mereka berjanji akan terus membantu orang-orang di sekitar mereka. Mereka juga ingin mengajak teman-teman lainnya untuk melakukan hal yang sama.",

        f"Malam harinya, {hero} duduk di dekat jendela rumahnya. Ia memikirkan semua kejadian yang dialaminya hari itu. Ia merasa bersyukur karena mendapatkan pengalaman yang sangat berharga.",

        f"Keesokan harinya, {hero} dan {friend} kembali berjalan menyusuri desa. Kali ini mereka melihat banyak orang yang mulai melakukan kebaikan kecil. Suasana desa terasa semakin hangat dan menyenangkan.",

        f"Dari petualangan tersebut, mereka mendapatkan sebuah pelajaran penting. {rng.choice(lessons)}. Mereka pun memahami bahwa setiap orang memiliki kesempatan untuk membuat dunia menjadi lebih baik."
    ]

    story = {
        "title": title,
        "hero": hero,
        "friend": friend,
        "paragraphs": paragraphs,
        "created_at": datetime.now().isoformat()
    }

    with open("output/story.json", "w", encoding="utf-8") as f:
        json.dump(story, f, ensure_ascii=False, indent=2)

    with open("output/naskah.txt", "w", encoding="utf-8") as f:
        f.write(title + "\n\n")
        f.write("\n\n".join(paragraphs))

    print("Naskah berhasil dibuat:", title)

    return story


if __name__ == "__main__":
    make_story()
