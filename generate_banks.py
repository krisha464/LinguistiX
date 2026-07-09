import os
import json
import random

os.makedirs('data', exist_ok=True)

# Generate Word Quest Bank (30 items)
wq_items = []
vocab = [
    ("Bonjour", "Hello", ["Goodbye", "House", "River"], "fr→en", "beginner"),
    ("Libro", "Book", ["Door", "Moon", "Apple"], "es→en", "beginner"),
    ("Chat", "Cat", ["Dog", "Bird", "Mouse"], "fr→en", "beginner"),
    ("Agua", "Water", ["Fire", "Earth", "Air"], "es→en", "beginner"),
    ("Maison", "House", ["Tree", "Car", "Sun"], "fr→en", "beginner"),
    ("Sol", "Sun", ["Moon", "Star", "Cloud"], "es→en", "beginner"),
    ("Merci", "Thank you", ["Please", "Sorry", "Welcome"], "fr→en", "beginner"),
    ("Perro", "Dog", ["Cat", "Fish", "Bird"], "es→en", "beginner"),
    ("Fille", "Girl", ["Boy", "Man", "Woman"], "fr→en", "beginner"),
    ("Niño", "Boy", ["Girl", "Man", "Woman"], "es→en", "beginner"),
    ("Mañana", "Tomorrow", ["Yesterday", "Today", "Morning"], "es→en", "intermediate"),
    ("Toujours", "Always", ["Never", "Sometimes", "Often"], "fr→en", "intermediate"),
    ("Cuchara", "Spoon", ["Fork", "Knife", "Plate"], "es→en", "intermediate"),
    ("Fenêtre", "Window", ["Door", "Wall", "Floor"], "fr→en", "intermediate"),
    ("Desarrollo", "Development", ["Decline", "Growth", "Start"], "es→en", "intermediate"),
    ("Écran", "Screen", ["Keyboard", "Mouse", "Speaker"], "fr→en", "intermediate"),
    ("Bolsillo", "Pocket", ["Bag", "Purse", "Wallet"], "es→en", "intermediate"),
    ("Voiture", "Car", ["Bus", "Train", "Plane"], "fr→en", "intermediate"),
    ("Reloj", "Clock", ["Watch", "Time", "Hour"], "es→en", "intermediate"),
    ("Ciel", "Sky", ["Cloud", "Rain", "Sun"], "fr→en", "intermediate"),
    ("Courage", "Bravery", ["Silence", "Weather", "Fury"], "fr→en", "advanced"),
    ("Madrugada", "Dawn", ["Dusk", "Midnight", "Noon"], "es→en", "advanced"),
    ("Époustouflant", "Breathtaking", ["Boring", "Ugly", "Normal"], "fr→en", "advanced"),
    ("Imprescindible", "Essential", ["Optional", "Useless", "Extra"], "es→en", "advanced"),
    ("Cauchemar", "Nightmare", ["Dream", "Sleep", "Bed"], "fr→en", "advanced"),
    ("Inolvidable", "Unforgettable", ["Boring", "Routine", "Normal"], "es→en", "advanced"),
    ("Parapluie", "Umbrella", ["Raincoat", "Boots", "Hat"], "fr→en", "advanced"),
    ("Rascacielos", "Skyscraper", ["House", "Cabin", "Tent"], "es→en", "advanced"),
    ("Serrure", "Lock", ["Key", "Door", "Handle"], "fr→en", "advanced"),
    ("Cicatriz", "Scar", ["Wound", "Bandage", "Medicine"], "es→en", "advanced")
]
for word, correct, wrongs, lang, diff in vocab:
    wq_items.append({"word": word, "correct_translation": correct, "wrong_options": wrongs, "difficulty": diff, "language_pair": lang})


