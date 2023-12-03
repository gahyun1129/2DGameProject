def print_in_chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        chunk = lst[i:i + chunk_size]
        print(chunk)

# 예시 리스트
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# 4개씩 끊어서 출력
print_in_chunks(my_list, 4)

print(my_list[13:14])