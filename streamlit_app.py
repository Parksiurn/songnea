import streamlit as st
import random
import pandas as pd
from collections import deque

# 카드 생성
def create_deck(num_decks=8):
    single_deck = [1,2,3,4,5,6,7,8,9,0,0,0,0] * 4
    return deque(random.sample(single_deck * num_decks, len(single_deck) * num_decks))

# 카드 합 계산
def calc_hand_value(hand):
    return sum(hand) % 10

# 카드 뽑기
def draw_card(deck):
    return deck.popleft()

# 플레이어 추가 카드 규칙
def player_draw_rule(hand):
    total = calc_hand_value(hand)
    return total <= 5

# 뱅커 추가 카드 규칙
def banker_draw_rule(banker_hand, player_third):
    total = calc_hand_value(banker_hand)
    if total <= 2:
        return True
    elif total == 3:
        return player_third != 8
    elif total == 4:
        return player_third in [2,3,4,5,6,7]
    elif total == 5:
        return player_third in [4,5,6,7]
    elif total == 6:
        return player_third in [6,7]
    return False

# AI 베팅 결정
def ai_bets(last_result, pair_limit=0.1):
    bets = []
    for _ in range(500):
        bet = {}
        rand = random.random()
        if last_result == 'Player':
            bet['main'] = 'Player' if rand < 0.6 else 'Banker'
        elif last_result == 'Banker':
            bet['main'] = 'Banker' if rand < 0.6 else 'Player'
        else:
            bet['main'] = 'Player' if rand < 0.5 else 'Banker'

        # Tie와 Pair는 제한적
        bet['tie'] = random.random() < 0.05
        if random.random() < pair_limit:
            bet['player_pair'] = random.choice([True, False])
            bet['banker_pair'] = not bet['player_pair']
        else:
            bet['player_pair'] = False
            bet['banker_pair'] = False

        bets.append(bet)
    return bets

# 베팅 정산
def settle_bet(bet, result, player_pair, banker_pair):
    payout = 0
    if bet.get('main') == result:
        payout += 2
        if result == "Banker":
            payout -= 0.05
    if bet.get('tie') and result == "Tie":
        payout += 8
    if bet.get('player_pair') and player_pair:
        payout += 11
    if bet.get('banker_pair') and banker_pair:
        payout += 11
    return payout

# 게임 실행
def play_round(deck, user_bet, ai_bet_list, ai_profits, last_result):
    if len(deck) < 6:
        return None

    player_hand = [draw_card(deck), draw_card(deck)]
    banker_hand = [draw_card(deck), draw_card(deck)]

    player_pair = player_hand[0] == player_hand[1]
    banker_pair = banker_hand[0] == banker_hand[1]

    if player_draw_rule(player_hand):
        player_third = draw_card(deck)
        player_hand.append(player_third)
    else:
        player_third = None

    if player_third is not None:
        if banker_draw_rule(banker_hand, player_third):
            banker_hand.append(draw_card(deck))
    else:
        if calc_hand_value(banker_hand) <= 5:
            banker_hand.append(draw_card(deck))

    player_total = calc_hand_value(player_hand)
    banker_total = calc_hand_value(banker_hand)

    if player_total > banker_total:
        result = "Player"
    elif player_total < banker_total:
        result = "Banker"
    else:
        result = "Tie"

    # AI 정산
    for i, bet in enumerate(ai_bet_list):
        profit = settle_bet(bet, result, player_pair, banker_pair) - 1
        ai_profits[i] += profit

    # 사용자 정산
    user_profit = settle_bet(user_bet, result, player_pair, banker_pair) - 1

    round_result = {
        "Player": player_hand,
        "Banker": banker_hand,
        "승자": result,
        "Player Pair": player_pair,
        "Banker Pair": banker_pair,
        "User 수익": user_profit,
    }

    return round_result, result

# Streamlit 앱
st.title("바카라 게임 시뮬레이터")

# 초기화
if 'deck' not in st.session_state:
    st.session_state.deck = create_deck()
    st.session_state.history = []
    st.session_state.last_result = None
    st.session_state.user_money = 200
    st.session_state.ai_profits = [0 for _ in range(500)]

st.subheader(f"당신의 보유금: {st.session_state.user_money:.0f}만원")

# 베팅 입력
bet_main = st.selectbox("주 베팅", ["Player", "Banker", "Tie"])
bet_player_pair = st.checkbox("Player Pair")
bet_banker_pair = st.checkbox("Banker Pair")
submit = st.button("베팅 후 다음 라운드 진행")

if submit:
    user_bet = {
        "main": bet_main,
        "tie": bet_main == "Tie",
        "player_pair": bet_player_pair,
        "banker_pair": bet_banker_pair
    }

    ai_bet_list = ai_bets(st.session_state.last_result)
    result = play_round(st.session_state.deck, user_bet, ai_bet_list, st.session_state.ai_profits, st.session_state.last_result)

    if result:
        round_data, new_result = result
        st.session_state.history.append(round_data)
        st.session_state.user_money += round_data['User 수익']
        st.session_state.last_result = new_result
    else:
        st.warning("카드가 부족하여 게임이 종료됩니다.")

# 결과 테이블
if st.session_state.history:
    st.subheader("게임 결과")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df[::-1])

# AI 수익 테이블
st.subheader("AI 개별 수익 (상위 10명)")
ai_df = pd.DataFrame({
    "AI ID": [f"AI_{i+1}" for i in range(500)],
    "수익": st.session_state.ai_profits
})
top10 = ai_df.sort_values(by="수익", ascending=False).head(10)
st.table(top10.reset_index(drop=True))
