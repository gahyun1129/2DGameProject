file_path = 'resource/txt/Hitter.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    for content in file:
        print(content.strip())

print(content)