import requests
import streamlit as st
import os


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/ask")


st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 Enterprise Knowledge Assistant")

st.caption(
    "Ask questions from enterprise documents and get grounded answers with source references."
)


question = st.text_area(
    "Enter your question",
    placeholder="Example: What are the evaluation criteria?",
    height=100,
)


if st.button("Ask Assistant", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching knowledge base and generating answer..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=60,
                )

                response.raise_for_status()
                data = response.json()

                st.subheader("Answer")
                st.write(data["answer"])

                st.subheader("Sources")

                if data.get("sources"):
                    for source in data["sources"]:
                        document = source.get("document", "Unknown document")
                        page = source.get("page", "N/A")
                        section = source.get("section") or "N/A"

                        st.markdown(
                            f"- **{document}** | Page: `{page}` | Section: `{section}`"
                        )
                else:
                    st.info("No sources available.")

                st.divider()

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Confidence", f"{data.get('confidence', 0) * 100:.0f}%")

                with col2:
                    st.metric("Retrieved Chunks", data.get("retrieved_chunks", 0))

                with col3:
                    st.metric(
                        "Processing Time",
                        f"{data.get('processing_time_ms', 0):.0f} ms",
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the FastAPI backend. Make sure it is running on http://127.0.0.1:8000"
                )

            except requests.exceptions.Timeout:
                st.error("The request timed out. Please try again.")

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")