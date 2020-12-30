# Project_CashFlow_v3

부동산 개발사업 관련 Project Financing 검토시 사업의 현금흐름을 추정하는 프로그램입니다.

이번에는 분양을 하지 않는 사업의 예시를 가지고 현금흐름을 추정해보고자 합니다.

account 파일 : cashflow 분석을 위한 기본 모듈 포함
Execution_Cashflow 파일 : account 모듈을 이용하여, 부동산개발사업의 현금흐름을 추정함.


## 물류센터 개발 후 통매각 사업에 대한 현금흐름 추정 모델
### 입력데이터
* 개발기간 : 24개월
* 대출만기 : 26개월
* 준공후 가치평가 가정
  * Product A : 상온, 월 임대료 21,000원/평, 면적 8,000평, cap.rate 5.3% 가정
  * Product B : 저온, 월 임대료 50,000원/평, 면적 6,500평, cap.rate 5.8% 가정
  * 준공 후 통매각 가정
* 비용 가정
  * 최초 지급 고정비 : 215억원(토지비 등)
  * 공정률에 따른 비용 : 502억원(공사비 등)
  * 준공시 지급 비용 : 30억원(제세공과금 등)
* 대출 가정
  * 선순위 대출 : 550억원, 4.5% / 1.0%
  * 후순위 대출 : 200억원, 7.0% / 6.0%
  * 주관 fee : 1.5%
  
### 결과물
* acc_oprtg.df : 운영계좌의 현금흐름
* acc_repay.df : 대출금 상환계좌의 현금흐름
* sales.df : 매출 실행 계좌의 현금흐름
* cost.df : 비용 지급 계좌의 현금흐름
* loanA.amt.df : 선순위대출 계좌의 현금흐름
* loanB.amt.df : 후순위대출 계좌의 현금흐름
* loan_fee.df : 금융수수료 계좌 현금흐름
* loanA.IR.df : 선순위대출의 이자지급 계좌 현금흐름
* loanB.IR.df : 후순위대출의 이자지급 계좌 현금흐름
