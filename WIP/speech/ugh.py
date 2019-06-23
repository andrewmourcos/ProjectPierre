
import os
from pocketsphinx import LiveSpeech, get_model_path
import requests

precede_list = ['and','and(2)','you','or', 'an(2)']

def parse(sentence):#,fillers):
    iSaid = []
    last_word = ''
    for word in sentence:
        if word=='like' and (last_word in precede_list):
            iSaid.append(word)
        if word=='basically' and (last_word in precede_list):
            iSaid.append(word)
        if word=='essentially' and (last_word in precede_list):
            iSaid.append(word)
        if (word=='okay' or word=='ok')  and (last_word in precede_list):
                iSaid.append(word)
        if word=='so' and (last_word in precede_list):
                iSaid.append(word)
        if (word=='no' or word=='know') and (last_word in precede_list):
            iSaid.append(word)
        if word=='something' and (last_word in precede_list):
            iSaid.append(word)
        last_word=word
    return iSaid, sentence



model_path = get_model_path()

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=512,#2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'en-us'),
    lm=os.path.join(model_path, 'en-us.lm.bin'),
    dic=os.path.join(model_path, 'cmudict-en-us.dict')
)

#fillers= ['and','essentially', 'okay', 'basically', 'so', 'like']

for phrase in speech:
    filler, sentence = parse(phrase.segments())
    joined_filler = '.'.join(filler)

    print(joined_filler,sentence)
    if len(filler)!=0:
        print(requests.get('https://roberttoyonaga.api.stdlib.com/pierre-sms@dev/?name='+joined_filler))

