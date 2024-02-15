
import os
import nltk
from tqdm import tqdm
import unicodedata
import glob
from random import sample

def sample_and_make_tempfile(sentences_dir, num_files):
    """ Use the set of files containing a sentence per line,
    sample num_files out of those and save as a temp file """

    sentence_files = glob.glob(sentences_dir + "/*.txt")

    # sample num_files
    sampled_files=sample(sentence_files, num_files)

    print("sampled files:")
    print(sampled_files)

    #read all the lines from sampled files and save to a list
    all_lines = []
    for filename in sampled_files:
        with open(filename) as f:
            lines = f.read().splitlines()

        all_lines.extend(lines)

    print("number of lines sampled:", len(all_lines))

    #combine into a single file and save
    data_dir = sentences_dir.rpartition("/")[0]
    data_dir = data_dir.rpartition("/")[0]
    data_dir = f"{data_dir}/combined"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    file_dir = sentences_dir.rpartition("/")[-1]
    tempfile_path = os.path.join(data_dir, f"{file_dir}-temp.txt")
    with open(tempfile_path, "w") as f:


        f.writelines(all_lines)
    print("Wrote to ", tempfile_path)
    return tempfile_path

def get_training_corpus(data, chunksize):
    for start_idx in range(0, len(data), chunksize):
      samples = data[start_idx : start_idx+chunksize]
      yield samples

def make_sentence_files(dataset, data_dir = "jp_sentences"):
    """
    Make a sentence per line files, chuncsize sentences per file"""
    chunksize = 1000000
    # make sure data dir exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for chunk_ind, sentence_chunk in enumerate(get_training_corpus(dataset, chunksize)):

        # new file for each chunk
        filename = "sent_{}.txt".format(chunk_ind)
        filepath = os.path.join(data_dir, filename)

        print("writing to ", filepath)

        with open(filepath, "w") as f:

            lines = [
                line
                for line in sentence_chunk.splitlines()
                if (len(line.split()) > 5 and not line.isspace())
            ]


            f.writelines(lines)


dir = "data/train"
comb_dir = "combined_dataset/individual"

for file_name in os.listdir(dir):
    filepath = os.path.join(dir, file_name)
    data_dir = f"{comb_dir}/{file_name}-v1"
    with open(filepath, 'r') as infile:
        content = infile.read()
        # print(len(content))
        make_sentence_files(content, data_dir = data_dir)

for file_name in os.listdir(comb_dir):
  file_path = os.path.join(comb_dir, file_name)
  # print(file_name)
  tempfile_path = sample_and_make_tempfile(
      sentences_dir = file_path,
      num_files = 5)

dir = "combined_dataset/combined"

temp_path = "combined_dataset/combined_temp.txt"

for file_name in os.listdir(dir):
  file_path = os.path.join(dir, file_name)
  with open(file_path, 'r') as infile:
      content = infile.read()
  with open(temp_path, "w") as f:
      f.writelines(content + '\n')
  print("Wrote to ", temp_path)
  # return tempfile_path

with open("combined_dataset/combined_temp.txt", 'r') as f:
  text = f.read()

print(len(text))
print(len(sorted(list(set(text)))))

"""## Train Tokenizer"""

# def get_training_corpus(data, chunksize):
#     for start_idx in range(0, len(data), chunksize):
#       samples = data[start_idx : start_idx+chunksize]
#       yield samples

from transformers import AutoTokenizer

with open("combined_dataset/combined_temp.txt", 'r') as f:
  text = f.read()

training_corpus = get_training_corpus(text, chunksize = 1000000)
old_tokenizer = AutoTokenizer.from_pretrained("DAMO-NLP-MT/polylm-1.7b")

new_tokenizer = old_tokenizer.train_new_from_iterator(text, 70000)
new_tokenizer.save_pretrained("PalmLM-70000-tokenizer")
