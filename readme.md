# FastAPI With MongoDB

> FastAPI와 MongoDB를 사용한 간단한 RestAPI 서버 입니다.


# Tech/Framework Used

|명칭       |버전   |
|---        |---    |
|FastAPI    |0.78.0 |
|MongoDB    |5.0.8  |


# 라이브러리 설치

```bash
python -m venv vnev
> venv/scripts/activate
> pip install fastapi
> pip install pydantic[email]
> pip install python-multipart

# db
> pip install pymysql

# 비동기 서버 실행
> pip install uvicorn

# jwt
> pip install python-jose
> pip install passlib[bcrypt]

# test
> pip install pytest
> pip install requests
```


# DB 설정

- 설정 파일 : `app/config/secrets.json`

## mysql



## MongoDB
- MongoDB Local 접속시 변수 형식
    ```bash
    MONGODB_URL="mongodb://localhost:27017"
    ```
- MongoDB Cloud 접속시 변수 형식
    ```bash
    MONGODB_URL="mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"
    ```


# 실행

## 1. FastAPI 서버 실행

```
> uvicorn app.main:app --reload
```

## 2. 접속

웹브라우저에서 `http://localhost:8000/docs` 주소로 접속


# 테스트 실행

```
> python -m pytest
```