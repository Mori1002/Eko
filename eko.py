import discord
from discord.ext import commands
import random
import os
import requests
from settings import setting
import asyncio 

# Podstawowe ustawienia bota
description = "Bot edukacyjny o zmianach klimatycznych."
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user} (ID: {bot.user.id})')
    print('Bot jest gotowy!')

    
@bot.command()
async def hej(ctx):
    await ctx.send("Cześć! Jak mogę pomóc w dowiadywaniu się o zmianach klimatycznych? Spróbuj:\n"
                   "- !mem - zobacz memy klimatyczne\n"
                   "- !fakt - poznaj ciekawostki\n"
                   "- !edu - sprawdź zasoby edukacyjne\n"
                   "- !tematy - zobacz definicje zwrotów i dowiedz sie więcej\n"
                   "- !quiz - sprawdź swoją wiedzę o klimacie!")
                   
                    

@bot.command()
async def mem(ctx):
    #Wysyła mem na temat zmian klimatycznych.
    images_folder = 'images'
    valid_extensions = ('.jpg', '.jpeg', '.png')
    images = [os.path.join(images_folder, image) for image in os.listdir(images_folder) if image.endswith(valid_extensions)]
    
    if images:
        random_image = random.choice(images)
        with open(random_image, 'rb') as f:
            picture = discord.File(f)
        await ctx.send(file=picture)
    else:
        await ctx.send("Brak obrazów w folderze 'images'. ")


def get_climate_fact():
    facts = [
        "Od 1880 roku średnia temperatura na Ziemi wzrosła o około 1,1°C.",
        "Poziom morza rośnie w tempie około 3,3 mm rocznie.",
        "80% energii globalnej pochodzi z paliw kopalnych.",
        "Każdego roku wycinane są lasy o powierzchni porównywalnej do Wielkiej Brytanii.",
        "Ponad milion gatunków zwierząt i roślin jest zagrożonych wyginięciem z powodu zmian klimatycznych.",
        "Ostatnia dekada była najcieplejszą w historii pomiarów temperatury. Rok 2016 i 2020 były rekordowo gorące.",
        "Poziom oceanów wzrósł o ponad 20 cm od 1880 roku z powodu topnienia lodowców i rozszerzalności cieplnej wody.",
        "Poziom dwutlenku węgla w atmosferze jest obecnie najwyższy od 800 tysięcy lat.",
        "Lodowiec Grenlandii traci około 280 miliardów ton lodu rocznie.",
        "Ponad milion gatunków roślin i zwierząt jest zagrożonych wyginięciem z powodu zmian klimatycznych.",
        "Lasy deszczowe Amazonii pochłaniają ogromne ilości CO₂, ale w wyniku wylesiania mogą same stać się źródłem emisji.",
        "Oceany pochłaniają około 25% dwutlenku węgla emitowanego przez ludzi, co powoduje ich zakwaszenie i wpływa na życie morskie.",
    ]
    return random.choice(facts)

@bot.command()
async def fakt(ctx):
    #Wysyła losowy fakt o zmianach klimatycznych.
    fact = get_climate_fact()
    await ctx.send(f"🌍 **Fakt o klimacie:** {fact}")


def get_climate_resource():
    resources = [
        "https://climate.nasa.gov/",
        "https://www.ipcc.ch/",
        "https://www.un.org/en/climatechange",
        "https://ec.europa.eu/clima/index_en",
        "https://350.org/"
    ]
    return random.choice(resources)

@bot.command()
async def edu(ctx):
    #Wysyła link do zasobu edukacyjnego na temat zmian klimatycznych.
    resource = get_climate_resource()
    await ctx.send(f"📚 **Zasób edukacyjny:** {resource}")

