import sys
import io
import os
import codecs

locdict = sys.argv[1]
dirpath = os.getcwd()

dictraw = codecs.open(dirpath + '/ravn/ravndict.csv', 'r', 'utf-8')

wordlist = []
mydict = {}

#print(' '.join(doublesampalist))

herding = ['Ø','Æ']

vokalar = ['O','E','a','y','Y','2','9','u','U','o','i','I','e','8']
diffvokal = ['EA','OA','UJ','EJ','aJ','aW','3W','EW','9W','9J']
kons = ['p','b','t','d','k','g','f','v','s','S','z','h','tS','dZ','m','M','n','x','N','X','l','L','j','w','r','J','W','A']

sounds = []
    
for line in dictraw:
    tmpsampa = []
    thesplit = line.split("[",1)
    word = thesplit[0].strip()
    wordlist.append(word)
    sampa = thesplit[1].split("]",1)[0].strip()
    n = 0
    i = 0
    r = len(sampa)
    for value in sampa:
        if i == 0:
            if value in herding:
                if n+2 < r:
                    if sampa[n+1:n+3] in diffvokal:
                        
                        tmpsampa.append(value+sampa[n+1:n+3])
                        i = 3
                
                if sampa[n+1] in vokalar and i == 0:
                    
                    tmpsampa.append(value+sampa[n+1])
                    i = 2
        
        
            if sampa[n:n+2] in diffvokal  and i == 0:
                tmpsampa.append(sampa[n:n+2])
                i = 2
            if sampa[n] in vokalar and i == 0:
                tmpsampa.append(sampa[n])
                i = 1
            if sampa[n:n+2] in kons  and i == 0:
                tmpsampa.append(sampa[n:n+2])
                i = 2
            if sampa[n] in kons and i == 0:
                tmpsampa.append(sampa[n])
                i = 1
                

            
        if i > 0:
            i = i - 1
        n = n + 1

    if word in mydict:
        arr2 = mydict[word]
        tmp = ' '.join(tmpsampa)
        arr2.append(tmp)
        mydict[word] = arr2
    else:
        mydict[word] = [' '.join(tmpsampa)]
    for singleSound in tmpsampa:
        sounds.append(singleSound)
        
    
        
    
    

lextxt = open(locdict+'/lexicon.txt','a+',encoding='utf-8')
lextxtp = open(locdict+'/lexiconp.txt','a+',encoding='utf-8')


for key in mydict:
    for j in set(mydict[key]):
        lextxt.write(key+'\t'+j+'\n')
        lextxtp.write(key+'\t1.0'+'\t'+j+'\n')



nonsilpho = open(locdict+'/nonsilence_phones.txt','a+',encoding='utf-8')
silpho = open(locdict+'/silence_phones.txt','a+',encoding='utf-8')
vocab = open(locdict+'/vocab-oov.txt','a+',encoding='utf-8')
extraquestions = open(locdict+'/extra_questions.txt','a+',encoding='utf-8')





sampalist = sorted(set(sounds))

for value in sampalist:
    nonsilpho.write(value+'\n')

silpho.write('SIL\n')
#silpho.write('NSN\n')
optsil = open(locdict+'/optional_silence.txt','a+',encoding='utf-8')
optsil.write('SIL\n')


lextxt.write('!SIL\tSIL\n')
#lextxt.write('<unk>\tNSN\n')
lextxtp.write('!SIL\t1.0\tSIL\n')
#lextxtp.write('<unk>\t1.0\tNSN\n')

optsil.close()
lextxt.close()
lextxtp.close()
nonsilpho.close()
silpho.close()
vocab.close()
extraquestions.close()

