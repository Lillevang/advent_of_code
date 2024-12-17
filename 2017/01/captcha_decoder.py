
def read_input(path='input'):
    with open(path, 'r') as file:
        return file.readline().strip()


def captcha1(sequence: str) -> int:
    return sum(int(sequence[i]) 
               for i in range(len(sequence)) 
               if sequence[i] == sequence[(i+1)%len(sequence)])

def captcha2(sequence: str) -> int:
    N = len(sequence) // 2
    return sum(int(a) for a, b in zip(sequence, sequence[N:] + sequence[:N]) if a == b)


if __name__ == "__main__":
    sequence = read_input()
    print(captcha1(sequence))
    print(captcha2(sequence))