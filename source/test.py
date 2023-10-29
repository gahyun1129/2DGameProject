file_path = 'resource/txt/Hitter.txt'

hitter_player = []

with open(file_path, 'r', encoding='utf-8') as file:
    for content in file:
        content = content.strip()
        hitter_player.append(content.split())
        print(content)

print(hitter_player)