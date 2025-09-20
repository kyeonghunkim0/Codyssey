import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup


def get_kbs_headlines(url):
    """
    지정된 KBS 뉴스 URL에서 주요 헤드라인을 가져와 출력하는 함수.
    """
    try:
        # requests.get() 함수로 서버에 웹페이지의 HTML 원본을 요청합니다.
        # 웹 스크래핑의 첫 단계인 웹 페이지의 소스 코드를 가져오는 과정입니다.
        response = requests.get(url)

        # 서버가 404, 500과 같은 잘못된 상태 코드를 반환하면 HTTPError 예외를 발생시킵니다.
        # 이 검증 과정을 통해 스크립트가 유효하지 않은 페이지로 계속 진행하는 것을 방지합니다.
        response.raise_for_status()

        # BeautifulSoup은 HTML 텍스트를 파싱하여 검색 가능한 트리 구조로 만듭니다.
        # 이를 통해 태그, 클래스, ID 등을 이용해 특정 요소를 쉽게 찾을 수 있습니다.
        soup = BeautifulSoup(response.text, 'html.parser')

        # 'box head-line main-head-line main-page-head-line' 클래스는
        # 모든 상단 뉴스 기사를 담고 있는 주 컨테이너를 식별하는 고유한 값입니다.
        main_container = soup.find('div', class_='box head-line main-head-line main-page-head-line')

        # 컨테이너를 찾지 못했다면 웹사이트 구조가 변경되었을 가능성이 높습니다.
        # 이 확인 절차는 예기치 않은 페이지 레이아웃 변화에 대응하는 데 중요합니다.
        if not main_container:
            print('지정된 클래스 이름을 가진 메인 헤드라인 컨테이너를 찾을 수 없습니다. 스크립트를 종료합니다.')
            return

        print('KBS 뉴스 헤드라인 목록을 추출합니다:')

        # 1. 메인 뉴스 기사를 찾아 처리하는 코드 블록.
        # 'main-news-wrapper' 클래스는 가장 중요한 단일 뉴스 기사를 포함하는 섹션입니다.
        main_news_wrapper = main_container.find('div', class_='main-news-wrapper')
        if main_news_wrapper:
            # 'a' 태그에 'main-news box-content' 클래스가 붙어있어 기사 링크를 나타냅니다.
            # 이 요소를 통해 기사 제목과 링크에 직접 접근합니다.
            main_news_tag = main_news_wrapper.find('a', class_='main-news box-content')
            if main_news_tag:
                # 'p' 태그의 'title' 클래스는 뉴스 기사의 제목 텍스트를 담고 있습니다.
                # get_text(strip=True) 함수를 사용하여 불필요한 공백과 줄바꿈 문자를 제거합니다.
                title_tag = main_news_tag.find('p', class_='title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    # 상대 경로로 된 링크에 도메인을 결합하여 완전한 URL을 구성합니다.
                    link = 'http://news.kbs.co.kr' + main_news_tag.get('href', '')
                    print(f'1. [주요뉴스] {title}')
                    print(f'   링크: {link}\n')

        # 2. 서브 뉴스 기사들을 찾아 처리하는 코드 블록.
        # 'small-sub-news-wrapper' 클래스는 여러 개의 작은 뉴스 기사 목록을 담고 있습니다.
        sub_news_wrapper = main_container.find('div', class_='small-sub-news-wrapper')
        if sub_news_wrapper:
            # find_all() 함수는 조건에 맞는 모든 'a' 태그를 리스트 형태로 반환합니다.
            # 이 리스트를 반복문으로 돌면서 각 서브 뉴스를 처리할 수 있습니다.
            sub_news_tags = sub_news_wrapper.find_all('a', class_='box-content')

            # 메인 뉴스가 1번으로 시작했으므로, 서브 뉴스는 2번부터 번호를 매깁니다.
            for index, sub_news_tag in enumerate(sub_news_tags, 2):
                title_tag = sub_news_tag.find('p', class_='title')
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = 'http://news.kbs.co.kr' + sub_news_tag.get('href', '')
                    print(f'{index}. {title}')
                    print(f'   링크: {link}\n')

    except requests.exceptions.RequestException as e:
        # requests 라이브러리에서 발생하는 네트워크 관련 오류(예: DNS 오류, 연결 거부)를 처리합니다.
        print(f'웹페이지를 가져오는 중 네트워크 오류가 발생했습니다: {e}')
    except Exception as e:
        # 위에서 잡지 못한 모든 종류의 일반적인 오류(예: 예상치 못한 HTML 구조 변경)를 처리합니다.
        print(f'스크립트 실행 중 알 수 없는 오류가 발생했습니다: {e}')


def get_danawa_product_info(keyword):
    """
    다나와에서 검색어를 이용해 상품 목록과 가격을 가져와 출력하는 함수.

    Args:
        keyword (str): 검색할 상품 키워드.
    """
    try:
        # 검색어를 URL에 포함시키기 위해 인코딩합니다.
        encoded_keyword = requests.utils.quote(keyword)
        url = f"http://search.danawa.com/dsearch.php?query={encoded_keyword}"

        # 웹페이지에 접속하여 HTML 소스를 가져옵니다.
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()

        # HTML을 파싱합니다.
        soup = BeautifulSoup(response.text, 'html.parser')

        # 상품 목록을 담고 있는 div 태그를 찾습니다.
        # 이 클래스 이름은 상품 목록 페이지의 구조에 따라 달라질 수 있습니다.
        product_list = soup.find('div', class_='main_prodlist main_prodlist_list')

        if not product_list:
            print('상품 목록을 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.')
            return

        print(f"--- 다나와 '{keyword}' 검색 결과 ---")

        # 목록 안의 모든 개별 상품을 나타내는 li 태그를 찾습니다.
        products = product_list.find_all('li', class_='prod_item')

        for index, product in enumerate(products, 1):
            # 상품명을 담고 있는 a 태그를 찾습니다.
            product_name_tag = product.find('p', class_='prod_name').find('a')

            # 가격 정보를 담고 있는 a 태그를 찾습니다.
            price_tag = product.find('p', class_='price_sect').find('a')

            if product_name_tag and price_tag:
                product_name = product_name_tag.get_text(strip=True)
                product_price = price_tag.get_text(strip=True)

                print(f"{index}. 상품명: {product_name}")
                print(f"   가격: {product_price}\n")

    except requests.exceptions.RequestException as e:
        print(f'네트워크 오류 발생: {e}')
    except Exception as e:
        print(f'알 수 없는 오류가 발생했습니다: {e}')


if __name__ == '__main__':
    # KBS 뉴스
    KBS_URL = "https://news.kbs.co.kr/news/pc/main/main.html"
    get_kbs_headlines(KBS_URL)

    # 보너스
    search_keyword = '게이밍 마우스'
    get_danawa_product_info(search_keyword)


