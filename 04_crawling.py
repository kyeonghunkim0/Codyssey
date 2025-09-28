# crawling_KBS.py (최종 완성본)

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_naver_user_info(user_id, user_pw):
    '''
    셀레니움을 사용해 네이버에 로그인하여 닉네임과 이메일 주소를 가져오는 함수
    '''
    driver = None
    crawled_data = []

    try:
        service = Service()
        options = Options()
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 10)

        # 네이버 메인 페이지로 이동 및 로그인 페이지로 전환
        driver.get('http://naver.com')
        login_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'MyView-module__link_login___HpHMW'))
        )
        login_button.click()

        # 아이디와 비밀번호 입력
        id_input = wait.until(EC.presence_of_element_located((By.NAME, 'id')))
        pw_input = driver.find_element(By.NAME, 'pw')

        driver.execute_script('arguments[0].value = arguments[1];', id_input, user_id)
        driver.execute_script('arguments[0].value = arguments[1];', pw_input, user_pw)

        # 로그인 버튼 최종 클릭
        driver.find_element(By.ID, 'log.login').click()

        # --- 크롤링 시작 ---

        # 닉네임 찾기
        nickname_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="MyView-module__nickname"]'))
        )
        nickname = nickname_element.text
        crawled_data.append(f'로그인된 닉네임: {nickname}')

        # 이메일 주소 찾기
        email_element = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[class*="MyView-module__desc_email"]')
            )
        )
        email = email_element.text
        crawled_data.append(f'이메일 주소: {email}')

    except TimeoutException:
        error_message = '로그인 실패 또는 정보를 찾을 수 없습니다 (시간 초과)'
        crawled_data.append(error_message)
        if driver:
            driver.save_screenshot('error_screenshot.png')
    except Exception as e:
        error_message = f'알 수 없는 오류 발생: {e}'
        crawled_data.append(error_message)
    finally:
        if driver:
            driver.quit()

    return crawled_data


# 메인 실행 블록
if __name__ == '__main__':
    my_id = 'MY_ID'
    my_pw = 'MY_PASSWORD'

    result_list = get_naver_user_info(my_id, my_pw)

    print('\n--- 최종 크롤링 결과 ---')
    print(result_list)