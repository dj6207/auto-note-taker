import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("KoboldAI/GPT-Neo-2.7B-Horni")

model = AutoModelForCausalLM.from_pretrained("KoboldAI/GPT-Neo-2.7B-Horni")

text = ("Be me Ze Jun. I want to go get ramen. Lets meet at 5 but gets there at 4:30. Imma go get some corn dogs while I wait.")

encoded_input = tokenizer.encode(text, return_tensors='pt')

# output = model.generate(encoded_input, max_length=200, do_sample=True)
output = model.generate(encoded_input, max_length=200)

words = tokenizer.decode(output[0], skip_special_tokens=True)
print(words)

# from transformers import pipeline
# generator = pipeline('text-generation', model='KoboldAI/GPT-Neo-2.7B-Shinen')
# output = generator("She was staring at me", do_sample=True, min_length=50)
# print(output)

