import requests
from bs4 import BeautifulSoup

#대구(칠성로)메가박스 url
url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"

parameters = {"masterType": "brch",
              "detailType": "area",
              "brchNo": "7022",
              "firstAt": "N",
              "brchNo1": "7022",
              "crtDe": "20210421",
              "playDe": "20210421"}

response = requests.post(url, data=parameters).json()
#json형태로 파라미터를 전송하여 데이터를 받음

movie_response = response['megaMap']['movieFormList']
#megaMap==상영관
#movieFormList==상영목록

def get_movie_no_list(response):
    movie_no_list = []  #상영목록 배열생성
    for item in response:   #칠성로의 상영목록만큼 반복
        movie_no = item["movieNo"] #movieNo == 영화번호
        if movie_no not in movie_no_list: #상영목록에 영화가없다면 movie_no_list에  movie_no 넣기
            movie_no_list.append(movie_no) #리스트에 영화번호를 추가
    return movie_no_list


def get_time_table(res):
    tuples = []
    for movie in res:
        time = movie["playStartTime"]  #time==시간
        seats = movie["restSeatCnt"]   #seats==좌석
        tuple = (time, seats)          #시간과 좌석을 튜플로 생성          /    리스트는 배열안의 값이 생성,수정,삭제가 되지만 튜플은 값을 바꿀 수 없다   https://wikidocs.net/15
        tuples.append(tuple)           #튜플에 한 행을 추가(값을 추가)
    return tuples

def split_movies_by_no(response):
    movie_no_list = get_movie_no_list(response) #해당상영목록 받아옴
    for movie_no in movie_no_list: #상영목록만큼 반복
        movies = [item for item in response if item["movieNo"] == movie_no]  # 크롤링을 했을때 우리가 필요한 자료들만 받아 오면 되는데 movieNo 를 찾기위해서 for문을 작성한건데
        #movieNo 를 찾기위해서 저 경로들을 지나온거라고 이해하면 편함
        title = movies[0]["movieNm"] #movieNm == 영화제목

        timetable = get_time_table(movies) #튜플을 사용한게 맞고 튜플은 리스트 처럼 요소를 일렬로 저장을
        #간단하게 해주기 위해서 사용하는데 여기서 튜플을 사용한 이유는 timetable안에 저장되는 요소의 값을
        #변경,추가,삭제를 할 계획이 없는 읽기전용 리스트 라서 사용을 했음
        #튜플은 안에 값을 변경,추가,삭제 가 불가능함

        print(title, timetable, "\n")      #제목과 tuples를 합해 출력



split_movies_by_no(movie_response)     #상영관과 상영목록 정보를 넘겨주며 함수 실행
