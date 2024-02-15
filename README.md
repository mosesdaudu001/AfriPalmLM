# AfriPalmLM
The Finetuning of the PalmLM LLM, which is a 1.7B model with multilingual dataset

Process:
* Process Data (Data is processed in `src/data_processing.py`, but not stored on Github because of size - 0.99GB)
* Train Tokenizer (270,000 and 70,000)
* Build Model
* Evaluate Model

Steps To Reproduce
1. `pip install -r requirements`
2. `python src/data_processing`
