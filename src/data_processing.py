import os

from datasets import load_dataset

lang = ['afaanoromoo', 'amharic', 'gahuza', 'hausa', 'igbo', 'pidgin', 'somali', 'swahili', 'tigrinya', 'yoruba']

for lan in lang:
  train_dataset = load_dataset("castorini/afriberta-corpus", lan, split="train")
  test_dataset = load_dataset("castorini/afriberta-corpus", lan, split="test")

  # Extract the text data from the dataset
  train_data = train_dataset['text']
  test_data = test_dataset['text']


  train_folder = "data/train"
  test_folder = "data/eval"


  if not os.path.exists(train_folder):
      os.makedirs(train_folder)
      os.makedirs(test_folder)
      print('Folders created successfully!!')
  else:
      print("Directory already exists.")


  # Define the path to save the text file
  output_train_path = f"{train_folder}/train.{lan}"
  output_test_path = f"{test_folder}/eval.{lan}"

  # Write the text data to the text file
  with open(output_train_path, "w", encoding="utf-8") as file:
      for text in train_data:
          file.write(text + "\n")
  with open(output_test_path, "w", encoding="utf-8") as file:
      for text in test_data:
          file.write(text + "\n")

def combine_dataset(typ):
  # Directory containing the text files
  directory = f"data/{typ}"

  # Output file name
  output_file = f"data/{typ}/all_{typ}.txt"

  # Open the output file in write mode
  with open(output_file, 'w') as outfile:
      # Iterate over each file in the directory
      for filename in os.listdir(directory):
          # Open the file in read mode and read its content
          with open(os.path.join(directory, filename), 'r') as infile:
              content = infile.read()
              # Write the content to the output file
              outfile.write(content)
              # Add a newline character after each file's content
              outfile.write('\n')
  print(f"length of {typ} dataset in characters: ", len(output_file))

# combine_dataset("train")
combine_dataset("eval")
