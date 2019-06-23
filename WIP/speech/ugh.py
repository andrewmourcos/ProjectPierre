
import os
from pocketsphinx import LiveSpeech, get_model_path
import requests

#while 1==1:
#    a=requests.get('https://roberttoyonaga.api.stdlib.com/pierre-sheets@dev/?operation=get&data=poll')
#    if a== 'true':
#        print('poll is true')
#    elif a=='false':
#        print('poll is false')

#name= requests.get('https://roberttoyonaga.api.stdlib.com/pierre-sheets@dev/?operation=get&data=user_name')
#command =requests.get('https://roberttoyonaga.api.stdlib.com/pierre-sheets@dev/?operation=get&data=command')

name = str(input('what is your username: '))
command = str(input('what should I do? [record] or [clear] '))

if command=='clear':
    req = requests.get('https://roberttoyonaga.api.stdlib.com/pierre-sheets@dev/?operation=entries')
    req_list = req.content.decode('utf-8').split("\"")
    for i in req_list:
        if name in i:
            requests.get('https://roberttoyonaga.api.stdlib.com/pierre-sheets@dev/?operation=clear&myKey='+i)

    exit()

precede_list = ['and','and(2)','you','or', 'an(2)','ok', 'okay']
single_list = ['just','just(2)','normally']
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
            iSaid.append('you know')
        if word=='something' and (last_word in precede_list):
            iSaid.append(word)
        if word in single_list:
                iSaid.append(word)
        if word=='also' and (last_word in precede_list):
                iSaid.append(word)
        if word=='yeah' and (last_word in precede_list):
                iSaid.append(word)
        if word=='in' and last_word=='as':
                iSaid.append('as in')
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
filler_words = []
frequencies = []

for phrase in speech:
    filler, sentence = parse(phrase.segments())
    joined_filler = ','.join(filler)

    print(joined_filler,sentence)
    if len(filler)!=0:
        print(requests.get('https://roberttoyonaga.api.stdlib.com/pierre-sms@dev/?name='+joined_filler))
        for filler_word in filler:
            if filler_word not in filler_words:
                filler_words.append(filler_word)
                frequencies.append(1)
            else:
                frequencies[filler_words.index(filler_word)]+=1

            for filler_word in filler_words:
                requests.get('https://roberttoyonaga.api.stdlib.com/pierre-sheets@dev/?operation=set&data='+str(frequencies[filler_words.index(filler_word)])+
                '&myKey='+name+'_'+filler_word)


print(filler_words)
print(frequencies)




