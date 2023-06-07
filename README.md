# inno2team

## API

#### Room

| 기능                | Method      | URL | request                                                     | response       |
| ------------------- | ----------- | --- | ----------------------------------------------------------- | -------------- |
| 방 전체 리스트 조회 | GET         |     |                                                             | room list data |
| 방 생성             | POST        |     | - room_name<br/>- room_info<br/>- max_people<br/>- location | 200 OK         |
| 방 삭제             | POST/DELETE |     | - room_id<br/>- user_id                                     | 200 OK         |
| 방 정보             | GET         |     | - room_id                                                   | room data      |

#### User

| 기능      | Method      | URL | request | response |
| --------- | ----------- | --- | ------- | -------- |
| 회원가입  | POST        |     |         | 200 OK   |
| 로그인    |             |     |         | 200 OK   |
| 로그아웃  |             |     |         | 200 OK   |
| 방 참여   | POST/update |     | room_id | 200 OK   |
| 방 나가기 | POST/update |     | room_id | 200 OK   |
