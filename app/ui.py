import os
import sys
import time

# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import streamlit as st
from dotenv import load_dotenv
from langsmith import Client

from app.graph import graph, MODEL_NAME


# ---------------------------------------------------------
# Load environment
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="TechNova Customer Support",
    page_icon="🛒",
    layout="centered"
)


# ---------------------------------------------------------
# Compact layout
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Sidebar spacing */
    [data-testid="stSidebarContent"] {
        padding-top: 0.5rem;
    }

    [data-testid="stSidebarHeader"] {
        height: 0rem;
        min-height: 0rem;
    }

    /* Main content spacing */
    [data-testid="stMainBlockContainer"] {
        padding-top: 1.5rem;
    }

    [data-testid="stMainBlockContainer"] h1 {
        margin-top: 0rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = (
        f"streamlit-{int(time.time())}"
    )


# ---------------------------------------------------------
# LangSmith
# ---------------------------------------------------------

langsmith_client = Client()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("🛒 TechNova")


    # =====================================================
    # TRY THESE QUESTIONS
    # =====================================================

    st.subheader("🧪 Try These Questions")


    with st.expander(
        "📦 Order Questions",
        expanded=False
    ):

        st.markdown(
            """
            **Try:**

            • What is the status of order **TN1001**?

            • What is the item in order **TN1002**?

            • What is the status of order **TN1003**?
            """
        )


    with st.expander(
        "📋 Policy Questions",
        expanded=False
    ):

        st.markdown(
            """
            **Try:**

            • What is the return policy?

            • What is the warranty policy?

            • Is shipping free for orders above Rs.999?

            • How long does standard delivery take?
            """
        )


    with st.expander(
        "🧠 Memory Test",
        expanded=False
    ):

        st.markdown(
            """
            Ask these questions one after another:

            **1.** What is the status of order TN1001?

            **2.** What was the item in that order?

            The second question tests conversation memory.
            """
        )


    with st.expander(
        "🛡️ Guardrail & Error Tests",
        expanded=False
    ):

        st.markdown(
            """
            **Unknown order:**

            • What is the status of order **TN9999**?

            **Off-topic question:**

            • What is the weather today?

            These demonstrate error handling and
            the chatbot's guardrail.
            """
        )


    # =====================================================
    # SUPPORTED TOPICS
    # =====================================================

    st.write(
        "AI customer support assistant for:"
    )

    st.write("• Order status")
    st.write("• Returns")
    st.write("• Warranty")
    st.write("• Shipping")


    st.divider()


    # =====================================================
    # SAMPLE ORDERS
    # =====================================================

    st.subheader("📌 Sample Orders")

    st.markdown(
        """
        **TN1001** — Laptop Pro 14

        **TN1002** — Noise-cancel Earbuds

        **TN1003** — Phone X
        """
    )


    st.divider()


    # =====================================================
    # MODEL
    # =====================================================

    st.subheader("Model")

    st.code(MODEL_NAME)


    st.divider()


    # =====================================================
    # SESSION
    # =====================================================

    st.subheader("Session")

    st.code(
        st.session_state.thread_id
    )


    st.divider()


    # =====================================================
    # CLEAR CONVERSATION
    # =====================================================

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True,
        key="clear_conversation_button"
    ):

        st.session_state.messages = []

        st.session_state.thread_id = (
            f"streamlit-{int(time.time())}"
        )

        st.rerun()


# ---------------------------------------------------------
# Main title
# ---------------------------------------------------------

st.title("🛒 TechNova Customer Support")

st.caption(
    "AI-powered customer support using "
    "LangGraph + NVIDIA + LangSmith"
)


# ---------------------------------------------------------
# Display conversation history
# ---------------------------------------------------------

for message_index, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


        # =================================================
        # Assistant feedback
        # =================================================

        if (
            message["role"] == "assistant"
            and message.get("run_id")
        ):

            col1, col2 = st.columns(2)


            # -------------------------------------------------
            # Helpful
            # -------------------------------------------------

            with col1:

                if st.button(
                    "👍 Helpful",
                    key=f"helpful_{message_index}_{message['run_id']}"
                ):

                    try:

                        langsmith_client.create_feedback(
                            message["run_id"],
                            key="user_rating",
                            score=1,
                            comment=(
                                "User marked the response "
                                "as helpful."
                            )
                        )

                        st.success(
                            "Thanks for your feedback!"
                        )

                    except Exception as error:

                        st.error(
                            f"Could not send feedback: {error}"
                        )


            # -------------------------------------------------
            # Not helpful
            # -------------------------------------------------

            with col2:

                if st.button(
                    "👎 Not helpful",
                    key=f"not_helpful_{message_index}_{message['run_id']}"
                ):

                    try:

                        langsmith_client.create_feedback(
                            message["run_id"],
                            key="user_rating",
                            score=0,
                            comment=(
                                "User marked the response "
                                "as not helpful."
                            )
                        )

                        st.success(
                            "Thanks for your feedback!"
                        )

                    except Exception as error:

                        st.error(
                            f"Could not send feedback: {error}"
                        )


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

user_question = st.chat_input(
    "Ask about your order, returns, warranty, or shipping..."
)


# ---------------------------------------------------------
# Process user question
# ---------------------------------------------------------

if user_question:

    # =====================================================
    # Save user message
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )


    # =====================================================
    # Display user message
    # =====================================================

    with st.chat_message("user"):

        st.markdown(user_question)


    # =====================================================
    # LangGraph configuration
    # =====================================================

    config = {

        "configurable": {
            "thread_id": st.session_state.thread_id
        },

        "metadata": {
            "model_name": MODEL_NAME,
            "user_id": "streamlit-user",
            "app_version": "1.0.0",
            "session_id": st.session_state.thread_id
        },

        "tags": [
            "technova-bot",
            "streamlit-ui",
            "production-demo"
        ]
    }


    # =====================================================
    # Generate response
    # =====================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "TechNova is thinking..."
        ):

            try:

                result = graph.invoke(
                    {
                        "messages": [
                            ("user", user_question)
                        ]
                    },
                    config=config
                )


                # -------------------------------------------------
                # Get final assistant response
                # -------------------------------------------------

                answer = result[
                    "messages"
                ][-1].content


                st.markdown(answer)


                # -------------------------------------------------
                # Give LangSmith time to record the run
                # -------------------------------------------------

                time.sleep(1)


                # -------------------------------------------------
                # Find LangGraph run
                # -------------------------------------------------

                run_id = None

                try:

                    project_name = os.getenv(
                        "LANGSMITH_PROJECT"
                    )

                    runs = list(
                        langsmith_client.list_runs(
                            project_name=project_name,
                            limit=20
                        )
                    )


                    for run in runs:

                        if run.name == "LangGraph":

                            run_id = str(
                                run.id
                            )

                            break


                except Exception:

                    run_id = None


                # -------------------------------------------------
                # Save assistant message
                # -------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "run_id": run_id
                    }
                )


                # -------------------------------------------------
                # LangSmith indicator
                # -------------------------------------------------

                if run_id:

                    st.caption(
                        "✓ Response traced in LangSmith"
                    )


            except Exception:

                # -------------------------------------------------
                # Friendly error
                # -------------------------------------------------

                answer = (
                    "I'm sorry, but I'm currently "
                    "unable to process your request. "
                    "Please try again later."
                )


                st.error(answer)


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "run_id": None
                    }
                )
