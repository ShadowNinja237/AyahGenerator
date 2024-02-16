from flask import Flask, render_template, request
import csv, random, requests

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/', methods=["GET", "POST"])
def index():

    ayah = None
    info, link = "", ""
    juz = request.args.get("juz_num", None)

    if juz:
        chapters = []
        ayahs = {}

        with open('Arabic-Quran.csv', 'r', encoding="utf8") as file:

            reader = csv.reader(file)

            # Find what chapters there are in the Juz
            for line in reader:
                if line[0] == juz:
                    chapters.append(int(line[1]))

            # Pick a random chapter from the chapters in the Juz
            picked_chapter = random.choice(chapters)

            # Reset reader position
            file.seek(0)

            for line in reader:
                if line[0] == juz:
                    if line[1] == str(picked_chapter):
                        ayahs[int(line[2])] = line[3]

            # max(ayah_nums) - 2 because we dont want to pick the 2 last ayahs of a chapter (whats the point of that)
            picked_ayah_num = random.randint(min(ayahs.keys()) + 1, max(ayahs.keys()) - 2)

            ayah = ayahs[picked_ayah_num]

            api = "https://api.alquran.cloud/v1/surah/" + str(picked_chapter) +"?limit=1"

            data = get_data(api)

            surah_name = data["data"]["englishName"]

            info = surah_name + " " + str(picked_chapter) + ":" + str(picked_ayah_num)

            link = f"https://quran.com/{str(picked_chapter)}?startingVerse={str(picked_ayah_num)}"


    return render_template("index.html", juz=juz, ayah=ayah, info=info, link=link)

def get_data(api):

    response = requests.get(api)

    if response.status_code == 200:
        print("Fetched the data")
        return response.json()
    else:
        print(f"There is an {response.status_code} error with your request. The API may be down at this time.")


if __name__ == '__main__':
    app.run()