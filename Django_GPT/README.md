# Django GPT

Django + Hugging Face pipeline을 이용한 AI 웹 서비스 과제입니다.
텍스트를 입력하면 감정 분석, 문서 요약, 유해 표현 분석을 각각 실행할 수 있고,
챌린지로 세 모델을 체이닝하는 복합 분석 기능도 구현했습니다.

## 기능

| 탭 | URL | 설명 | 접근 |
|---|---|---|---|
| 감정 분석 | /sentiment/ | 영어 문장 감정 분석 | 비로그인 가능 |
| 문서 요약 | /summarize/ | 영어 문서 요약 | 로그인 필요 |
| 유해 표현 분석 | /moderate/ | 영어 문장 유해성 분석 | 로그인 필요 |
| 복합 분석 (챌린지) | /combo/ | 요약 → 감정분석 → 유해표현분석 체이닝 리포트 | 로그인 필요 |

## 사용 모델

| 기능 | Model ID | Task | License | 입력 언어 | 출력 |
|---|---|---|---|---|---|
| 감정 분석 | cardiffnlp/twitter-roberta-base-sentiment-latest | text-classification | cc-by-4.0 | 영어 | negative / neutral / positive |
| 문서 요약 | sshleifer/distilbart-cnn-6-6 | summarization | apache-2.0 | 영어 | 요약 텍스트 |
| 유해 표현 분석 | unitary/toxic-bert | text-classification (multi-label) | apache-2.0 | 영어 | toxic / severe_toxic / obscene / threat / insult / identity_hate |

## 실행 방법

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# .env 열어서 DJANGO_SECRET_KEY 값 채우기

python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
```

`http://127.0.0.1:8000/sentiment/` 접속해서 확인.

## 환경변수

`.env` 파일에 아래 값을 넣으면 됩니다. (`.env`는 gitignore 처리되어 있고, `.env.example`만 저장소에 포함되어 있습니다.)

## 구현 내용

- 세 기능 모두 URL/View 분리 (query parameter 방식 아님)
- 모델은 lru_cache로 최초 요청 시 1회만 로드하고 이후 재사용
- 로그인 필요 페이지는 커스텀 데코레이터로 서버단에서 접근 제한. 비로그인 접근 시 로그인 페이지로 리다이렉트되고 로그인 후 원래 페이지로 복귀
- 로그인 사용자의 실행 결과는 InferenceHistory에 저장, 본인 기록만 최근 5개 조회
- 비로그인 상태의 감정 분석 기록은 DB에 저장하지 않고 JS 변수로만 유지 (새로고침 시 초기화)
- CSRF 미들웨어 유지, fetch 요청에 X-CSRFToken 헤더 포함, csrf_exempt 미사용
- 서버단에서 입력값 검증 (빈 값, 공백, 최소/최대 길이, 타입)
- 모델 실행 실패 시 사용자에게는 고정 메시지만 표시, 상세 오류는 서버 로그에만 기록
- 복합 분석은 요약문을 감정분석/유해표현분석 입력으로 사용해 체이닝하고, 재생성 버튼으로 실제 모델을 다시 추론 (do_sample=True)