# **Funkcja quizu**
quiz_questions = [
    {
        "question": "Ile stopni wzrosła średnia temperatura Ziemi od 1880 roku?",
        "options": ["1°C", "1.5°C", "2°C"],
        "answer": "1°C"
    },
    {
        "question": "Jaką część dwutlenku węgla pochłaniają oceany?",
        "options": ["10%", "25%", "50%"],
        "answer": "25%"
    },
    {
        "question": "Który sektor jest największym źródłem emisji CO2?",
        "options": ["Transport", "Energia", "Rolnictwo"],
        "answer": "Energia"
    },
]

@bot.command()
async def quiz(ctx):
    question = random.choice(quiz_questions)
    options = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(question["options"])])
    await ctx.send(f"❓ **{question['question']}**\n{options}")

    def check(m):
        return m.author == ctx.author and m.content.isdigit() and 1 <= int(m.content) <= len(question["options"])

    try:
        msg = await bot.wait_for("message", check=check, timeout=30.0)
        selected_option = question["options"][int(msg.content) - 1]
        if selected_option == question["answer"]:
            await ctx.send("✅ **Brawo! To poprawna odpowiedź.**")
        else:
            await ctx.send(f"❌ **Źle! Prawidłowa odpowiedź to:** {question['answer']}.")
    except asyncio.TimeoutError:
        await ctx.send("⏰ **Czas minął! Spróbuj jeszcze raz.**")

# Lista tematów i szczegółowych informacji
topics = {
    "globalne ocieplenie": "Globalne ocieplenie to wzrost średniej temperatury atmosfery Ziemi i oceanów, głównie z powodu emisji gazów cieplarnianych. To zjawisko wpływa na ekstremalne zjawiska pogodowe, topnienie lodowców i podnoszenie się poziomu mórz.",
    "energia odnawialna": "Energia odnawialna pochodzi ze źródeł naturalnych, takich jak słońce, wiatr i woda. Jest kluczowym elementem walki ze zmianami klimatycznymi, ponieważ pozwala redukować emisje dwutlenku węgla.",
    "wylesianie": "Wylesianie to usuwanie lasów, często w celu pozyskania ziemi rolniczej lub drewna. Powoduje to utratę bioróżnorodności, zakłócenie cyklu wodnego i zwiększenie emisji CO₂.",
    "zakwaszenie oceanów": "Zakwaszenie oceanów to proces, w którym oceany pochłaniają CO₂ z atmosfery, co prowadzi do obniżenia ich pH. Wpływa to negatywnie na organizmy morskie, szczególnie na koralowce i skorupiaki.",
    "emisja gazów cieplarnianych": "Gazy cieplarniane, takie jak CO₂, metan i podtlenek azotu, zatrzymują ciepło w atmosferze, co powoduje efekt cieplarniany. Ich głównymi źródłami są spalanie paliw kopalnych, rolnictwo i wylesianie.",
    "Efekt cieplarniany": "Mechanizm naturalny, który utrzymuje ciepło na Ziemi, ale jest wzmacniany przez emisję gazów cieplarnianych, co prowadzi do globalnego ocieplenia.",
    "Katastrofy naturalne": "Wzrost częstotliwości i intensywności huraganów, powodzi, susz oraz pożarów lasów spowodowanych zmianami klimatycznymi.",
    "Ślad węglowy": "Miara emisji gazów cieplarnianych generowanych przez indywidualne osoby, firmy i kraje."
}

@bot.command()
async def tematy(ctx):
    # Wyświetla listę dostępnych tematów
    available_topics = "\n".join([f"- {topic}" for topic in topics.keys()])
    await ctx.send(f"🌍 **Dostępne tematy:**\n{available_topics}\n\nWpisz `!rozwin <nazwa tematu>`, aby dowiedzieć się więcej i poznać definicje!")

@bot.command()
async def rozwin(ctx, *, topic_name):
    # Rozwija szczegóły na temat wybranego tematu
    topic_name = topic_name.lower()
    if topic_name in topics:
        await ctx.send(f"📖 **{topic_name.capitalize()}:** {topics[topic_name]}")
    else:
        await ctx.send("❌ Nie znam tego tematu. Sprawdź listę dostępnych tematów za pomocą komendy `!tematy`.")


bot.run(setting['TOKEN'])
