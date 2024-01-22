import random

random.seed(42)

# cut lines from a dataset to create a smaller dataset
def sample_lines(input_file, output_file, num_lines):
    with open(input_file, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()

    num_lines = min(num_lines, len(all_lines))
    sampled_lines = random.sample(all_lines, num_lines)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(sampled_lines)

num_lines = 5000

source_file = "dataSets/kosarak10k.txt"
output_file = "dataSets5k/KOSARAK5k.txt"

sample_lines(source_file, output_file, num_lines)

source_file = "dataSets/BIBLE.txt"
output_file = "dataSets5k/BIBLE5k.txt"

sample_lines(source_file, output_file, num_lines)

source_file = "dataSets/LEVIATHAN.txt"
output_file = "dataSets5k/LEVIATHAN5K.txt"

sample_lines(source_file, output_file, num_lines)
