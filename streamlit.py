import streamlit as st
import streamlit.components.v1 as components
import time
import random
import uuid
from celery.result import AsyncResult
# from tasks import celery_app, answer_with_file_task, call_agent
from streamlit_autorefresh import st_autorefresh
import json, base64
aws_token='3HMLKQG7BV17VOIENY'
### user authentic ###
user_id = st.query_params.to_dict().get("user_id", "none")
depart_info = st.query_params.to_dict().get("depart_info", "none")

st.set_page_config(page_title="AI 검색 시스템", page_icon="🧊",layout="wide")

# 세션 상태 초기화
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = [{"role": "assistant", "content": "무엇을 검색해 드릴까요?"}]
    
if "use_external_docs" not in st.session_state:
    st.session_state.use_external_docs = False
    # st.session_state.use_cont_msg = False
if "example_questions" not in st.session_state:
    st.session_state.example_questions = [
        "어제 롯데 경기 결과 알려줘.",
        "23년 LG에서 10홈런 이상친 선수",
        "24년 한화 이글스 최종 순위 알려줘.",
        "22년 SK 와이번스 투수중 ERA 3점 이하인 선수",
        "21년 두산 베어스에서 20도루 이상한 선수 알려줘.",
        "작년 기아 타이거즈에서 20-20 클럽 달성한 선수",
        "23년 NC 다이노스에서 3할3푼 이상 달성한 선수",
        "24년 삼성 라이온즈에서 가장 많은 삼진을 잡은 선수",
        "25년 KT 안현민 선수 타율 알려줘.",
        "24년 KT 고영표 선수 ERA 알려줘.",
        # "두산 이승엽 감독 눈물 사건에 대해서 알려줘.",
        "23년 KT 엄상백 선수 삼진 개수 알려줘."
    ]
if "random_questions" not in st.session_state:
    st.session_state.random_questions = random.sample(st.session_state.example_questions, 9)

# 메시지 추가 함수
def add_message(role, content):
    chat_id = st.session_state.current_chat
    st.session_state.chats[chat_id].append({"role": role, "content": content})

# 채팅 전환 함수
def switch_chat(chat_id):
    st.session_state.current_chat = chat_id
    st.rerun()
    
# figure 추가 함수
def add_fig(role, content, dir_):
    chat_id = st.session_state.current_chat
    st.session_state.chats[chat_id].append({"role":role, "content": content, "figure": dir_})

# 🌍 웹 검색 포함 여부 설정
with st.sidebar:
    st.markdown(f"**이름 : {user_id}**")
    st.markdown(f"**소속 : {depart_info}**")
    st.divider()
    
    for chat_id in st.session_state.chats:
        if len(st.session_state.chats[chat_id]) > 1:
            if st.sidebar.button(f"""{st.session_state.chats[chat_id][1]['content']}""", key=chat_id):
                switch_chat(chat_id)
                
    if st.sidebar.button("📝 New Chat"):
        new_chat_id = str(uuid.uuid4())
        st.session_state.chats[new_chat_id] = [{"role": "assistant", "content": "무엇을 검색해 드릴까요?"}]
        switch_chat(new_chat_id)
        
    st.divider()
    st.markdown("")
    st.markdown('<p style="font-size: 15px; font-weight: bold;line-height: 1.2;">※ 기능 구현</p>', unsafe_allow_html=True)
    st.markdown("")
    
    st.markdown('<p style="font-size: 13px; font-weight: bold;line-height: 1.2;">◈ 대화 맥락을 고려하여 답변.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 12px; font-weight: bold;line-height: 1.2;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 좀 더 자세히 알려줘.</p>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 13px; font-weight: bold;line-height: 1.2;">◈ 파이썬 코드 작성 및 실행.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 12px; font-weight: bold;line-height: 1.2;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 1부터 500까지 소수만 출력해줘.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 12px; font-weight: bold;line-height: 1.2;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 머신러닝 모델 기본 코드 작성해줘.</p>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 13px; font-weight: bold;line-height: 1.2;">◈ 데이터 수집 및 그래프 시각화.</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 12px; font-weight: bold;line-height: 1.2;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ 전기차 Market 21년부터 30년 까지의 CAGR 그래프 그려줘.</p>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 13px; font-weight: bold;line-height: 1.2;">◈ 파일 요약 or 유사 사례 추천 가능.</p>', unsafe_allow_html=True)
    
    


st.title("💬 KBO stats AI 검색 시스템 구현")
st.caption("🚀 **하강우**")
components.html(
    """
    <style>
    .blink {
      animation: blinker 5s linear infinite;
    }

    @keyframes blinker {
      50% {
        opacity: 0;
      }
    }
    </style>
    <p class="blink" style="color: blue; font-weight: bold; font-size: smaller;">
    본 시스템은 KBO 선수 기록 AI 검색 시스템 입니다. 자유롭게 자연어로 검색해 주세요.
    </p>
    """,
    height=50, # 필요에 따라 높이 조정
    scrolling=False, # 스크롤바 제거 (내용이 한 줄로 표시될 경우)
)

def send_question_to_queue(question):
    add_message("user",f"{question}")
    try:
        response = requests.get(FASTAPI_URL, json={"question": question+"sql table은 batter야 그리고 쿼리를 마크다운 없이 출력해주세요."})
        response.raise_for_status()  # 200 OK 아니면 예외 발생

        result = response.json().get("result", "No result found.")
        add_message("assistant", result)

    except Exception as e:
        error_msg = f"❗ FastAPI 서버 오류: {str(e)}"
        add_message("assistant", error_msg)
    
# file upload와 함께 질문을 큐에 전송하는 함수
def send_question_with_file_to_queue(question, file):

    add_message("User", question)
    
    # task = answer_with_file_task.apply_async(args=[st.session_state.chats[st.session_state.current_chat], question, file])
    st.toast(f"📑 AI 기반 답변을 생성 중입니다. Task ID: {task.id}")
    st.session_state["task_id"] = task.id
    st.session_state["loading"] = True
    st.rerun()


st.subheader("💡 Example Questions")
for i in range(3):
    cols = st.columns(3)  # 가로로 3개 열 만들기
    for idx, col in enumerate(cols):
        question = st.session_state.random_questions[i*3 + idx]
        if col.button(question, use_container_width=True):  # key를 다르게 해야 함
            send_question_to_queue(question)
        
# 사용자 입력 처리
if user_input := st.chat_input(accept_file=True):
    if user_input.files:
        byte_file = user_input.files[0].read()
        send_question_with_file_to_queue(user_input.text, byte_file)
    send_question_to_queue(user_input.text)

# 채팅 메시지 출력
# st.subheader("Conversation")
st.divider()
for msg in st.session_state.chats[st.session_state.current_chat]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"], unsafe_allow_html=True)
        
        if msg.get("figure"):
            st.image(msg["figure"])