# Generate Story Bank (30 items)
story_items = []
templates = [
    # Beginner
    ("The cat sat on the ______.", "mat", ["mat", "dog", "sky", "water"], "noun", "beginner", "🛏️", "🐕", "☁️", "💧"),
    ("She likes to eat ______.", "apples", ["apples", "rocks", "clouds", "books"], "noun", "beginner", "🍎", "🪨", "☁️", "📚"),
    ("He is very ______ today.", "happy", ["happy", "blue", "loud", "square"], "adjective", "beginner", "😊", "🟦", "📢", "⬛"),
    ("They run ______ the park.", "in", ["in", "on", "under", "over"], "preposition", "beginner", "🌳", "📦", "🔽", "🔼"),
    ("The sun is very ______.", "bright", ["bright", "cold", "dark", "wet"], "adjective", "beginner", "☀️", "❄️", "🌑", "💧"),
    ("I drink water when I am ______.", "thirsty", ["thirsty", "hungry", "tired", "sad"], "adjective", "beginner", "💧", "🍔", "😴", "😢"),
    ("The sky is ______.", "blue", ["blue", "green", "red", "yellow"], "color", "beginner", "🟦", "🟩", "🟥", "🟨"),
    ("He drives a fast ______.", "car", ["car", "tree", "house", "book"], "noun", "beginner", "🚗", "🌳", "🏠", "📚"),
    ("She reads a ______.", "book", ["book", "shoe", "apple", "door"], "noun", "beginner", "📚", "👞", "🍎", "🚪"),
    ("They live in a big ______.", "house", ["house", "car", "tree", "cloud"], "noun", "beginner", "🏠", "🚗", "🌳", "☁️"),
    # Intermediate
    ("The detective found a ______ clue.", "hidden", ["hidden", "loud", "tasty", "soft"], "adjective", "intermediate", "🔍", "📢", "🍔", "☁️"),
    ("She spoke ______ during the meeting.", "quietly", ["quietly", "heavy", "blue", "spicy"], "adverb", "intermediate", "🤫", "🪨", "🟦", "🌶️"),
    ("The bridge was built across the ______ river.", "wide", ["wide", "dry", "solid", "loud"], "adjective", "intermediate", "🌊", "🏜️", "🪨", "📢"),
    ("He decided to ______ the old bicycle.", "repair", ["repair", "eat", "sing", "drink"], "verb", "intermediate", "🔧", "🍔", "🎤", "💧"),
    ("The mountain peak was covered in ______.", "snow", ["snow", "fire", "sand", "grass"], "noun", "intermediate", "❄️", "🔥", "🏜️", "🌱"),
    ("She painted a beautiful ______ on the canvas.", "landscape", ["landscape", "noise", "smell", "taste"], "noun", "intermediate", "🖼️", "📢", "👃", "👅"),
    ("The old book had ______ pages.", "yellowed", ["yellowed", "loud", "spicy", "heavy"], "adjective", "intermediate", "📄", "📢", "🌶️", "🪨"),
    ("They walked through the dense ______.", "forest", ["forest", "ocean", "sky", "desert"], "noun", "intermediate", "🌲", "🌊", "☁️", "🏜️"),
    ("He bought a new ______ for his camera.", "lens", ["lens", "tire", "shoe", "cup"], "noun", "intermediate", "📷", "🚗", "👞", "☕"),
    ("The cake was baked to ______.", "perfection", ["perfection", "failure", "sadness", "anger"], "noun", "intermediate", "🎂", "❌", "😢", "😠"),
    # Advanced
    ("He is very ______ about detail; even the smallest error is noticed.", "meticulous", ["meticulous", "flippant", "loquacious", "ephemeral"], "adjective", "advanced", "🛡️", "💬", "📢", "🕐"),
    ("Her explanation was highly ______ and difficult to grasp.", "esoteric", ["esoteric", "lucid", "banal", "trite"], "adjective", "advanced", "🧠", "💡", "🥱", "♻️"),
    ("The politician's speech was full of ______ rhetoric.", "bombastic", ["bombastic", "succinct", "timid", "laconic"], "adjective", "advanced", "💥", "✂️", "🐭", "🤐"),
    ("The desert climate is famously ______.", "arid", ["arid", "humid", "frigid", "temperate"], "adjective", "advanced", "🏜️", "💧", "❄️", "🌡️"),
    ("He showed a ______ disregard for the rules.", "flagrant", ["flagrant", "subtle", "covert", "hidden"], "adjective", "advanced", "🚩", "🕵️", "🕶️", "📦"),
    ("The negotiations reached an ______.", "impasse", ["impasse", "agreement", "opening", "start"], "noun", "advanced", "🛑", "🤝", "🔓", "🏁"),
    ("She has a ______ for finding trouble.", "penchant", ["penchant", "dislike", "aversion", "fear"], "noun", "advanced", "🧲", "👎", "🙅", "😱"),
    ("The disease is ______ in that region.", "endemic", ["endemic", "rare", "unknown", "absent"], "adjective", "advanced", "🦠", "🦄", "❓", "❌"),
    ("His mood was incredibly ______.", "mercurial", ["mercurial", "stable", "constant", "fixed"], "adjective", "advanced", "🌡️", "🪨", "⏳", "📌"),
    ("The evidence was purely ______.", "anecdotal", ["anecdotal", "empirical", "scientific", "proven"], "adjective", "advanced", "🗣️", "🔬", "🧪", "✅")
]

