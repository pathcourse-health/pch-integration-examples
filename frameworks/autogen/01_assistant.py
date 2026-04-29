"""
AutoGen — single AssistantAgent on PCH.

Run:
    pip install pyautogen autogen-pathcourse    # or: ag2 autogen-pathcourse
    export PCH_API_KEY=pch_prod_b_...
    python frameworks/autogen/01_assistant.py

The simplest AutoGen pattern: one assistant answers a question via the
UserProxyAgent. Confirms the PCH config_list works end-to-end before you
move on to multi-agent group chats.
"""

from autogen import AssistantAgent, UserProxyAgent

from autogen_pathcourse import pch_config

llm_config = {"config_list": pch_config(model="pch-pro"), "temperature": 0.7}

assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="You are a helpful AI assistant. Be concise.",
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    code_execution_config=False,
)

user_proxy.initiate_chat(
    assistant,
    message="Explain x402 and why it matters for autonomous agents. Two sentences max.",
)
