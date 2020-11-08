## MONAWE PRJ 소개 및 선정 이유

- 소개 <br>
  . 국내 문구 Commerce 사이트 [모나미](https://www.monamimall.com/w/main.do) 클론 프로젝트<br>(짧은 기간, 개발에만 집중하기 위해서 디자인/기획 부분만 클론하였습니다.)
- 선정 이유 <br>
  . 문구 Commerce 사이트로 디자인 요소가 적절히 들어가 있으면서 쇼핑몰의 기본기능에 충실하여 선정하게 되었습니다.

### 개발 기간 및 인원
- 개발 기간: 2020/10/19 ~ 2020/10/30 (2주)

- 개발 인원<br>
  . [Fontend](https://github.com/wecode-bootcamp-korea/13-monawe-frontend): 김수연(🦸‍♀️PM), 김한나, 백경민, 이지영 (+ 쩜오론트 민경민님👍) <br>
  . [Backend](https://github.com/wecode-bootcamp-korea/13-monawe-backend): 민경민, 황채영

### 적용 기술
- Frontend: React.js(Class), React-router, React-slick, Sass
- Backend: Django, MySQL, bycrypt, PyJWT, cors-headers
- 공통: git / github, Postman, Trello

### 구현 기능
- 회원가입, 로그인/로그아웃
- 메인페이지(MyCurator, 상품 검색기능, 디자인 요소)
- 리스트페이지 (신상품/가격순 필터기능 및 페이지네이션)
- 상세페이지 (장바구니추가, 찜목록추가, 상품댓글)
- 마이페이지(최근본상품/장바구니/배송지관리)

### 개인별 담당 기능

#### 김수연
1. NavBar MenuTab 및 Transition 구현
2. Login User 정보 활용(localStorage), Navbar User Icon 생성
3. 유저 툴 박스 구현 (최근 본 상품: fetch get 사용)
4. 사이트 검색 기능 구현
5. 메인페이지 모나위 스토리 Slick-slider 구현
6. 마이페이지 구현

#### 김한나
1. 상품리스트페이지 SubNav 기능 구현
2. fetch를 사용하여 Back-End에 호출하하고 응답받은 데이터를 구현함.
3. 상품 filter 기능구현.
4. Pagenation.
5. qurey string과 path로 동적 라우팅 구현.
6. map을 사용해서 jsx 리턴하여 목록 구현.

#### 백경민
1. 회원가입 입력 값 validation check 기능구현
2. 로그인 기능 구현
3. 메인페이지 배너 슬라이드 구현
4. 장바구니 추가/삭제/수량변경 기능구현

#### 이지영

1. 상품 디테일 페이지
2. fetch (GET, POST)를 사용하여 백엔드와 통신 
3. 댓글 기능 구현 (map을 사용하여 jsx return)
4. query string 사용하여, 상품리스트에서 상세 페이지로 이동 
5. 메인페이지의 추천 상품 component 제작 (hover를 이용한 transition 기능 구현)

#### 민경민
1. 회원가입 / 로그인 엔드포인트 작성
1. JWT 발행, 데코레이터로 검증
1. 주소지 CRUD 엔드포인트 작성
1. 주소지 CRUD React component 작성
1. 상품 리스팅 / 검색 / 필터링 / 페이지네이션
1. 상품 상세 정보 엔드포인트 작성

#### 황채영
1. 장바구니 CRUD 엔드포인트 작성
1. 최근 본 상품 CRUD 엔드포인트 작성
1. 찜리스트 CRUD 엔드포인트 작성

### PRJ 후기
- 김수연: [1차 프로젝트 후기](https://velog.io/@link717/WeCode-1%EC%B0%A8-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%9B%84%EA%B8%B0)
- 김한나: [1차 프로젝트 후기](https://velog.io/@nana_kim/1차-프로젝트-후기-Moname)
- 백경민: 
- 이지영:
- 민경민: [1차 프로젝트 후기](https://velog.io/@mgm-dev/%ED%9B%84%EA%B8%B0-wecode-1%EC%B0%A8-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%9B%84%EA%B8%B0)
- 황채영: [1차 프로젝트 후기](https://velog.io/@hwangninaa/monawe-1%EC%B0%A8-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EB%A6%AC%EB%B7%B0)

### 주의사항
- commit 작업 시, branch 확인!

### Team Rules✨
- `어?` 하지말기
- 최종발표 날 모나미룩 입고오기!
- PM님을 마음 속에 품고살기

## Reference
- 이 프로젝트는 [모나미](https://www.monamimall.com/w/main.do) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
