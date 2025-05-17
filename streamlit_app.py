import streamlit as st
import random
import pandas as pd
from collections import deque

# 카드 덱 초기화 (8덱 기준)
def init_deck(num_decks=8):
    deck = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4 * num_decks
    random.shuffle(deck)
    return deque(deck)

# 카드 점수 계산
def card_value(card):
    if card in ['10', 'J', 'Q', 'K']:
        return 0
    elif card == 'A':
        return 1
    else:
        return int(card)

# 두 장 합산 후 일의 자리만 남기기
def hand_total(cards):
    return sum(card_value(c) for c in cards) % 10

# 카드 뽑기
def draw(deck):
    return deck.popleft()

# 게임 한 라운드 시뮬레이션
def simulate_round(deck):
    if len(deck) < 6:
        return None  # 카드 부족 시 종료

    player = [draw(deck), draw(deck)]
    banker = [draw(deck), draw(deck)]

    pt = hand_total(player)
    bt = hand_total(banker)

    player_third = None
    banker_third = None

    # Player 규칙
    if pt <= 5:
        player_third = draw(deck)
        player.append(player_third)

    # Banker 규칙 (간략화, 정확한 룰 필요시 확장 가능)
    bt = hand_total(banker)
    if pt >= 0 and pt <= 7:
        if bt <= 2:
            banker_third = draw(deck)
            banker.append(banker_third)

    final_pt = hand_total(player)
    final_bt = hand_total(banker)

    winner = 'Tie' if final_pt == final_bt else 'Player' if final_pt > final_bt else 'Banker'

    return {
        'player': player,
        'banker': banker,
        'winner': winner,
        'player_total': final_pt,
        'banker_total': final_bt,
        'pair_player': player[0] == player[1],
        'pair_banker': banker[0] == banker[1]
    }

# 초기 자본 설정
USER_INITIAL = 2_000_000
AI_INITIAL = 2_000_000
NUM_AI = 500

st.title("바카라 시뮬레이터")

if 'deck' not in st.session_state:
    st.session_state.deck = init_deck()
    st.session_state.user_money = USER_INITIAL
    st.session_state.ai_money = [AI_INITIAL] * NUM_AI
    st.session_state.logs = []

# 사용자 베팅 입력
st.subheader("당신의 베팅")
bet_target = st.radio("베팅 대상", ['Player', 'Banker', 'Tie', 'Player Pair', 'Banker Pair'])
bet_amount = st.number_input("베팅 금액", 10000, st.session_state.user_money, step=10000)

# 게임 진행
if st.button("게임 시작"):
    result = simulate_round(st.session_state.deck)
    if result is None:
        st.warning("카드가 부족해 게임 종료됩니다. 다시 시작해주세요.")
    else:
        payout = 0
        # 사용자 수익 처리
        if bet_target == result['winner']:
            if bet_target == 'Tie':
                payout = bet_amount * 8
            else:
                payout = bet_amount * (0.95 if bet_target == 'Banker' else 1)
        elif bet_target == 'Player Pair' and result['pair_player']:
            payout = bet_amount * 11
        elif bet_target == 'Banker Pair' and result['pair_banker']:
            payout = bet_amount * 11
        else:
            payout = -bet_amount

        st.session_state.user_money += payout

        # AI 베팅 및 수익 처리
        for i in range(NUM_AI):
            ai_bet = random.choice(['Player']*4 + ['Banker']*4 + ['Tie'] + ['Player Pair', 'Banker Pair'])  # Pair 몰림 방지
            ai_amount = 10_000
            ai_gain = 0
            if ai_bet == result['winner']:
                if ai_bet == 'Tie':
                    ai_gain = ai_amount * 8
                else:
                    ai_gain = ai_amount * (0.95 if ai_bet == 'Banker' else 1)
            elif ai_bet == 'Player Pair' and result['pair_player']:
                ai_gain = ai_amount * 11
            elif ai_bet == 'Banker Pair' and result['pair_banker']:
                ai_gain = ai_amount * 11
            else:
                ai_gain = -ai_amount
            st.session_state.ai_money[i] += ai_gain

        # 결과 기록
        st.session_state.logs.append({
            'Player': result['player'],
            'Banker': result['banker'],
            'Winner': result['winner'],
            'P_Total': result['player_total'],
            'B_Total': result['banker_total'],
            'UserMoney': st.session_state.user_money,
        })

        st.success(f"결과: {result['winner']} 승! 당신의 현재 자금: {st.session_state.user_money:,.0f}원")

# 게임 로그 출력
if st.session_state.logs:
    st.subheader("게임 기록")
    df = pd.DataFrame(st.session_state.logs)
    st.dataframe(df.tail(10), use_container_width=True)

# AI 수익 요약
ai_df = pd.DataFrame({'AI': range(NUM_AI), 'Balance': st.session_state.ai_money})
st.subheader("AI 수익 상위 TOP 10")
st.dataframe(ai_df.sort_values('Balance', ascending=False).head(10), use_container_width=True)