for prompt, ans, opts, hint, diff, ic1, ic2, ic3, ic4 in templates:
    opt_dicts = []
    icons = [ic1, ic2, ic3, ic4]
    for i, opt in enumerate(opts):
        opt_dicts.append({"title": opt.capitalize(), "desc": f"Definition for {opt}", "icon": icons[i]})
    story_items.append({"prompt": prompt, "answer": ans.capitalize(), "options": opt_dicts, "hint": hint, "difficulty": diff})

# Lightning Blitz (30 items)
lb_items = []
for i in range(30):
    diff = "beginner" if i < 10 else "intermediate" if i < 20 else "advanced"
    word = vocab[i]
    lb_items.append({"prompt": f"Translate '{word[1]}' to {word[3].split('→')[0].upper()}", "answer": word[0], "options": [word[0]] + word[2], "difficulty": diff})

# Detective Bank (30 items)
det_items = []
det_data = [
    # Beginner
    ("A place where books are kept", "building", "l", "I borrowed a novel from the ________.", "library", "beginner"),
    ("A person who writes stories", "job", "a", "The ________ published a new fairy tale.", "author", "beginner"),
    ("A vehicle that carries people across water", "transport", "b", "We crossed the river by ________.", "boat", "beginner"),
    ("A yellow fruit", "food", "b", "Monkeys love to eat ________.", "banana", "beginner"),
    ("A domesticated feline", "animal", "c", "The ________ meowed loudly.", "cat", "beginner"),
    ("A warm, glowing sphere in the sky", "nature", "s", "The ________ shines brightly today.", "sun", "beginner"),
    ("A place to sleep", "furniture", "b", "I went to ________ early.", "bed", "beginner"),
    ("A tool for cutting paper", "tool", "s", "Use the ________ carefully.", "scissors", "beginner"),
    ("A large plant with a trunk", "nature", "t", "The ________ provided shade.", "tree", "beginner"),
    ("A sweet baked good", "food", "c", "We had ________ for dessert.", "cake", "beginner"),
    # Intermediate
    ("A device for measuring time", "object", "c", "The ________ struck twelve.", "clock", "intermediate"),
    ("A person who treats sick animals", "job", "v", "The ________ examined the dog.", "veterinarian", "intermediate"),
    ("A large body of saltwater", "nature", "o", "We sailed across the ________.", "ocean", "intermediate"),
    ("A musical instrument with black and white keys", "instrument", "p", "She played the ________ beautifully.", "piano", "intermediate"),
    ("A building where paintings are shown", "place", "g", "The ________ featured modern art.", "gallery", "intermediate"),
    ("A piece of glass that reflects images", "object", "m", "He looked in the ________.", "mirror", "intermediate"),
    ("A person who prepares food", "job", "c", "The ________ cooked a great meal.", "chef", "intermediate"),
    ("A vehicle that travels in space", "transport", "r", "The ________ launched into orbit.", "rocket", "intermediate"),
    ("A place where scientific experiments are done", "place", "l", "The scientist worked in the ________.", "laboratory", "intermediate"),
    ("A tool used to see distant objects", "tool", "t", "He looked at the stars through a ________.", "telescope", "intermediate"),
    # Advanced
    ("A persistent false belief", "psychology", "d", "He suffered from a ________ of grandeur.", "delusion", "advanced"),
    ("A state of physical or mental weariness", "health", "l", "She was overcome with ________.", "lethargy", "advanced"),
    ("A subtle difference in meaning", "language", "n", "He explained the ________ of the word.", "nuance", "advanced"),
    ("A chronological misplacement", "history", "a", "The sword in the modern movie was an ________.", "anachronism", "advanced"),
    ("A universal remedy", "medicine", "p", "There is no single ________ for all diseases.", "panacea", "advanced"),
    ("A deviation from what is normal", "science", "a", "The result was a statistical ________.", "anomaly", "advanced"),
    ("A noisy, confusing situation", "event", "c", "The protest turned into a ________.", "cacophony", "advanced"),
    ("A superficial appearance or illusion", "abstract", "v", "He maintained a ________ of respectability.", "veneer", "advanced"),
    ("A sudden realization or comprehension", "abstract", "e", "She had an ________ about the problem.", "epiphany", "advanced"),
    ("A shortage or lack of something", "abstract", "d", "There is a ________ of evidence.", "dearth", "advanced")
]
for d, c, f, e, a, diff in det_data:
    det_items.append({"definition": d, "category": c, "first_letter": f, "example": e, "answer": a, "difficulty": diff})

