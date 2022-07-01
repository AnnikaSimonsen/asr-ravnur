# asr-ravnur

Currently there is a s5 version for kaldi. (https://github.com/kaldi-asr/kaldi)

To use, install Kaldi, make a subfolder under egs add this s5 folder there, check path.sh if it's correct and the run the run.sh. (https://kaldi-asr.org/doc/install.html , try the yesno model to learn how it works.)

It is using a mixture of the TEDLIUM scripts and mini-librispeech scripts.

The final DNN model can be exported and used with Vosk-API (https://github.com/alphacep/vosk-api)

https://ravn.fo contains the datasets and models for ASR.

The scripts for datapreperation will be added soon.
