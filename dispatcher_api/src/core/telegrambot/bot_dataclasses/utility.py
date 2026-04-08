from .entity_dataclasses import Entity
from .user_dataclasses import User
from .chat_dataclasses import Chat
from .updates_dataclasses import UpdateMessage, UpdateCallback, Update
from .message_dataclasses import Message
from .callbacks_dataclasses import CallbackQuery


def get_chat_dc(update_part_with_chat: dict) -> Chat:
    return Chat(
        id=update_part_with_chat['id'],
        type=update_part_with_chat['type'],
        title=update_part_with_chat.get('title', ''),
        username=update_part_with_chat.get('username', ''),
        first_name=update_part_with_chat.get('first_name', ''),
        last_name=update_part_with_chat.get('last_name', ''),
        is_forum=update_part_with_chat.get('is_forum', False),
    )


def get_user_dc(update_part_with_user: dict | None) -> User | None:
    if update_part_with_user is None:
        return None
    return User(
        id=update_part_with_user['id'],
        is_bot=update_part_with_user['is_bot'],
        first_name=update_part_with_user['first_name'],
        last_name=update_part_with_user.get('last_name', ''),
        username=update_part_with_user.get('last_name', ''),
    )


def get_entities_dc(update_part_with_entities: dict | None) -> tuple[Entity, ...] | None:
    if update_part_with_entities is None:
        return None
    ans: list = []
    for entity in update_part_with_entities:
        ans.append(Entity(
            offset=entity['offset'],
            length=entity['length'],
            type=entity['type']
        ))
    return tuple(ans)


def get_users_in_list_dc(update_part_with_users: dict | None) -> tuple[User, ...] | None:
    if update_part_with_users is None:
        return None
    ans: list = []
    for user in update_part_with_users:
        ans.append(get_user_dc(user))
    return tuple(ans)


def get_message_dc(update_part_with_message: dict | None) -> Message | None:
    if update_part_with_message is None:
        return None
    return Message(
        message_id=update_part_with_message['message_id'],
        message_thread_id=update_part_with_message.get('message_thread_id'),
        date=update_part_with_message['date'],
        chat=get_chat_dc(update_part_with_message['chat']),
        from_user=get_user_dc(update_part_with_message.get('from')),
        reply_to_message=update_part_with_message.get('reply_to_message'),
        text=update_part_with_message.get('text'),
        entities=get_entities_dc(update_part_with_message.get('entities')),
        new_chat_members=get_users_in_list_dc(update_part_with_message.get('new_chat_members')),
        left_chat_member=get_users_in_list_dc(update_part_with_message.get('left_chat_members')),
    )


def get_callback_dc(update_dict_with_callback: dict) -> CallbackQuery | None:
    from_user=get_user_dc(update_dict_with_callback['from'])
    if from_user is None:
        return None
    return CallbackQuery(
        id=update_dict_with_callback['id'],
        from_user=from_user,
        chat_instance=update_dict_with_callback['chat_instance'],
        message=get_message_dc(update_dict_with_callback.get('message')),
        data=update_dict_with_callback.get('data')
    )


def get_update_dc(update_dict: dict) -> Update | None:
    if update_dict.get('message') is not None:
        message=get_message_dc(update_dict['message'])
        if message is None:
            return None
        return UpdateMessage(
            update_id=update_dict['update_id'],
            message=message
        )
    elif update_dict.get('callback_query') is not None:
        callback_query=get_callback_dc(update_dict['callback_query'])
        if callback_query is None:
            return None
        return UpdateCallback(
            update_id=update_dict['update_id'],
            callback_query=callback_query
        )
