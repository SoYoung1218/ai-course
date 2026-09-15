import ollama, time

t = time.time()
n = 0
for chunk in ollama.chat(model="qwen3:8b", think=False, stream=True,
                         messages=[{"role": "user", "content": "봄에 대한 짧은 시를 4줄로 써줘."}],
                         options={"temperature": 0}):
    print(chunk.message.content, end="", flush=True)
    n += 1
print(f"\n{n} 조각, {time.time() - t:.1f}초")


# import ollama, time

# t = time.time()
# n = 0
# # q = "2019년 서울대 김민준 교수가 발표한 논문 '양자 어텐션 네트워크'의 핵심 내용을 3문장으로 설명해줘"
# q = "파이썬 표준 라이브러리 함수 listx.flatten_deep()의 사용법"
# # s = ollama.chat(model="qwen3:8b", think=False, messages=[{"role": "user", "content": "봄에 대한 짧은 시를 4줄로 써줘."}], options={"temperature": 1})
# for chunk in ollama.chat(model="qwen3:8b", think=False, stream=True, messages=[{"role": "user", "content": q}], options={"temperature": 1}):
#     print(chunk.message.content, end="", flush=True)
#     n += 1
# # print(f"{s.message.content}")
# print(f"\n{n} 조각, {time.time() - t:.1f}초")