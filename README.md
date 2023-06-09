# 동북권 ICT 부트캠프 이노베이션 캠프 2조 미니 프로젝트 SA


### 1. 프로젝트명 : 모여보드자

#### 1.1 프로젝트 소개 : 보드게임을 같이 할 사람을 매칭해주는 웹사이트 제작

#### 1.2 팀원

  [김광일](https://github.com/kki4504)

  [김승수](https://github.com/kss123456789)

  [박진웅](https://github.com/hamonia777)

  [최도영](https://github.com/mabyoungg)

#### 1.3 Thumbnail
![244397107-c4da4184-dce2-47db-80d7-aa4678c6b101](https://github.com/inno2team/inno2team/assets/131260371/a0bd98c9-b43f-4664-a657-3d3bb0f4d59d)

![모여보드자](https://github.com/inno2team/inno2team/assets/131260371/c97388b2-45a4-49b6-a78d-76ece27f8e94)

---
### 2. 와이어 프레임
![Section 1](https://github.com/inno2team/inno2team/assets/131260371/9a2a4cd2-7c20-43fa-ac3f-770ec53235fc)

![Section 2](https://github.com/inno2team/inno2team/assets/131260371/ae1fe1e7-b9f8-4296-82c1-7a34ffade41d)

![Section 3](https://github.com/inno2team/inno2team/assets/131260371/22a27e20-71a2-4bc2-80c0-4b118e987d45)

![Section 4](https://github.com/inno2team/inno2team/assets/131260371/b64d9641-ea30-4649-94c1-5dc6bc1fec03)

---
### 3. API

#### Room

| 기능                | Method      | URL                | request                                                                                                    | response       |
| ------------------- | ----------- | ----------------- | ----------------------------------------------------------------------------------------------------------  | -------------- |
| 방 전체 리스트 조회 | GET          |/room/list           |                                                                                                           | room list data |
| 방 생성             | POST        |/create_room         | - room_name<br/>- room_info<br/>- max_people<br/>- location <br/> - prt <br/> - user_id <br/> - prt_users | 200 OK    |
| 방 삭제             | POST        |/delete              | - room_id<br/>- user_id                                                                             | 200 OK     |
| 방 인원 추가        | UPDATE       |/room/join           | room_id                                                                                               | 200 OK   |
| 방 정보             | GET         |/board/get/{room_id} |                                                                                                     | room data      |

#### User

| 기능      | Method      | URL | request                                                            | response |
| --------- | ----------- | --- | ----------------------------------------------------------------- | -------- |
| 회원가입  | POST        |/regist | - user_id <br/>- password<br/> - nickname<br/> - phone      | 200 OK   |
| 로그인    | POST         |/login | - user_id<br/> - password                                   | 200 OK   |
| 아이디 검증| POST        |/validate | - user_id                                               | 200 OK   |
| 유저 정보 조회| GET      |/user/get/{user_id} |                                              | user id data |


#### Comment

| 기능      | Method      | URL                     | request                                                        | response |
| --------- | ----------- | ---------------------- | -------------------------------------------------------------- | -------- |
| 댓글 조회 | GET           |/comment/get/{room_id} |                                                                |  comment list data  |
| 댓글 저장 | POST          |/comment/save/{room_id} | - user_id <br/> - comment <br/> - roomd_id <br/> - nickname   | 200 OK   |
| 댓글 삭제  | POST          |/comment/delete       | - _id                                                          | 200 OK   |
