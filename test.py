import re

# 주어진 문자열
content = """
선택지:
1. 발자국을 따라 도봉산으로 향한다.
2. 추가 무기를 구비하여 도봉산으로 향한다. ('돈' -1)
3. 잠시 휴식하여 체력을 회복한 후 출발한다. ('체력' +1)
"""

# 정규 표현식을 사용하여 선택지를 분리
choices = re.findall(r'\d\.\s([^\d]+)', content)

# 결과를 변수에 할당
first, second, third = choices

# 출력하여 확인
print("first:", first.strip())
print("second:", second.strip())
print("third:", third.strip())