import streamlit as st
import openai
import io
from PIL import Image
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI API KEY ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- 제목 ---
st.title("감정 위로 카드 생성기 :heartpulse:")

# --- 감정 입력 ---
emotion_prompt = st.text_area("당신의 감정을 입력해주세요.", placeholder="예: 요즘 너무 힘들어요...")

# --- 버튼 ---
if st.button("GPT-4o로 위로받기"):
    if not emotion_prompt.strip():
        st.warning("감정을 입력해 주세요!")
    else:
        with st.spinner("GPT-4o가 위로 메시지를 작성 중입니다..."):
            gpt_response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "당신은 다정하게 위로해주는 친구입니다."},
                    {"role": "user", "content": f"내가 이렇게 말했을 때 따뜻하게 위로해줘: {emotion_prompt}"}
                ],
                max_tokens=200,
                temperature=0.7,
            )
            comforting_message = gpt_response.choices[0].message.content
            st.session_state['comforting_message'] = comforting_message
        st.success("위로 메시지가 생성되었습니다 :blush:")
        st.markdown(f"**위로 메시지:**\n\n{comforting_message}")

# 카드 생성
if 'comforting_message' in st.session_state:
    if st.button("카드 생성(이미지 포함)"):
        with st.spinner("이미지를 생성 중입니다..."):
            # 이미지 프롬프트 생성 (GPT를 통해 감정과 메시지에 어울리는 프롬프트 생성)
            image_prompt = f"{emotion_prompt}와 어울리는 따뜻하고 희망적인 분위기의 일러스트"
            response = openai.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            img_url = response.data[0].url
            image = Image.open(requests.get(img_url, stream=True).raw)
            st.session_state['comforting_image'] = image
            st.image(image, caption="당신을 위한 위로 카드", use_column_width=True)

# 다운로드 버튼
if 'comforting_image' in st.session_state:
    img_byte_arr = io.BytesIO()
    st.session_state['comforting_image'].save(img_byte_arr, format='PNG')
    st.download_button(
        label="이미지 다운로드",
        data=img_byte_arr.getvalue(),
        file_name="comforting_card.png",
        mime="image/png"
    )

# --- 참고: secrets.toml ---
# [OPENAI_API_KEY]  
# "your_openai_api_key"

