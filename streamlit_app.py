# import streamlit as st
# import openai

# user_api_key = st.text_input("키를 입력해주세요.")

# if user_api_key:

#     from openai import OpenAI

#     client = OpenAI(api_key = user_api_key)
#     prompt = st.text_input("프롬프트를 입력해주세요.")

#     completion = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     st.markdown("### 💡 GPT의 답변:")
#     st.write(completion.choices[0].message.content)

# st.title("소개")
# st.info(
#     "안녕하세요! 반갑습니다. 저는 입니다"
# )
# # 페이지 구조용 제목 출력
# st.header("문제")
# gender = st.radio("선준이가 좋아하는 사람을 선택하세요", ["남성", "여성", "유진"])
# if gender == "남성" :
#     st.success("✅ 정답!")
#     st.image("https://media3.giphy.com/media/CGXnGb7zpsvXD2uwvd/giphy.webp?cid=82a1493bf0i2w35giy8e9zadzndezaaal5pujrsii0terkfl&ep=v1_gifs_trending&rid=giphy.webp&ct=g", caption="예시 이미지")
# elif gender == "여성" :
#     st.error("❌삐빅")
# else :
#     st.success("✅ 정답!")
#     st.image("https://media0.giphy.com/media/wqb5K5564JSlW/giphy.webp?cid=82a1493b9mjypfzmo15yft87rk9q052fc66kisofvhukxxox&ep=v1_gifs_trending&rid=giphy.webp&ct=g", caption="예시 이미지")
    


# # st.sidebar: 사이드바 영역에 콘텐츠를 배치합니다
# st.sidebar.title("📌 사이드바 메뉴")
# option = st.sidebar.selectbox("옵션을 선택하세요", ["성유진", "박선준", "꺼임"])
# st.write("선택한 옵션:", option)
# with st.expander("ℹ️ 박선준에 대해서"):
#     st.write("최대업적 : 여자친구 사귐!")
#     st.write("마플시너지로 친구와 손절하기")
import streamlit as st
import openai

# 🎯 앱 제목 및 간단 소개
st.title("🧠 선준이")
st.caption("선준이이와 대화하고, 선준이 퀴즈도 즐겨보세요!")

# 🔄 탭 구분
tab1, tab2, tab3 = st.tabs(["💬 선준이와 대화하기", "🎯 선준이 퀴즈", "ℹ️ 앱 정보"])

# ──────────────────────────────
# 💬 GPT 탭
with tab1:
    st.header("선준이와 대화하기")
    user_api_key = st.secrets["openai"]["api_key"]

    if user_api_key:
        from openai import OpenAI
        client = OpenAI(api_key=user_api_key)

        prompt = st.text_input("✍️ 나 박선준인데 다 물어봐라:")

        if prompt:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            st.markdown("### 💡 박선준:")
            st.success(completion.choices[0].message.content)

# ──────────────────────────────
# 🎯 퀴즈 탭
with tab2:
    st.header("🎲 선준이 퀴즈 타임")
    gender = st.radio("Q. 선준이가 좋아하는 사람을 선택하세요:", ["남성", "여성", "유진"])

    if gender == "남성":
        st.success("✅ 정답!")
        st.image(
            "https://media3.giphy.com/media/CGXnGb7zpsvXD2uwvd/giphy.webp?cid=82a1493bf0i2w35giy8e9zadzndezaaal5pujrsii0terkfl&ep=v1_gifs_trending&rid=giphy.webp&ct=g",
            caption="🎉 정답을 맞췄어요!"
        )
    elif gender == "여성":
        st.error("❌ 삐빅! 다시 생각해보세요.")
    else:
        st.success("✅ 정답!")
        st.image(
            "https://media0.giphy.com/media/wqb5K5564JSlW/giphy.webp?cid=82a1493b9mjypfzmo15yft87rk9q052fc66kisofvhukxxox&ep=v1_gifs_trending&rid=giphy.webp&ct=g",
            caption="🎉 유진을 선택했군요!"
        )

# ──────────────────────────────
# ℹ️ 앱 정보 탭
with tab3:
    st.header("📌 앱 정보 및 사이드 메뉴")
    option = st.selectbox("👤 옵션을 선택하세요:", ["성유진", "박선준", "꺼임"])
    st.write("🧾 선택한 옵션:", option)

    with st.expander("ℹ️ 박선준에 대해서"):
        st.markdown("""
        - 🏆 **최대 업적**: 여자친구 사귐!  
        - 💔 **마플 시너지**: 친구와 손절하기...
        """)

