import streamlit as st
import random

# 초기 설정
if "results" not in st.session_state:
    st.session_state.results = []
if "ai_profit" not in st.session_state:
    st.session_state.ai_profit = 0
if "user_balance" not in st.session_state:
    st.session_state.user_balance = 1_000_000  # 초기 보유 자금 100만원

# 카드 덱 세팅
deck = [i for i in range(1, 14)] * 4 * 6  # 6덱
random.shuffle(deck)

def draw_card():
    return deck.pop() if deck else None

def baccarat_score(cards):
    return sum(min(c, 10) for c in cards) % 10

def play_round():
    player_cards = [draw_card(), draw_card()]
    banker_cards = [draw_card(), draw_card()]
    
    player_score = baccarat_score(player_cards)
    banker_score = baccarat_score(banker_cards)

    if player_score > banker_score:
        return "Player", player_cards, banker_cards
    elif banker_score > player_score:
        return "Banker", player_cards, banker_cards
    else:
        return "Tie", player_cards, banker_cards

def update_results(winner):
    st.session_state.results.append(winner)

def draw_big_road():
    color_map = {"Player": "blue", "Banker": "red", "Tie": "green"}
    board = []
    col, row = 0, 0
    last = None

    for result in st.session_state.results:
        if result == last:
            row += 1
        else:
            row = 0
            col += 1
        last = result
        board.append((col, row, result))

    for row in range(6):
        row_html = ""
        for col in range(20):
            match = [x for x in board if x[0] == col and x[1] == row]
            if match:
                _, _, result = match[0]
                color = color_map[result]
                row_html += f"<div style='width:20px;height:20px;background:{color};border-radius:50%;display:inline-block;margin:1px'></div>"
            else:
                row_html += "<div style='width:20px;height:20px;background:transparent;display:inline-block;margin:1px'></div>"
        st.markdown(row_html, unsafe_allow_html=True)

# UI
st.title("바카라 시뮬레이터")

st.markdown(f"### 보유 자금: **{st.session_state.user_balance:,}원**")

bet_choice = st.selectbox("당신의 베팅", ["Player", "Banker", "Tie"])
bet_amount = st.number_input("베팅 금액", min_value=1000, step=1000)

if st.button("게임 시작"):
    if st.session_state.user_balance < bet_amount:
        st.warning("잔액이 부족합니다.")
    else:
        winner, player_cards, banker_cards = play_round()
        update_results(winner)

        # 유저 수익 계산
        if bet_choice == winner:
            if winner == "Tie":
                win = bet_amount * 8
            elif winner == "Banker":
                win = bet_amount * 0.95
            else:
                win = bet_amount
            st.session_state.user_balance += win
            user_result = f"베팅 성공! +{win:,.0f}원"
        else:
            st.session_state.user_balance -= bet_amount
            user_result = f"베팅 실패! -{bet_amount:,.0f}원"

        # AI 간단 베팅 (예: 최근 결과에 따라)
        ai_bet = "Banker" if st.session_state.results and st.session_state.results[-1] == "Player" else "Player"
        ai_bet_amount = 1000
        if ai_bet == winner:
            st.session_state.ai_profit += ai_bet_amount * (0.95 if ai_bet == "Banker" else 1)
        else:
            st.session_state.ai_profit -= ai_bet_amount

        # 결과 표시
        st.subheader(f"결과: {winner}")
        st.write(f"플레이어 카드: {player_cards}, 뱅커 카드: {banker_cards}")
        st.success(user_result)
        st.markdown(f"**AI 수익:** {st.session_state.ai_profit:,.0f}원")
        st.markdown(f"**보유 자금:** {st.session_state.user_balance:,.0f}원")

        st.markdown("### 결과판 (빅로드)")
        draw_big_road()
