# 대시보드_V1[[Link](https://k7-dashboard.herokuapp.com/)]
## Data
- 서울_merged.csv
- 서울법정동.geojson
- TBGIS.geojson

## Project boilerplate

    apps
    ├── ...
    ├── Dashboard               # app project
    │   ├── app.py              # dash application
    │   ├── Procfile            # used for heroku deployment 
    │   ├── setup.sh            # dashobard setup
    │   ├── runtime.txt         # python version
    │   ├── requirements.txt    # project dependecies
    │   └── ...                 
    └── ...

## K7 Project boilerplate_v0.1
    Local
    ├── app.py                  # main.py 
    ├── apps
    │   ├── __init__.py         # package load
    │   ├── login_app.py        # 로그인 화면 구성
    │   ├── home_app.py         # 홈 화면 구성 
    │   ├── cheat_app.py        # 데이터정의서 화면 구성 
    │   ├── eda_app.py          # 클러스터링 화면 구성    
    │   ├── geo_app.py          # 상권분석 화면 구성         
    │   ├── kakao_api.py        # 카카오 api 패키지 load
    ├── resources               # 이미지 데이터
    └── ...