# Scramble Bank (30 items)
scramble_items = []
sentences = [
    # Beginner
    ("I enjoy learning languages", "beginner"),
    ("She reads every morning", "beginner"),
    ("We travel together often", "beginner"),
    ("The dog runs fast", "beginner"),
    ("He likes to eat apples", "beginner"),
    ("The sky is very blue", "beginner"),
    ("I have a red car", "beginner"),
    ("They play in the park", "beginner"),
    ("She sings a happy song", "beginner"),
    ("The book is on the table", "beginner"),
    # Intermediate
    ("The quick brown fox jumps over the lazy dog", "intermediate"),
    ("He decided to repair the old bicycle", "intermediate"),
    ("She painted a beautiful landscape on the canvas", "intermediate"),
    ("They walked through the dense forest together", "intermediate"),
    ("The detective found a hidden clue", "intermediate"),
    ("We will arrive at the station soon", "intermediate"),
    ("The chef prepared a delicious meal for us", "intermediate"),
    ("He carefully opened the fragile box", "intermediate"),
    ("She practiced the piano every evening", "intermediate"),
    ("The birds migrated south for the winter", "intermediate"),
    # Advanced
    ("The negotiations eventually reached an unexpected impasse", "advanced"),
    ("His explanation was highly esoteric and difficult to grasp", "advanced"),
    ("She demonstrated a flagrant disregard for the established rules", "advanced"),
    ("The evidence presented was purely anecdotal and lacked empirical support", "advanced"),
    ("The political climate in the region remained highly mercurial", "advanced"),
    ("They discussed the subtle nuances of the complex argument", "advanced"),
    ("The discovery of the artifact was a significant historical anomaly", "advanced"),
    ("He was overcome with profound lethargy after the arduous journey", "advanced"),
    ("The proposed solution was viewed as a universal panacea", "advanced"),
    ("The symphony concluded with a deafening cacophony of sound", "advanced")
]
for s, diff in sentences:
    scramble_items.append({"source": s, "target": s.split(), "difficulty": diff})

# Listening Bank (30 items)
list_items = []
for i in range(30):
    diff = "beginner" if i < 10 else "intermediate" if i < 20 else "advanced"
    word = vocab[i]
    list_items.append({"audio_text": word[0], "correct_translation": word[1], "options": [word[1]] + [w.capitalize() for w in word[2]], "lang": word[3].split('→')[0], "difficulty": diff})

