# 🪶 Nosce-Codicem: 네 코드를 알라
*A CLI-based visualization tool for understanding your Python logic.*

---
### 🧩 Project Overview
알고리즘 문제를 풀다보면 반복문이나 재귀문 내부에서 변수나 리스트의 값 변화를 직접 추적하고 싶을 때가 많습니다.  
그럴 때마다 테스트 코드를 작성하고, 지저분한 출력을 통해 오류를 찾는 과정이 번거롭다고 느꼈습니다.  

이에 착안하여,
1) **코드 한 줄만 실행해도 변수의 변화를 자동으로 추적**하고 
2) **별도의 창을 통해 이해하기 쉽게 출력**해주는  

툴을 만들어보자는 취지에서 해당 프로젝트를 기획했습니다.  

Nosce-Codicem 툴은 (개인적으로 오류를 확인하기 어려운) **반복문과 재귀문**에서 **변수와 리스트**의 상태를 추적하고,  
별도의 CLI 창을 통해 알고리즘 진행 단계에 따라 추적한 값을 출력합니다.

---
### 🚀 Project Goal

- **CLI 기반의 알고리즘 학습 보조 도구**를 개발하여,  
  학습자가 자신의 코드 흐름과 변수 변화를 직관적으로 이해할 수 있도록 돕습니다.  
- 최종적으로 **PyPI에 배포 가능한 오픈소스 파이썬 라이브러리**로 완성하는 것을 목표로 합니다.

---
### ✨ 주요 기능  

- sys.settrace 기반 변수와 이벤트 추적
- Table을 통한 Loop문 시각화
    - 다수의 변수와 리스트들도 table로 표현 가능
- 재귀호출 tree와 timeline을 통한 Recursive문 시각화
    - 함수 호출 시 tree와 timeline 동시 출력
- Rich 기반 CLI 출력


---
### ⚙️ 프로젝트 구조
```
NOSCE-CODICEM/
├─ src/
│  └─ nosce_codicem/
│     ├─ api/           # 사용자 API 구성
│     ├─ core/          # sys.settrace 컨트롤러, 이벤트 디스패처, 전체 실행 흐름 관리 로직
│     ├─ handlers/      # 이벤트를 해석하고, 전달하는 객체 정의
│     ├─ observers/     # 변수와 리스트를 관찰하고 기록하는 객체 정의
│     ├─ output/        # 이벤트 구조화, CLI 시각화
│     └─ __init__.py    # 패키지 초기화
│
├─ tests/               # 테스트 코드 모음
├─ LICENSE              # MIT 라이선스
└─ README.md
```

---
### 🧐 How to Use

1) `pip install nosce-codicem`으로 패키지를 설치합니다.

2) `from nosce_codicem import trace` 형태로 trace 빌더를 불러옵니다.

3) 반복문 안의 변수를 추적하려면 `trace.variable(...).loop(start, end)`를 사용합니다.  
   - `variable()`에는 추적할 변수명을 문자열로 입력합니다.  
     여러 변수를 추적하고 싶다면 쉼표로 구분해 나열할 수 있습니다.  
   - `loop(start, end)`에는 반복문의 **시작 라인 번호와 종료 라인 번호**를 입력합니다.

4) 반복문 안의 리스트를 추적하려면 `trace.list(...).loop(start, end)`를 사용합니다.  
   - `list()`에는 추적할 리스트명을 문자열로 입력합니다.  
     여러 리스트를 추적할 경우 역시 쉼표로 구분해 나열합니다.

5) 재귀문 안의 변수를 추적하려면 `trace.variable(...).recursion(func_name)`을 사용합니다.  
   - `variable()`의 사용 방식은 반복문과 동일합니다.  
   - `recursion(func_name)`에는 추적하고자 하는 재귀 함수명을 문자열로 입력합니다.

6) 재귀문 안의 리스트를 추적하려면 `trace.list(...).recursion(func_name)`을 사용합니다.  
   - 리스트 사용 방식 역시 반복문의 경우와 동일합니다.


**⚠️주의사항⚠️**  
trace는 반드시 **관찰하고자 하는 코드가 실행되기 전에** 호출해야 정상적으로 동작합니다.  
Python의 `sys.settrace`는 main 스크립트와 동일한 타이밍에서 트리거되기 때문에,  
trace가 실제로 감시할 수 있는 것은 **호출 시점 이후에 새로 실행되는 함수와 그 내부의 흐름뿐**입니다.  
따라서 이미 실행이 시작된 전역 코드나, 함수 호출이 끝난 뒤에 trace를 선언하면 어떤 이벤트도 포착할 수 없습니다.  
이러한 이유로, 관찰 대상 로직은 반드시 **함수 형태로 선언**하고,  
그 함수를 호출하기 전에 trace를 활성화하는 해야만 합니다.

---
### 🧑‍🏫 사용 예시

