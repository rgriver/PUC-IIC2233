with open('chatayudantes.iic2233', 'rb') as f:
    data1 = f.read()


temp = []
for i in range(0, len(data1), 4):
    temp.append(sum(data1[i:i+4]))


temp2 = []
for i in temp:
    # print(i, end=' ')
    hundreds = int(i / 100)
    i -= hundreds * 100
    tens = int(i / 10)
    i -= tens * 10
    ones = i
    nums = []
    for j in [hundreds, tens, ones]:
        if j not in [5, 0]:
            nums.append(abs(10 - j))
        else:
            nums.append(abs(5 - j))
    num = nums[0] * 100 + nums[1] * 10 + nums[2]
    # print(num, end=' ')
    num2 = int(str(num)[::-1])
    # print(num2)
    temp2.append(num2)


def get_evil():
    y = 1
    while True:
        num = bin(y)
        num = num.lstrip('0b')
        x = list(num)
        x = [int(j) for j in x]
        s = sum(x)
        y = int(num, 2)
        if s % 2 == 0:
            yield y
        y += 1


def get_prime():
    y = 2
    while True:
        is_prime = True
        n = y // 2
        for i in range(2, n + 1):
            if y % i == 0:
                is_prime = False

        if is_prime:
            yield y
        y += 1


evil = get_evil()
prime = get_prime()

audio_data = []
image_data = []

position = 0
while True:
    if len(audio_data) <= 9523:
        # print(len(audio_data))
        prime_num = next(prime)
        if len(audio_data) == 9523:
            audio_data += temp2[position:position + 260]
            position += 260
        else:
            audio_data += temp2[position:position + prime_num]
            position += prime_num
    evil_num = next(evil)
    if len(temp2[position:]) - evil_num < 0:
        image_data += temp2[position:]
        break
    image_data += temp2[position:position + evil_num]
    position += evil_num


print(len(audio_data))

with open('image.gif', 'wb') as f:
    f.write(bytearray(audio_data))

with open('audio.wav', 'wb') as f:
    f.write(bytearray(image_data))
