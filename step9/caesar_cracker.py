# caesar_cracker.py
from datetime import datetime


def caesar_cipher_decode(target_text: str) -> dict[int, str]:
    """
    target_text의 모든 가능한 시프트(0~25)에 대해
    대문자/소문자 카이사르 디코딩 결과를 출력하고,
    shift→decoded_text 맵을 반환한다.
    """
    results = {}
    for shift in range(26):
        decoded_chars = []
        for ch in target_text:
            if 'a' <= ch <= 'z':
                # 소문자 디코딩
                offset = (ord(ch) - ord('a') - shift) % 26
                decoded_chars.append(chr(ord('a') + offset))
            elif 'A' <= ch <= 'Z':
                # 대문자 디코딩
                offset = (ord(ch) - ord('A') - shift) % 26
                decoded_chars.append(chr(ord('A') + offset))
            else:
                # 그 외 문자(공백·숫자·구두점)는 그대로
                decoded_chars.append(ch)

        decoded = ''.join(decoded_chars)
        print(f"Shift {shift:2d}: {decoded}")
        results[shift] = decoded

    return results


def main():
    # 1) 암호문 읽기 (현재 스크립트와 같은 디렉토리의 password.txt)
    with open("password.txt", "r", encoding="utf-8") as f:
        cipher_text = f.read().strip()

    print(f"[TEXT] {cipher_text}\n")
    # 2) 모든 시프트 결과 보기
    candidates = caesar_cipher_decode(cipher_text)

    # 3) 눈에 띄는 해독 결과(예: Shift 19 → I love Mars)를 선택
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

    result = candidates[sel]
    # 4) 선택된 결과를 파일에 저장
    with open("result.txt", "w", encoding="utf-8") as out:
        out.write(result)

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    print(f"[SAVED] Shift {sel} → {result} 을 result.txt에 저장했습니다.")

if __name__ == "__main__":
    main()
