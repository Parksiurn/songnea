import streamlit as st

st.title("소개")
st.info(
    "안녕하세요! 반갑습니다. 저는 입니다"
)
# 페이지 구조용 제목 출력
st.header("문제")
gender = st.radio("선준이가 좋아하는 사람을 선택하세요", ["남성", "여성", "유진"])
if gender == "남성" :
    st.success("✅ 정답!")
    st.image("https://media3.giphy.com/media/CGXnGb7zpsvXD2uwvd/giphy.webp?cid=82a1493bf0i2w35giy8e9zadzndezaaal5pujrsii0terkfl&ep=v1_gifs_trending&rid=giphy.webp&ct=g", caption="예시 이미지")
elif gender == "여성" :
    st.error("❌삐빅")
else :
    st.success("✅ 정답!")
    st.image("https://media0.giphy.com/media/wqb5K5564JSlW/giphy.webp?cid=82a1493b9mjypfzmo15yft87rk9q052fc66kisofvhukxxox&ep=v1_gifs_trending&rid=giphy.webp&ct=g", caption="예시 이미지")
    


# st.sidebar: 사이드바 영역에 콘텐츠를 배치합니다
st.sidebar.title("📌 사이드바 메뉴")
option = st.sidebar.selectbox("옵션을 선택하세요", ["성유진", "박선준", "꺼임"])
st.write("선택한 옵션:", option)
with st.expander("ℹ️ 박선준에 대해서"):
    st.write("최대업적 : 여자친구 사귐!")