# Grammar Bank (30 items)
grammar_items = []
grammar_data = [
    # Beginner
    ("She go to school every day.", 1, "goes", ["go", "goes", "gone", "going"], "beginner"),
    ("They has finished the task.", 1, "have", ["has", "have", "had", "having"], "beginner"),
    ("I am reading a interesting book.", 4, "an", ["a", "an", "the", "one"], "beginner"),
    ("He don't like apples.", 1, "doesn't", ["don't", "doesn't", "didn't", "isn't"], "beginner"),
    ("The cats is sleeping.", 2, "are", ["is", "are", "am", "be"], "beginner"),
    ("I seen him yesterday.", 1, "saw", ["seen", "saw", "see", "seeing"], "beginner"),
    ("She is more taller than me.", 2, "taller", ["more taller", "taller", "tallest", "tall"], "beginner"),
    ("We was at the park.", 1, "were", ["was", "were", "are", "is"], "beginner"),
    ("He plays good.", 2, "well", ["good", "well", "better", "best"], "beginner"),
    ("I want to goes home.", 3, "go", ["goes", "go", "going", "gone"], "beginner"),
    # Intermediate
    ("If I was you, I would leave.", 2, "were", ["was", "were", "am", "be"], "intermediate"),
    ("She told me that she will come.", 6, "would", ["will", "would", "shall", "can"], "intermediate"),
    ("He is used to wake up early.", 5, "waking", ["wake", "waking", "woke", "waken"], "intermediate"),
    ("Despite of the rain, we went out.", 1, "Despite", ["Despite of", "Despite", "In spite", "Although"], "intermediate"),
    ("I look forward to meet you.", 4, "meeting", ["meet", "meeting", "met", "meets"], "intermediate"),
    ("Hardly had I left than it started raining.", 4, "when", ["than", "when", "then", "that"], "intermediate"),
    ("She enjoys to read books.", 2, "reading", ["to read", "reading", "read", "reads"], "intermediate"),
    ("The police is investigating the case.", 2, "are", ["is", "are", "was", "has"], "intermediate"),
    ("He denied to steal the money.", 2, "stealing", ["to steal", "stealing", "steal", "stolen"], "intermediate"),
    ("I prefer tea than coffee.", 3, "to", ["than", "to", "over", "from"], "intermediate"),
    # Advanced
    ("The principal, along with the teachers, are attending.", 6, "is", ["are", "is", "were", "have"], "advanced"),
    ("Scarcely had she arrived than the meeting began.", 4, "when", ["than", "when", "then", "that"], "advanced"),
    ("He insisted on me going there.", 3, "my", ["me", "my", "mine", "I"], "advanced"),
    ("The committee have reached a decision.", 2, "has", ["have", "has", "had", "are"], "advanced"),
    ("Neither the manager nor the employees was aware.", 6, "were", ["was", "were", "is", "has"], "advanced"),
    ("She is one of those who is always late.", 6, "are", ["is", "are", "was", "am"], "advanced"),
    ("It is high time you start studying.", 5, "started", ["start", "started", "starting", "starts"], "advanced"),
    ("By the time you arrive, I will leave.", 7, "will have left", ["will leave", "will have left", "left", "have left"], "advanced"),
    ("Not only he is smart, but also hardworking.", 2, "is he", ["he is", "is he", "he was", "he has"], "advanced"),
    ("I wish I have a car.", 3, "had", ["have", "had", "has", "having"], "advanced")
]
for s, idx, cw, opts, diff in grammar_data:
    grammar_items.append({"sentence": s, "error_word_index": idx, "correct_word": cw, "options": opts, "difficulty": diff})

