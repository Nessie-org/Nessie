from nessie_api.models import Action, ConsoleMessage, ConsoleMessageType
from nessie_api.protocols import Context

import nessie_platform.constants as constants

types = {
    "ok": ConsoleMessageType.OK,
    "error": ConsoleMessageType.ERROR,
    "info": ConsoleMessageType.INFO,
    "warn": ConsoleMessageType.WARN,
    "input": ConsoleMessageType.INPUT,
}

def add_message(action: Action, context: Context):
    msg = action.payload.get("message", None)
    if msg is None or not isinstance(msg, dict):
        return
    msg_type = msg.get("type", None)
    if msg_type is None or not isinstance(msg_type, str):
        return
    content = msg.get("message", None)
    if content is None:
        return

    console_message = ConsoleMessage(content, types[msg_type])
    index = context.get_active_workspace_index()
    if index is None:
        return

    context.add_console_message_at(index, console_message)

def clear_console(action: Action, context: Context):
    index = context.get_active_workspace_index()
    if index is None:
        return
    context.clear_console_messages_at(index)