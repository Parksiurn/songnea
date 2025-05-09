import streamlit as st

st.title("소개")
st.info(
    "안녕하세요! 반갑습니다. 저는 입니다"
)
# 페이지 구조용 제목 출력
st.title("성")
st.header("유")
st.subheader("진")
# st.sidebar: 사이드바 영역에 콘텐츠를 배치합니다
st.sidebar.title("📌 사이드바 메뉴")
option = st.sidebar.selectbox("옵션을 선택하세요", ["성유진", "박선준", "꺼임"])
st.write("선택한 옵션:", option)