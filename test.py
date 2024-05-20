import requests
texto = "meu marido quer que eu pague pensão aliemticia para ele, o que devo fazer?"
url = "https://api.clara.projetohorizontes.com/search"

resposta = requests.post(url, json = {"query" : texto})
bot_context = "\n\n".join(resposta.json()["text"])
print(bot_context)