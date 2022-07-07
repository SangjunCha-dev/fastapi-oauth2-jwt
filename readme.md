# FastAPI With JWT

> FastAPI를 사용한 간단한 로그인 RestAPI 서버 입니다.


---

# Tech/Framework Used

|명칭       |버전   |
|---        |---    |
|FastAPI    |0.78.0 |
|MariaDB    |10.8   |
|Python	    |3.9.12 |


---

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


---

# DB 설정

- 설정 파일 위치
```
/app/config/secrets.json
/db/.env
```


---

# 실행

## 1-1. FastAPI 서버 실행

```
> uvicorn app.main:app --reload
```

## 1-2. docker-compose 실행

- docker container 실행
    ```bash
    > docker-compose up -d --build
    ```
- docker container 종료
    ```bash
    > docker-compose down
    ```

## 2. Swagger 접속

웹브라우저에서 `http://localhost:8000/docs` 주소로 접속


---

## 3. FastAPI 서버 테스트 실행

```
> docker-compose exec fastapi01 pytest app/
```