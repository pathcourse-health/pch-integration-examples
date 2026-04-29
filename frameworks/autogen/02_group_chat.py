"""
AutoGen — three-agent group chat with mixed PCH models.

Run:
    pip install pyautogen autogen-pathcourse    # or: ag2 autogen-pathcourse
    export PCH_API_KEY=pch_prod_b_...
    python frameworks/autogen/02_group_chat.py

A planner, coder, and reviewer collaborate in an AutoGen GroupChat. Each
agent uses a PCH model matched to its job — pch-pro for planning, pch-coder
for implementation, pch-fast for review.
"""

from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent

from autogen_pathcourse import pch_config

planner = AssistantAgent(
    name="planner",
    llm_config={"config_list": pch_config(model="pch-pro")},
    system_message="You are a solutions architect. Plan implementations and break them into tasks.",
)

coder = AssistantAgent(
    name="coder",
    llm_config={"config_list": pch_config(model="pch-coder")},
    system_message="You are a senior engineer. Write clean, tested Python following the planner's instructions.",
)

reviewer = AssistantAgent(
    name="reviewer",
    llm_config={"config_list": pch_config(model="pch-fast")},
    system_message="You review code for correctness, style, and missing edge cases. Be specific. Reply 'TERMINATE' when satisfied.",
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=8,
    is_termination_msg=lambda m: "TERMINATE" in (m.get("content") or "").upper(),
    code_execution_config=False,
)

group = GroupChat(
    agents=[user_proxy, planner, coder, reviewer],
    messages=[],
    max_round=10,
)

manager = GroupChatManager(
    groupchat=group,
    llm_config={"config_list": pch_config(model="pch-fast")},   # cheap model is fine for orchestration
)

user_proxy.initiate_chat(
    manager,
    message=(
        "Implement a Python function `usdc_to_atomic(amount: float) -> int` that converts "
        "USDC amounts to their 6-decimal atomic representation. Plan it, implement it with "
        "tests, then review. Reply TERMINATE when done."
    ),
)
