# https://zh.wikipedia.org/wiki/%E6%95%B4%E6%95%B8%E5%88%86%E6%8B%86
def overall_spin_off(max_length):
    num_arr = [1] * (max_length + 1)
    for i in range(max_length):
        for j in range(max_length):
            if j < i:
                continue
            num_arr[j] += num_arr[j - 1]

    for i in range(max_length):
        print(f'{i+3}: {num_arr[i]}')


if __name__ == "__main__":
    max_length = 5
    overall_spin_off(max_length)
