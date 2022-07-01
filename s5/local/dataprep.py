import sys
import glob
import os
import random


dirpath = os.getcwd()
spk2genfile = str(sys.argv[2] + '/local/spk2gender')
wrtfile = open(spk2genfile, 'a+',encoding='utf-8')
speakall = open(sys.argv[1],'r', encoding='utf-8')
srcfolder = sys.argv[3]
ptest = float(sys.argv[4])
pdev = float(sys.argv[5])


speakallfile = sys.argv[2] + "/local/tmp/speakers_all.txt"
speaktestfile = sys.argv[2] + "/local/tmp/speakers_test.txt"
speaktrainfile = sys.argv[2] + "/local/tmp/speakers_train.txt"
speakdevfile = sys.argv[2] + "/local/tmp/speakers_dev.txt"

speakallf = open(speakallfile,'r',encoding='utf-8')
speaktest = open(speaktestfile,'w',encoding='utf-8')
speaktrain = open(speaktrainfile, 'w',encoding='utf-8')
speakdev = open(speakdevfile, 'w',encoding='utf-8')

for row in speakallf:
    r = random.random()
    if r < pdev:
        speakdev.write(row)
    elif r < ptest + pdev:
        speaktest.write(row)
    else:
        speaktrain.write(row)
speaktest.close()
speaktrain.close()
speakdev.close()



speaktest = open(speaktestfile,'r',encoding='utf-8')
speaktrain = open(speaktrainfile,'r',encoding='utf-8')
speakdev = open(speakdevfile,'r',encoding='utf-8')

for line in speakall:
    if line[0] == "K":
        wrtfile.write(str(line.strip())+ " f\n")
    else:
        wrtfile.write(str(line.strip())+ " m\n")

testspk2utt = open(sys.argv[2] + '/test/spk2utt', 'a+',encoding='utf-8')
testutt2spk = open(sys.argv[2] + '/test/utt2spk', 'a+',encoding='utf-8')
test_trans = open(sys.argv[2] + '/test/text', 'a+',encoding='utf-8')
test_wav_scp = open(sys.argv[2] + '/test/wav.scp', 'a+',encoding='utf-8')

for line in speaktest:
    speaker = line.strip()
    spkfolder = srcfolder + speaker + "/wav"
    files = glob.glob(spkfolder + '/*.wav', recursive =False)
    lines = []
    for fline in files:
        filename = fline.rsplit("/",1)[1]
        lines.append(filename.split(".")[0] + " " + dirpath+"/"+fline)
    lines.sort()
    for lline in lines:
        test_wav_scp.write(lline + "\n")
    
    lines = []
    for fline in files:
        filename = fline.rsplit("/",1)[1].split(".")[0]
        lines.append(str(filename))
    lines.sort()
    testspk2utt.write(str(speaker + " " + " ".join(lines))+"\n")
    for lline in lines:
        testutt2spk.write(lline + " "+ speaker + "\n")

    txtfiles = sorted(glob.glob(spkfolder + '/text/*', recursive = False))

    for txtfile in txtfiles:
        tekstfile = open(txtfile, 'r')
        for tline in tekstfile:
            test_trans.write(speaker.replace('_','') +"-"+ tline)

testspk2utt.close()
testutt2spk.close()
test_trans.close()
test_wav_scp.close()

# Shameless copy paste from previous, just replaced with the training/dev set.

testspk2utt = open(sys.argv[2] + '/dev/spk2utt', 'a+',encoding='utf-8')
testutt2spk = open(sys.argv[2] + '/dev/utt2spk', 'a+',encoding='utf-8')
test_trans = open(sys.argv[2] + '/dev/text', 'a+',encoding='utf-8')
test_wav_scp = open(sys.argv[2] + '/dev/wav.scp', 'a+',encoding='utf-8')

for line in speakdev:
    speaker = line.strip()
    spkfolder = srcfolder + speaker + "/wav"
    files = glob.glob(spkfolder + '/*.wav', recursive =False)
    lines = []
    for fline in files:
        filename = fline.rsplit("/",1)[1]
        lines.append(filename.split(".")[0] + " " + dirpath+"/"+fline)
    lines.sort()
    for lline in lines:
        test_wav_scp.write(lline + "\n")
    
    lines = []
    for fline in files:
        filename = fline.rsplit("/",1)[1].split(".")[0]
        lines.append(str(filename))
    lines.sort()
    testspk2utt.write(str(speaker + " " + " ".join(lines))+"\n")
    for lline in lines:
        testutt2spk.write(lline + " "+ speaker + "\n")

    txtfiles = sorted(glob.glob(spkfolder + '/text/*', recursive = False))

    for txtfile in txtfiles:
        tekstfile = open(txtfile, 'r')
        for tline in tekstfile:
            test_trans.write(speaker.replace('_','') +"-"+ tline)




testspk2utt.close()
testutt2spk.close()
test_trans.close()
test_wav_scp.close()


testspk2utt = open(sys.argv[2] + '/train/spk2utt', 'a+',encoding='utf-8')
testutt2spk = open(sys.argv[2] + '/train/utt2spk', 'a+',encoding='utf-8')
test_trans = open(sys.argv[2] + '/train/text', 'a+',encoding='utf-8')
test_wav_scp = open(sys.argv[2] + '/train/wav.scp', 'a+',encoding='utf-8')

for line in speaktrain:
    speaker = line.strip()
    spkfolder = srcfolder + speaker + "/wav"
    files = glob.glob(spkfolder + '/*.wav', recursive =False)
    lines = []
    for fline in files:
        filename = fline.rsplit("/",1)[1]
        lines.append(filename.split(".")[0] + " " + dirpath+"/"+fline)
    lines.sort()
    for lline in lines:
        test_wav_scp.write(lline + "\n")
    
    lines = []
    for fline in files:
        filename = fline.rsplit("/",1)[1].split(".")[0]
        lines.append(str(filename))
    lines.sort()
    testspk2utt.write(str(speaker + " " + " ".join(lines))+"\n")
    for lline in lines:
        testutt2spk.write(lline + " "+ speaker + "\n")

    txtfiles = sorted(glob.glob(spkfolder + '/text/*', recursive = False))

    for txtfile in txtfiles:
        tekstfile = open(txtfile, 'r')
        for tline in tekstfile:
            test_trans.write(speaker.replace('_','') +"-"+ tline)
            

testspk2utt.close()
testutt2spk.close()
test_trans.close()
test_wav_scp.close()


wrtfile.close()
speakall.close()
speaktest.close()
speaktrain.close()
