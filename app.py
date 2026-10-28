
import random
import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="숫자 맞히기 게임 🎯",
    page_icon="🎯",
    layout="centered"
)

TIME_LIMIT = 120
MAX_LIVES = 5

def new_game():
    st.session_state.answer = random.randint(1, 100)
    st.session_state.lives = MAX_LIVES
    st.session_state.attempts = 0
    st.session_state.start_time = time.time()
    st.session_state.active = True
    st.session_state.message = "🍀 새 게임 시작! 숫자를 맞혀 보세요."
    st.session_state.result = None

if "answer" not in st.session_state:
    new_game()

# 게임 상태와 남은 시간 계산
if st.session_state.active:
    st_autorefresh(interval=1000, key="game_timer")
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, TIME_LIMIT - int(elapsed))

    if remaining <= 0:
        st.session_state.active = False
        st.session_state.result = "timeout"
        st.session_state.message = "⏰ 시간이 끝났어요!"
else:
    remaining = max(
        0,
        TIME_LIMIT - int(time.time() - st.session_state.start_time)
    )

# 제목과 설명
st.title("🎯 숫자 맞히기 게임")
st.write("컴퓨터가 고른 1부터 100 사이의 숫자를 맞혀 보세요!")

minutes, seconds = divmod(remaining, 60)

# 점수판
col1, col2 = st.columns(2)

with col1:
    st.metric("⏰ 남은 시간", f"{minutes:02d}:{seconds:02d}")

with col2:
    st.metric("🎯 시도 횟수", st.session_state.attempts)

st.progress(remaining / TIME_LIMIT)

st.subheader(
    "❤️ " * st.session_state.lives
    + "🖤 " * (MAX_LIVES - st.session_state.lives)
)

st.caption(f"남은 목숨: {st.session_state.lives} / {MAX_LIVES}")

# 숫자 입력 및 정답 확인
if st.session_state.active:
    with st.form("guess_form"):
        guess = st.number_input(
            "어떤 숫자일까요?",
            min_value=1,
            max_value=100,
            value=50,
            step=1
        )
        submitted = st.form_submit_button(
            "✨ 정답 확인!",
            use_container_width=True
        )

    if submitted:
        # 제출 시점에 시간 다시 확인
        elapsed = time.time() - st.session_state.start_time

        if elapsed >= TIME_LIMIT:
            st.session_state.active = False
            st.session_state.result = "timeout"
            st.session_state.message = "⏰ 시간이 끝났어요!"
        else:
            st.session_state.attempts += 1

            if guess == st.session_state.answer:
                st.session_state.active = False
                st.session_state.result = "won"
                st.session_state.message = (
                    f"🎉 정답입니다! 정답은 {st.session_state.answer}!"
                )

            else:
                st.session_state.lives -= 1

                if guess < st.session_state.answer:
                    hint = "⬆️ 정답은 더 큰 숫자예요!"
                else:
                    hint = "⬇️ 정답은 더 작은 숫자예요!"

                if st.session_state.lives <= 0:
                    st.session_state.active = False
                    st.session_state.result = "lost"
                    st.session_state.message = (
                        f"💔 목숨을 모두 사용했어요! "
                        f"정답은 {st.session_state.answer}였어요."
                    )
                else:
                    st.session_state.message = hint

        st.rerun()

# 안내 메시지
st.divider()
st.info(st.session_state.message)

if not st.session_state.active:
    if st.session_state.result == "won":
        st.balloons()
        st.success(
            f"🏆 {st.session_state.attempts}번 만에 성공했어요!"
        )
    elif st.session_state.result in ("lost", "timeout"):
        st.error("다음 게임에서는 꼭 성공해 보세요!")

    if st.button(
        "🔄 다시 시작하기",
        type="primary",
        use_container_width=True
    ):
        new_game()
        st.rerun()

st.caption("Made with ❤️ using Streamlit")
