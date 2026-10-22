import json
import streamlit as st
from logic import analyze

import tempfile
from pathlib import Path

st.set_page_config(
    page_title="Chat Analyzer",
    page_icon="💬",
    layout="wide",
)

st.title("Chat Analyzer")
st.write("Загрузи переписку, чтобы проанализировать её с помощью Ollama.")

with st.sidebar:
    st.header("Настройки")

    model = st.text_input(
        "Модель Ollama",
        value="qwen3.5:9b",
    )

    context = st.number_input(
        "Размер контекста",
        min_value=1024,
        max_value=131072,
        value=8192,
        step=1024,
    )

uploaded_file = st.file_uploader(
    "Выбери файл с перепиской",
    type=["txt", "md", "log", "json"],
)

if uploaded_file is not None:
    chat_text = uploaded_file.getvalue().decode("utf-8")

    st.subheader("Предпросмотр переписки")
    st.text_area(
        "Содержимое файла",
        value=chat_text,
        height=200,
        disabled=True,
    )

    if st.button("Анализировать", type="primary"):
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                suffix=".txt",
                delete=False,
            ) as temp_file:
                temp_file.write(chat_text)
                temp_path = Path(temp_file.name)

            with st.spinner("Анализирую переписку..."):
                result = analyze(temp_path, model, int(context))

            st.success("Анализ завершён")

            st.subheader("Результаты:")

            for key, value in result.items():
                if key == "scores":
                    st.markdown("### Оценки")
                    st.json(value)
                else:
                    st.markdown(f"### {key.replace('_', ' ').title()}")
                    st.write(value)

            st.download_button(
                "Скачать результат JSON",
                data=json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=2,
                ),
                file_name="analysis.json",
                mime="application/json",
            )

        except Exception as error:
            st.error(f"Ошибка при анализе: {error}")

        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
else:
    st.info("Сначала загрузи файл с перепиской.")
