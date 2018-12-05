# duplication_processing_machine

기업/학교 이름이 중복되었을 경우 찾아서 알맞게 처리하는 프로그램입니다.

# algorithm

기존에 가지고 있는 중복처리된 기업 데이터를 member_count 기준으로 descending order로 정렬한다.

기업 A가 input으로 들어오는 경우/ 두 가지 과정을 거친다.
  1. 동일한 이름이 존재하는 경우
    * 동일한 이름이 존재하는 경우 member_count가 높은 기업으로 merge 시킨다.
    
  2. 유사한 이름이 존재하는 경우
    * 기업 A와 기업 B가 유사한 경우는 기업 A의 이름이 기업 B를 포함하거나, 기업 B의 이름이 기업 A를 포함하는 경우이다. (index 0 부터)
    * "로지텍"은 "제로지텍"에 포함되기는 하지만, index 0 부터 포함되지 않아 제외한다.
    * 유사한 이름이라고 판단되는 경우(user input), member_count가 높은 기업으로 merge 시킨다.
    
  3. 모두 아닌경우
    * 자신의 id를 merge_to value로 갖는 data를 추가한다.


# variables

* company table/LIST classification
* is_user_request (0 : created by 기업생성 , 1 : created by 경력/프로젝트)
* member_count : members signed up company page
* homepage_url : company homepage url
* generated_user : user generated company
* merge_to : company should merge to "id"
COMPANY_TABLE = [ "id", "is_user_request", "member_count", "name_ko", "name_en", "url", "homepage_url", "generated_user", "merge_to"]
COMPANY_LIST = COMPANY data가 Table 형태로 저장된다.

# functions

PREPROCESSING : 기업 이름이 들어왔을 경우/ 불필요한 prefix나 suffix를 제거한다.
  * Delimeter에 저장된 값을 제거.

heapSort : COMPANY_LIST가 member_count 기준으로 descending order가 되게 heapsort 시킨다.

is_same : 새로운 company name Input A가 들어왔을 때 기존에 저장되어 있는 기업 이름과 동일한지 체크하는 function
  * 기업을 string 취급해 두 기업을 character by chacracter로 비교한다.
  * 두 기업이 동일하지만, merge_to value가 다른경우 member_count가 높은 기업으로 merge (connect_company)
  
is_similar : 새로운 company name Input A가 들어왔을 때 기존에 저장되어 있는 기업 이름과 유사한지 체크한다.
  * user input necessary
  * 유사한 경우 member_count가 높은 기업으로 merge_to
  
post_processing : processing 과정이 끝난 후/ 동일한 기업 이름을 가지지만 merge_to value가 다른경우 merge
