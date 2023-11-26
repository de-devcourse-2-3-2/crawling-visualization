# 무신사 추천 코디로 보는 패션 트렌드

------------------------------
#### *데브코스 데이터엔지니어링 2기 1차 프로젝트*

------------------------------

## 1. 소개
국내 대표적인 패션 이커머스사 무신사(Musinsa)에서는 다양한 스타일별로 코디 추천과 함께 상품 정보를 제공하고 있다.
본 프로젝트에서는 코디 추천 게시물과 각 코디에 사용된 상품 정보를 크롤링 후 데이터로 저장해
날짜(시간), 계절, 조회수 등을 기준으로 인기 스타일을 파악할 수 있는 장고 웹 프로젝트다.
<br>

## 2. 기술 및 아키텍처
- 프레임워크 및 라이브러리: bs4, selenium, Django, webdriver, psycopg2
- 협업툴 및 DB: git, PostgreSQL
![tech-stack.png](..%2F..%2F%EB%8D%B0%EB%B8%8C%EC%BD%94%EC%8A%A4%ED%8C%8C%EC%9D%BC%2F1stPJ%2Ftech-stack.png)
<br>

## 3. 프로젝트 실행 방법
#### 1) CLI 에 "docker build --tag musinsa-trend:1.0 ." 입력해 도커 이미지를 빌드
#### 2) CLI 에 "docker-compose up -d" 입력
#### 앱 전체 종료 및 관련 자원 삭제를 원할 시 "docker-compose down" 명령 입력

## 4. 결과물 발표 자료 링크
https://www.canva.com/design/DAF0aNXiiIM/bU81GYtIMHKaENQprTVoRg/edit?utm_content=DAF0aNXiiIM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton