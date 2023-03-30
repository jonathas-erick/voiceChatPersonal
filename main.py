import openai
import speech_recognition as sr
import pyttsx3

openai.api_key = "" #Chave_de_API 
model_engine = "text-davinci-003"

recognizer = sr.Recognizer()
microphone = sr.Microphone()

engine = pyttsx3.init()

palavra_chamada = "olá"

palavra_encerramento = "fechar"

def transcrever_voz():
    with microphone as fonte:
        recognizer.adjust_for_ambient_noise(fonte)
        audio = recognizer.listen(fonte)
    texto = recognizer.recognize_google(audio, language='pt-BR')
    return texto


def gerar_resposta(pergunta):
    resposta = openai.Completion.create(
        engine=model_engine,
        prompt=pergunta,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5
    )
    return resposta.choices[0].text.strip()

def gerar_resposta_turbo(pergunta):
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user",
                   "content": pergunta}]
    )
    return completion


def falar_resposta(resposta):
    engine.say(resposta)
    engine.runAndWait()


while True:
    print("Fale algo para o aplicativo...")
    try:       
        entrada = transcrever_voz().lower()        
        
        if palavra_encerramento in entrada:
            print("Encerrando o aplicativo...")
            break
                
        if palavra_chamada in entrada:
            
            entrada = entrada.replace(palavra_chamada, "", 1).strip()            
            
            if entrada:
                print("Você disse: " + entrada)

                #resposta = gerar_resposta(entrada)
                resposta = gerar_resposta(entrada)
                print("Resposta do ChatGPT: " + resposta)

                falar_resposta(resposta)
        
    except sr.UnknownValueError:
        print("Não foi possível entender o que você disse")
    except sr.RequestError as e:
        print("Erro ao tentar obter a sua mensagem; {0}".format(e))