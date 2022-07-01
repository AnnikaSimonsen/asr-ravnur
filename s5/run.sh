#!/bin/bash

# Modified by Egil Hofgaard
# Heavily influenced by the TEDLIUM r3 script and mini_librispeech
# Apache 2.0

# Load the paths

. ./path.sh || exit 1

# Select the engine to run the scripts
. ./cmd.sh || exit 1

# Number of jobs, don't select more than you have cores.
njobs=15
# Start stage and stop stage
stage=1
stopstage=15

# Check the arguments 
. utils/parse_options.sh || exit 1

# Data Preperation
if [ $stage -le 0 ]; then
	local/download_dataset.sh
	ln -sf ../../wsj/s5/steps steps
	ln -sf ../../wsj/s5/utils utils
fi

if [ $stage -le 1 ]; then
	local/ravn_data_prep.sh
	local/ravn_prepare_dict.sh
fi



if [ $stage -le 2 ] && [ $stopstage -ge 2 ]; then
	echo "Stage 2"
	utils/prepare_lang.sh data/local/dict_nosp  "!SIL" data/local/lang_nosp data/lang_nosp
fi


if [ $stage -le 4 ] && [ $stopstage -ge 4 ]; then

	echo "Stage 4"
	
	local/format_lms.sh
fi

if [ $stage -le 6 ] && [ $stopstage -ge 6 ]; then
  echo "Stage 6"
  for set in test dev train; do
    dir=data/$set
    steps/make_mfcc.sh --nj $njobs --cmd "$train_cmd" $dir
    steps/compute_cmvn_stats.sh $dir
  done

  utils/fix_data_dir.sh data/test
  utils/fix_data_dir.sh data/train
  utils/fix_data_dir.sh data/dev
fi
if [ $stage -le 7 ] && [ $stopstage -ge 7 ]; then
  echo "Stage 7"
  utils/subset_data_dir.sh --shortest data/train 10000 data/train_10kshort
  utils/data/remove_dup_utts.sh 10 data/train_10kshort data/train_10kshort_nodup
fi

if [ $stage -le 8 ] && [ $stopstage -ge 8 ]; then
  echo "Stage 8"
  steps/train_mono.sh --nj $njobs --cmd "$train_cmd" \
    data/train_10kshort_nodup data/lang_nosp exp/mono
fi

if [ $stage -le 9 ] && [ $stopstage -ge 9 ]; then
  echo "Stage 9"
  steps/align_si.sh --nj $njobs --cmd "$train_cmd" \
    data/train data/lang_nosp exp/mono exp/mono_ali
  steps/train_deltas.sh --cmd "$train_cmd" \
    2500 30000 data/train data/lang_nosp exp/mono_ali exp/tri1
fi

if [ $stage -le 10 ] && [ $stopstage -ge 10 ]; then
  echo "Stage 10"
  utils/mkgraph.sh data/lang_nosp exp/tri1 exp/tri1/graph_nosp

  for dset in dev test; do
    steps/decode.sh --nj $njobs --cmd "$decode_cmd"  --num-threads 4 \
      exp/tri1/graph_nosp data/${dset} exp/tri1/decode_nosp_${dset}
    steps/lmrescore_const_arpa.sh  --cmd "$decode_cmd" data/lang_nosp data/lang_nosp_rescore \
       data/${dset} exp/tri1/decode_nosp_${dset} exp/tri1/decode_nosp_${dset}_rescore
  done
fi

if [ $stage -le 11 ] && [ $stopstage -ge 11 ]; then
  echo "Stage 11"
  steps/align_si.sh --nj $njobs --cmd "$train_cmd" \
    data/train data/lang_nosp exp/tri1 exp/tri1_ali

  steps/train_lda_mllt.sh --cmd "$train_cmd" \
    3000 40000 data/train data/lang_nosp exp/tri1_ali exp/tri2
fi

if [ $stage -le 12 ] && [ $stopstage -ge 12 ]; then
  echo "Stage 12"
  utils/mkgraph.sh data/lang_nosp exp/tri2 exp/tri2/graph_nosp
  for dset in dev test; do
    steps/decode.sh --nj $njobs --cmd "$decode_cmd"  --num-threads 4 \
      exp/tri2/graph_nosp data/${dset} exp/tri2/decode_nosp_${dset}
    steps/lmrescore_const_arpa.sh  --cmd "$decode_cmd" data/lang_nosp data/lang_nosp_rescore \
       data/${dset} exp/tri2/decode_nosp_${dset} exp/tri2/decode_nosp_${dset}_rescore
  done
fi

if [ $stage -le 13 ] && [ $stopstage -ge 13 ]; then
  echo "Stage 13"
  steps/get_prons.sh --cmd "$train_cmd" data/train data/lang_nosp exp/tri2
  utils/dict_dir_add_pronprobs.sh --max-normalize true \
    data/local/dict_nosp exp/tri2/pron_counts_nowb.txt \
    exp/tri2/sil_counts_nowb.txt \
    exp/tri2/pron_bigram_counts_nowb.txt data/local/dict
fi

if [ $stage -le 14 ] && [ $stopstage -ge 14 ]; then
  echo "Stage 14"
  utils/prepare_lang.sh data/local/dict "!SIL" data/local/lang data/lang
  cp -rT data/lang data/lang_rescore
  cp data/lang_nosp/G.fst data/lang/
  cp data/lang_nosp_rescore/G.carpa data/lang_rescore/

  utils/mkgraph.sh data/lang exp/tri2 exp/tri2/graph

  for dset in dev test; do
    steps/decode.sh --nj $njobs --cmd "$decode_cmd"  --num-threads 4 \
      exp/tri2/graph data/${dset} exp/tri2/decode_${dset}
    steps/lmrescore_const_arpa.sh --cmd "$decode_cmd" data/lang data/lang_rescore \
       data/${dset} exp/tri2/decode_${dset} exp/tri2/decode_${dset}_rescore
  done
fi

if [ $stage -le 15 ] && [ $stopstage -ge 15 ]; then
  echo "Stage 15"
  steps/align_si.sh --nj $njobs --cmd "$train_cmd" \
    data/train data/lang exp/tri2 exp/tri2_ali

  steps/train_sat.sh --cmd "$train_cmd" \
    7000 70000 data/train data/lang exp/tri2_ali exp/tri3

  utils/mkgraph.sh data/lang exp/tri3 exp/tri3/graph

  for dset in dev test; do
    steps/decode_fmllr.sh --nj $njobs --cmd "$decode_cmd"  --num-threads 4 \
      exp/tri3/graph data/${dset} exp/tri3/decode_${dset}
    steps/lmrescore_const_arpa.sh --cmd "$decode_cmd" data/lang data/lang_rescore \
       data/${dset} exp/tri3/decode_${dset} exp/tri3/decode_${dset}_rescore
  done
fi

# Removes segments that cannot be aligned, up to here takes less than 1 hour with 15 cores
if [ $stage -le 16 ] && [ $stopstage -ge 16 ]; then
  local/run_cleanup_segmentation.sh

fi

# You need a dedicated GPU with at least 16 GB of RAM for this stage
if [ $stage -le 17 ] && [ $stopstage -ge 17 ]; then
  local/chain/tuning/run_tdnn_1j.sh

fi  




echo "$0: success."
exit 0

