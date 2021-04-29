import requests
from bs4 import BeautifulSoup

url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"  # 크롤링할 url
parameters = {"masterType": "brch",
              "detailType": "area",
              "brchNo": "7022",
              "firstAt": "N",
              "brchNo1": "7022",
              "crtDe": "20210421",
              "playDe": "20210421"}  # url의 파라미터 값
response = requests.post(url, data=parameters).json()  # json 응답

movie_response = response['megaMap']['movieFormList']  # 영화 정보를 뽑는다.


def split_movies_by_no(response):
    movie_no_list = get_movie_no_list(response)
    for movie_no in movie_no_list:
        movies = [item for item in response if item["movieNo"] == movie_no]
        title = movies[0]["movieNm"]  # 영화 타이틀
        timetable = get_time_table(movies)  # 영화 시간정보
        print(title, timetable, "\n")  # 영화 정보 출력


def get_movie_no_list(response):  # movieNo로 영화를 구분하여 출력하는 함수
    movie_no_list = []  # 변수 movie_no_list 선언
    for item in response:
        movie_no = item["movieNo"]  # 변수 movie_no 선언
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)  # movie_no_list에 movie_no의 값을 입력
    return movie_no_list  # movie_no_list 리턴


def get_time_table(movies):
    tuples = []  # 변수 tuples 선언
    for movie in movies:
        time = movie["playStartTime"]  # 영화 상영 시작 시간
        seats = movie["restSeatCnt"]  # 영화 남은 좌석
        tuple = (time, seats)  # 상영 시간과 남은 좌석을 변수 tuple에 입력
        tuples.append(tuple)
    return tuples  # tuples 값 리턴


split_movies_by_no(movie_response)  # 영화 정보 출력