# Picture Match (30 items)
pic_items = []
pic_data = [
    # Beginner
    ("🍎", "apple", ["apple", "car", "book", "house"], "beginner"),
    ("🚗", "car", ["car", "tree", "cat", "sun"], "beginner"),
    ("🏠", "house", ["house", "shoe", "chair", "river"], "beginner"),
    ("🐶", "dog", ["dog", "cat", "bird", "fish"], "beginner"),
    ("🐱", "cat", ["cat", "dog", "mouse", "cow"], "beginner"),
    ("☀️", "sun", ["sun", "moon", "star", "cloud"], "beginner"),
    ("🌙", "moon", ["moon", "sun", "sky", "rain"], "beginner"),
    ("📚", "book", ["book", "pen", "paper", "desk"], "beginner"),
    ("🌳", "tree", ["tree", "flower", "grass", "leaf"], "beginner"),
    ("👟", "shoe", ["shoe", "sock", "shirt", "pant"], "beginner"),
    # Intermediate
    ("📷", "camera", ["camera", "phone", "tv", "radio"], "intermediate"),
    ("🚲", "bicycle", ["bicycle", "car", "bus", "train"], "intermediate"),
    ("⌚", "watch", ["watch", "clock", "bracelet", "ring"], "intermediate"),
    ("🎸", "guitar", ["guitar", "piano", "drum", "violin"], "intermediate"),
    ("🚀", "rocket", ["rocket", "plane", "helicopter", "boat"], "intermediate"),
    ("🍔", "hamburger", ["hamburger", "pizza", "hotdog", "taco"], "intermediate"),
    ("⛰️", "mountain", ["mountain", "hill", "valley", "river"], "intermediate"),
    ("🏖️", "beach", ["beach", "desert", "forest", "city"], "intermediate"),
    ("🏰", "castle", ["castle", "house", "tent", "building"], "intermediate"),
    ("🚁", "helicopter", ["helicopter", "plane", "rocket", "drone"], "intermediate"),
    # Advanced
    ("🔬", "microscope", ["microscope", "telescope", "glasses", "lens"], "advanced"),
    ("🧬", "dna", ["dna", "cell", "virus", "bacteria"], "advanced"),
    ("🧲", "magnet", ["magnet", "iron", "steel", "metal"], "advanced"),
    ("⚖️", "scales", ["scales", "weight", "balance", "measure"], "advanced"),
    ("🏺", "amphora", ["amphora", "vase", "jug", "pot"], "advanced"),
    ("🗿", "moai", ["moai", "statue", "sculpture", "monument"], "advanced"),
    ("🧿", "nazar", ["nazar", "amulet", "charm", "gem"], "advanced"),
    ("🪬", "hamsa", ["hamsa", "hand", "symbol", "sign"], "advanced"),
    ("🪷", "lotus", ["lotus", "lily", "flower", "rose"], "advanced"),
    ("🪸", "coral", ["coral", "reef", "seaweed", "shell"], "advanced")
]
for e, w, opts, diff in pic_data:
    pic_items.append({"emoji": e, "word": w, "options": opts, "difficulty": diff})


with open("data/game_banks.py", "w", encoding="utf-8") as f:
    f.write("WORD_QUEST_BANK = " + json.dumps(wq_items, indent=4, ensure_ascii=False) + "\n\n")
    f.write("STORY_BANK = " + json.dumps(story_items, indent=4, ensure_ascii=False) + "\n\n")
    f.write("LIGHTNING_BANK = " + json.dumps(lb_items, indent=4, ensure_ascii=False) + "\n\n")
    f.write("DETECTIVE_BANK = " + json.dumps(det_items, indent=4, ensure_ascii=False) + "\n\n")
    f.write("SCRAMBLE_BANK = " + json.dumps(scramble_items, indent=4, ensure_ascii=False) + "\n\n")
    f.write("LISTENING_BANK = " + json.dumps(list_items, indent=4, ensure_ascii=False) + "\n\n")
    f.write("GRAMMAR_BANK = " + json.dumps(grammar_items, indent=4, ensure_ascii=False) + "\n\n")
    f.write("PICTURE_BANK = " + json.dumps(pic_items, indent=4, ensure_ascii=False) + "\n\n")

print("Generated game banks successfully!")
