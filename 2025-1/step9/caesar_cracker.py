# caesar_cracker.py

import string
from datetime import datetime

def caesar_cipher_decode(target_text: str) -> dict[int, str]:
    results = {}
    for shift in range(26):
        decoded_chars = []
        for ch in target_text:
            if 'a' <= ch <= 'z':
                offset = (ord(ch) - ord('a') - shift) % 26
                decoded_chars.append(chr(ord('a') + offset))
            elif 'A' <= ch <= 'Z':
                offset = (ord(ch) - ord('A') - shift) % 26
                decoded_chars.append(chr(ord('A') + offset))
            else:
                decoded_chars.append(ch)
        decoded = ''.join(decoded_chars)
        print(f"Shift {shift:2d}: {decoded}")
        results[shift] = decoded
    return results

def main():
    # 1) Read password.txt
    with open("password.txt", "r", encoding="utf-8") as f:
        cipher_text = f.read().strip()

    print(f"[TEXT] {cipher_text}\n")
    # 2) Print all of shift's result
    candidates = caesar_cipher_decode(cipher_text)

    # 3) Input shift
    sel = None
    while sel is None:
        try:
            num = int(input("\n해독된 올바른 Shift 번호(0~25)를 입력하세요: "))
            if 0 <= num < 26:
                sel = num
            else:
                print("0에서 25 사이 숫자를 입력해주세요.")
        except ValueError:
            print("숫자 형태로 입력해주세요.")

    # 4) Save result from select shift
    result = candidates[sel]
    with open("result.txt", "w", encoding="utf-8") as out:
        out.write(result)

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    print(f"[SAVED] Shift {sel} → {result} 을 result.txt에 저장했습니다.")

if __name__ == "__main__":
    main()
