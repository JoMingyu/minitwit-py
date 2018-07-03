# minitwit-py
Python + Flask + peewee ORM for SQLite + JWT 조합의 minitwit

## minitwit
### 사용자
username, email, password로 이루어진다.

#### API
- 회원가입
- 로그인
- 로그아웃

### 타임라인
메시지(tweet)는 업로더, timestamp, text로 이루어진다.

#### API
- tweet 업로드
- index : 로그인되어 있으면 해당 사용자의 타임라인, 아니라면 public 타임라인(모든 사용자의 최근 n개 트윗) 정보를 떨궈 주기
- 특정 username의 타임라인

### 팔로우
#### API
- 팔로우
- 언팔로우