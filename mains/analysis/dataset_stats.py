from data_io.instructions import get_all_instructions, tokenize_instruction, get_word_to_token_map
from data_io.env import load_path

import parameters.parameter_server as P

import numpy as np


def path_length(path):
    dst = 0
    for p1, p2 in zip(path[:-1], path[1:]):
        dst += np.linalg.norm(p2-p1)
    return dst


def analyze_instruction_set(name, iset, corpus, merge_len):
    token_lengths = []
    demo_lengths = []
    token2word, word2token = get_word_to_token_map(corpus)

    for e, instr_sets in iset.items():
        segs = instr_sets[0]["instructions"]
        if len(segs) > 0:
            full_path = load_path(e)
        for seg in segs:
            if seg["merge_len"] != merge_len:
                continue
            tok_i = tokenize_instruction(seg['instruction'], word2token)
            start_idx = seg["start_idx"]
            end_idx = seg["end_idx"]
            seg_path = full_path[start_idx:end_idx]
            demo_len = path_length(seg_path)

            demo_lengths.append(demo_len)
            token_lengths.append(len(tok_i))

    avg_tok_len = sum(token_lengths) / len(token_lengths)
    avg_pth_len = sum(demo_lengths) * 4.7 / (len(demo_lengths) * 1000)

    print("Dataset: ", name)
    print(" {}  &  {}  &  {:.2f}  &  {:.2f}".format(len(iset), len(token_lengths), avg_tok_len, avg_pth_len))
    #print(f"{len(iset)}  &  {len(token_lengths)}  &  {avg_tok_len}  &  {avg_pth_len}")

    #print("Dataset: ", name)
    #print("   num paragraphs: ", len(set)),
    #print("   num segs:", len(token_lengths))
    #print("   avg token len: ", avg_tok_len)
    #print("   avg traj len: ", avg_pth_len)

dev_small_envs =  [6168, 6169, 6191, 6192, 6296, 6299, 6415, 6419, 6567, 6569, 6632, 6634, 6825, 6827, 6856, 6857, 6876, 6878, 6917, 6919]
test_small_envs = [6045, 6047, 6101, 6103, 6255, 6257, 6381, 6382, 6406, 6408, 6450, 6451, 6540, 6542, 6740, 6742, 6757, 6758, 6851, 6853]

def analyze_lani():
    P.initialize_experiment()

    train_i, dev_i, text_i, corpus = get_all_instructions()

    train_i_lani = {k:v for k,v in train_i.items() if int(k) < 6000}
    dev_i_lani = {k:v for k,v in dev_i.items() if int(k) < 6000}
    test_i_lani = {k:v for k,v in text_i.items() if int(k) < 6000}

    train_i_real = {k:v for k,v in train_i.items() if int(k) >= 6000}
    dev_i_real = {k:v for k,v in dev_i.items() if int(k) >= 6000}
    test_i_real = {k:v for k,v in text_i.items() if int(k) >= 6000}

    test_i_small = {k:v for k,v in test_i_real.items() if int(k) in test_small_envs}
    dev_i_small = {k:v for k,v in dev_i_real.items() if int(k) in dev_small_envs}

    all_i_real = {**train_i_real, **dev_i_real, **test_i_real}

    analyze_instruction_set("Lani Train 1Seg", train_i_lani, corpus, merge_len=1)
    analyze_instruction_set("Lani Dev 1Seg", dev_i_lani, corpus, merge_len=1)
    analyze_instruction_set("Lani Test 1Seg", test_i_lani, corpus, merge_len=1)
    analyze_instruction_set("Lani Train 2Seg", train_i_lani, corpus, merge_len=2)
    analyze_instruction_set("Lani Dev 2Seg", dev_i_lani, corpus, merge_len=2)
    analyze_instruction_set("Lani Test 2Seg", test_i_lani, corpus, merge_len=2)

    analyze_instruction_set("Real Train 1Seg", train_i_real, corpus, merge_len=1)
    analyze_instruction_set("Real Dev 1Seg", dev_i_real, corpus, merge_len=1)
    analyze_instruction_set("Real Test 1Seg", test_i_real, corpus, merge_len=1)
    analyze_instruction_set("Real Train 2Seg", train_i_real, corpus, merge_len=2)
    analyze_instruction_set("Real Dev 2Seg", dev_i_real, corpus, merge_len=2)
    analyze_instruction_set("Real Test 2Seg", test_i_real, corpus, merge_len=2)

    #analyze_instruction_set("Real Test 1Seg", test_i_real, corpus, merge_len=1)
    #analyze_instruction_set("Real Test 2Seg", test_i_real, corpus, merge_len=2)
    #analyze_instruction_set("Small Test 1Seg", test_i_small, corpus, merge_len=1)
    #analyze_instruction_set("Small Test 2Seg", test_i_small, corpus, merge_len=2)
    analyze_instruction_set("Small Dev 1Seg", dev_i_small, corpus, merge_len=1)
    analyze_instruction_set("Small Dev 2Seg", dev_i_small, corpus, merge_len=2)
    analyze_instruction_set("Small Dev 1Seg", dev_i_small, corpus, merge_len=1)
    analyze_instruction_set("Small Dev 2Seg", dev_i_small, corpus, merge_len=2)


    print("ding")

if __name__ == "__main__":
    analyze_lani()