✔ 루프 + 변수 예시
```
from nosce_codicem import trace

def count_up():
    total = 0
    for i in range(5):    # line number : 8
        total += i        # line number : 9

trace.variable("i", "total").loop(5, 6)
count_up()
```
![preview](https://private-user-images.githubusercontent.com/104406039/517006452-e0771732-2d45-4633-8915-a9bad76c0749.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjM2NjMxODYsIm5iZiI6MTc2MzY2Mjg4NiwicGF0aCI6Ii8xMDQ0MDYwMzkvNTE3MDA2NDUyLWUwNzcxNzMyLTJkNDUtNDYzMy04OTE1LWE5YmFkNzZjMDc0OS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMTIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTEyMFQxODIxMjZaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0wMTViZDE1MmY2Yjg3ODY0ZGI3NzNlYzcwYzJlMzlhNWM4NjRjZjZjYTQ4MGRmYzA4NmQ4NTEwNzRmYTM0MTgyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.BLVCa1_o8srS60e3TDWmuwLzMgx4tfdvwvns7Q_Jy8Q)  

(중간 출력 생략)  

![preview](https://private-user-images.githubusercontent.com/104406039/517006453-17f69224-5dd5-4028-9c6c-23c2ef8a701e.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjM2NjMxODYsIm5iZiI6MTc2MzY2Mjg4NiwicGF0aCI6Ii8xMDQ0MDYwMzkvNTE3MDA2NDUzLTE3ZjY5MjI0LTVkZDUtNDAyOC05YzZjLTIzYzJlZjhhNzAxZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMTIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTEyMFQxODIxMjZaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05ZGZkZjZhMzI1NjU2Mzk4OWU4NTJlODE1ZDE3ZWU4ZTgwYjQ1NjhjOGY2MTQ5MWE5ZWM5MzhkZDRkYWQ5ZjZmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.uqYiDH7WjG0bHVan9WLuBfNHJx0CGlPoEhvLgrft10o)  
  
✔ 루프 + 리스트 예시  
```
from nosce_codicem import trace

def test_list_loop():
    arr = [1, 2, 3, 4, 5]
    i = 0
    while i < len(arr):        # line number : 6
        arr[i] = arr[i] * 2
        i += 1                 # line number : 8

trace.list("arr").loop(6, 8)
test_list_loop()
```
![preview](https://private-user-images.githubusercontent.com/104406039/517006459-7d54ba5a-fb8e-42fb-902b-5d660965df49.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjM2NjI5MjcsIm5iZiI6MTc2MzY2MjYyNywicGF0aCI6Ii8xMDQ0MDYwMzkvNTE3MDA2NDU5LTdkNTRiYTVhLWZiOGUtNDJmYi05MDJiLTVkNjYwOTY1ZGY0OS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMTIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTEyMFQxODE3MDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT01YzU5N2EwZDI2YWNhY2E0ZjBiODRmNThlNDI2MDYwNjgxYjc5NTlmMzNjNzk4ZDZiZjRiYzY2MWQzNDkwZTk5JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.nLwBIJvwl_0GMN2uXqGjGb_CwdwlZeQjTni9M_qI0DY)  

(중간 출력 생략)  

![preview](https://private-user-images.githubusercontent.com/104406039/517006454-36db55c9-7867-4b36-b550-e90a0b67ea2e.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjM2NjI5MjcsIm5iZiI6MTc2MzY2MjYyNywicGF0aCI6Ii8xMDQ0MDYwMzkvNTE3MDA2NDU0LTM2ZGI1NWM5LTc4NjctNGIzNi1iNTUwLWU5MGEwYjY3ZWEyZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMTIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTEyMFQxODE3MDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05ZDEzZTlmMzE0NTE2YzllYjgyOTE4MGU3NGI4ZTRiNjhiZDY3N2Y5MTdiYmI2Y2E4OWYxMTVjYzA3NzRhNmMyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.lx9-5yuqkTPD847haQdWeElg51rRPCcskXe4J8nfWvM)  

✔ 재귀 + 변수 예시
```
from nosce_codicem import trace

def fib(n):
    if n <= 1:
        return n
    
    a = fib(n - 1)   # 변수 a 추적
    b = fib(n - 2)   # 변수 b 추적
    result = a + b   # result도 추적
    return result

trace.variable("n", "a", "b", "result").recursion("fib")
fib(5)
```
![preview](https://private-user-images.githubusercontent.com/104406039/517006456-84ce0d87-8e68-43db-b246-f18904a7a721.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjM2NjI5MjcsIm5iZiI6MTc2MzY2MjYyNywicGF0aCI6Ii8xMDQ0MDYwMzkvNTE3MDA2NDU2LTg0Y2UwZDg3LThlNjgtNDNkYi1iMjQ2LWYxODkwNGE3YTcyMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMTIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTEyMFQxODE3MDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03YzZiNTRhMGU0YjgzN2NiNzgyYWY1MmI5YWUxNzczMzMzNjhmYjg3ZDlkMjc5ODkxNmRiMDE4ZTI0MDdkMjhjJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.Jf2jPKPlhYU_SX6Lhmzf_l7gEEILW5eiAtQUDlP50cs)  
(나머지 트리 생략)  

![preview](https://private-user-images.githubusercontent.com/104406039/517006455-7efcb875-9227-4bfc-984c-d57c42bccf6b.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjM2NjI5MjcsIm5iZiI6MTc2MzY2MjYyNywicGF0aCI6Ii8xMDQ0MDYwMzkvNTE3MDA2NDU1LTdlZmNiODc1LTkyMjctNGJmYy05ODRjLWQ1N2M0MmJjY2Y2Yi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMTIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTEyMFQxODE3MDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mN2I0MmIwODQ4YTA5MDY0NjMzZjhmMGM4NmZkZDE1OGRkNzJiNDU0MTg3NGRmY2NmMDhkNjE2YjA1YWRlM2VkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.iwbENb-ag-gs20qt0Cr_KNWIx3U0UNLGXMKTsWC9_kY)  
(나머지 타임라인 생략)  

✔ 재귀 + 리스트 예시
```
from nosce_codicem import trace

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

trace.list("arr").recursion("merge_sort")
arr = [7, 5, 2, 4, 1, 3, 6]
merge_sort(arr)
```  
![preview](https://private-user-images.githubusercontent.com/104406039/517006457-5d7a0350-0614-452b-9958-1cad8edc5cd9.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjM2NjI5MjcsIm5iZiI6MTc2MzY2MjYyNywicGF0aCI6Ii8xMDQ0MDYwMzkvNTE3MDA2NDU3LTVkN2EwMzUwLTA2MTQtNDUyYi05OTU4LTFjYWQ4ZWRjNWNkOS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMTIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTEyMFQxODE3MDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hOGI1OTY3NzExNDMyY2RlZGJhMTg5ZGFlZjUzY2Q1MjczMmUwODVhNjg1ODQ5NTA4ZjExNzM0NjIzM2EyYTUxJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.YYyeA13dkckWiaUPMa9qRn30uho6_fJGDojBwKOua1w)  
(나머지 트리 생략)  

![preview](https://private-user-images.githubusercontent.com/104406039/517006458-eaadd345-27af-4434-ae83-d78a2a79db9c.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjM2NjI5MjcsIm5iZiI6MTc2MzY2MjYyNywicGF0aCI6Ii8xMDQ0MDYwMzkvNTE3MDA2NDU4LWVhYWRkMzQ1LTI3YWYtNDQzNC1hZTgzLWQ3OGEyYTc5ZGI5Yy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMTIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTEyMFQxODE3MDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0xZDA4NzdjZGJmZWIyYTlmYTcwMWI5ZTY3ZTkwYWIxYWExNGFmMmExNjk2ZmMyY2Y2NGUzYmQxZjVjZDM2NjI0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.XtJ7HDD6ZhiRGV9AzoOO6EEtgSDxp-8eqM3Ac1r76So)  
(나머지 타임라인 생략)

---
### 🚧 Limitations
- "CLI 창을 통한 시각화"라는 주제의 한계에 의해  
추적하는 변수의 양이 너무 많거나, 리스트의 길이가 길거나, 재귀의 깊이가 너무 깊으면  
시인성이 보장되지 않습니다.

- 해당 프로젝트의 리스트 추적에는 안정적인 로직을 위해 deepcopy가 사용되어  
길고 복잡한 작업 시 프로그램의 성능을 급격히 떨어뜨릴 수 있습니다.  
간단한 알고리즘 풀이에만 적합합니다.


---
### 🛠️ 설치 환경

- **Python 3.9 ~ 3.13**
  - Windows Store Python은 `sys.settrace` 동작 방식 문제로 인해 정상적으로 작동하지 않을 수 있습니다.

- Windows/Mac/Linux 지원
  - 핵심 로직은 Windows 외의 OS에서도 작동할 수 있도록 구현했지만,  
  Windows 외의 환경에서 테스트를 해보지 못했기에 타 OS에서의 동작을 장담하지 못합니다.

- Rich 13.0 이상 권장
  - CLI 시각화는 파이썬의 외부 라이브러리 Rich를 기반으로 하며, 13.0 이상 버전을 권장합니다.  

---
### ⚖️ License
이 프로젝트는 **MIT License** 하에 배포됩니다.  
사용자는 라이선스 조건 내에서 자유롭게 소스코드를 수정·재배포할 수 있습니다.

보다 자세한 내용은 저장소의 `LICENSE` 파일을 참고하십시오.

---
### 🔎 Open Source & Reference

- **Rich (MIT License)** 
  - 파이썬의 외부 라이브러리
  - CLI 출력 스타일링 및 테이블·트리 렌더링에 사용  


- **Python Standard Library (PSF License)**  
  - `sys.settrace` : 실행 흐름 추적  
  - `subprocess` : viewer 독립 콘솔 실행  
