import os
import sys
import time

# ---------------------------------------------------------
# Make project root available for imports
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
import os
import sys
import time

# ---------------------------------------------------------
# Make project root available for imports
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
# Environment
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="TechNova Customer Support",
    page_icon="🛒",
    layout="centered"
)


# ---------------------------------------------------------
# Compact page spacing
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Reduce sidebar top spacing */
    [data-testid="stSidebarContent"] {
        padding-top: 0.5rem;
    }

    [data-testid="stSidebarHeader"] {
        height: 0rem;
        min-height: 0rem;
    }

    /* Reduce main page top spacing */
    [data-testid="stMainBlockContainer"] {
        padding-top: 1.5rem;
    }

    /* Remove extra space above the main title */
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
# LangSmith client
# ---------------------------------------------------------

langsmith_client = Client()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("🛒 TechNova")


    # -----------------------------------------------------
    # Demo Questions
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Supported topics
    # -----------------------------------------------------

    st.write(
        "AI customer support assistant for:"
    )

    st.write("• Order status")
    st.write("• Returns")
    st.write("• Warranty")
    st.write("• Shipping")


    st.divider()


    # -----------------------------------------------------
    # Available Demo Data
    # -----------------------------------------------------

    st.subheader("📌 Sample Orders")

    st.markdown(
        """
        **TN1001** — Laptop Pro 14  
        **TN1002** — Noise-cancel Earbuds  
        **TN1003** — Phone X
        """
    )


    st.divider()


    # -----------------------------------------------------
    # Model
    # -----------------------------------------------------

    st.subheader("Model")

    st.code(MODEL_NAME)


    st.divider()


    # -----------------------------------------------------
    # Session
    # -----------------------------------------------------

    st.subheader("Session")

    st.code(
        st.session_state.thread_id
    )


    st.divider()


    # -----------------------------------------------------
    # Clear conversation
    # -----------------------------------------------------

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []

        st.session_state.thread_id = (
            f"streamlit-{int(time.time())}"
        )

        st.rerun()


# ---------------------------------------------------------
# Main page
# ---------------------------------------------------------

st.title("🛒 TechNova Customer Support")

st.caption(
    "AI-powered customer support using "
    "LangGraph + NVIDIA + LangSmith"
)


# ---------------------------------------------------------
# Display previous conversation
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


        # -------------------------------------------------
        # Feedback buttons
        # -------------------------------------------------

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
                    key=f"up_{message['run_id']}"
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
                    key=f"down_{message['run_id']}"
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


if user_question:

    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)


    # -----------------------------------------------------
    # LangGraph configuration
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Run chatbot
    # -----------------------------------------------------

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
                # Get final response
                # -------------------------------------------------

                answer = (
                    result["messages"][-1].content
                )

                st.markdown(answer)


                # -------------------------------------------------
                # Give LangSmith time to record the run
                # -------------------------------------------------

                time.sleep(1)


                # -------------------------------------------------
                # Find latest LangGraph run
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

                            run_id = str(run.id)

                            break

                except Exception:

                    run_id = None


                # -------------------------------------------------
                # Store assistant response
                # -------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "run_id": run_id
                    }
                )


                # -------------------------------------------------
                # LangSmith status
                # -------------------------------------------------

                if run_id:

                    st.caption(
                        "✓ Response traced in LangSmith"
                    )


            except Exception:

                # -------------------------------------------------
                # Friendly failure message
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

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import streamlit as st
from dotenv import load_dotenv
from langsmith import Client

from app.graph import graph, MODEL_NAME


# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="TechNova Customer Support",
    page_icon="🛒",
    layout="centered"
)


# ---------------------------------------------------------
# Compact sidebar spacing
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    [data-testid="stSidebarContent"] {
        padding-top: 0.5rem;
    }

    [data-testid="stSidebarHeader"] {
        height: 0rem;
        min-height: 0rem;
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
# LangSmith client
# ---------------------------------------------------------

langsmith_client = Client()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("🛒 TechNova")


    # -----------------------------------------------------
    # Demo Questions
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Supported topics
    # -----------------------------------------------------

    st.write(
        "AI customer support assistant for:"
    )

    st.write("• Order status")
    st.write("• Returns")
    st.write("• Warranty")
    st.write("• Shipping")


    st.divider()


    # -----------------------------------------------------
    # Available Demo Data
    # -----------------------------------------------------

    st.subheader("📌 Sample Orders")

    st.markdown(
        """
        **TN1001** — Laptop Pro 14  
        **TN1002** — Noise-cancel Earbuds  
        **TN1003** — Phone X
        """
    )


    st.divider()


    # -----------------------------------------------------
    # Model
    # -----------------------------------------------------

    st.subheader("Model")

    st.code(MODEL_NAME)


    st.divider()


    # -----------------------------------------------------
    # Session
    # -----------------------------------------------------

    st.subheader("Session")

    st.code(
        st.session_state.thread_id
    )


    st.divider()


    # -----------------------------------------------------
    # Clear conversation
    # -----------------------------------------------------

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []

        st.session_state.thread_id = (
            f"streamlit-{int(time.time())}"
        )

        st.rerun()


# ---------------------------------------------------------
# Main page
# ---------------------------------------------------------

st.title("🛒 TechNova Customer Support")

st.caption(
    "AI-powered customer support using "
    "LangGraph + NVIDIA + LangSmith"
)


# ---------------------------------------------------------
# Display previous conversation
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


        # -------------------------------------------------
        # Feedback buttons
        # -------------------------------------------------

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
                    key=f"up_{message['run_id']}"
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
                    key=f"down_{message['run_id']}"
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


if user_question:

    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)


    # -----------------------------------------------------
    # LangGraph configuration
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Run chatbot
    # -----------------------------------------------------

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
                # Get final response
                # -------------------------------------------------

                answer = (
                    result["messages"][-1].content
                )

                st.markdown(answer)


                # -------------------------------------------------
                # Give LangSmith time to record the run
                # -------------------------------------------------

                time.sleep(1)


                # -------------------------------------------------
                # Find latest LangGraph run
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

                            run_id = str(run.id)

                            break

                except Exception:

                    run_id = None


                # -------------------------------------------------
                # Store assistant response
                # -------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "run_id": run_id
                    }
                )


                # -------------------------------------------------
                # LangSmith status
                # -------------------------------------------------

                if run_id:

                    st.caption(
                        "✓ Response traced in LangSmith"
                    )


            except Exception:

                # -------------------------------------------------
                # Friendly failure message
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
