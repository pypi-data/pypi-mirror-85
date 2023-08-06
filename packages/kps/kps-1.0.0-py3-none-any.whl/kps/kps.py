import random

sentences = [
    "Chal baap ko mat sikha",
    "Mein ja ra room",
    "I use Arch BTW",
    "Nothing changes if nothing changes",
    "Mein to nahi dene waala",
    "Tell me something I don't know",
    "La likh lu, kahin UPSC ke exam mein na aa jaaye",
    "Jo hai. So hai.",
    "Bhookh lagi hai",
    "Kun faya .. Kun faya .. Kun faya kun...",
    "Lode pe likha hai. Dekhega ?",
    "Papa nahi maanenge",
    "Pls don't talk to me",
    "Konsi assignment ?"
]

def say():
    print(random.choice(sentences))