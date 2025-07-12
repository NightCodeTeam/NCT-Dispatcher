from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BotMessage:
    chat_id: int
    message_id: int | None = None
    text: str = ''


class Test:
    @staticmethod
    def protect_text(func):
        def wrapper(self, *args, **kwargs):
            message = kwargs.get('message')
            if message is None:
                if len(args) > 0:
                    message = args[0]
            if message is None or type(message) is not BotMessage:
                return func(self, *args, **kwargs)

            message = BotMessage(
                chat_id=message.chat_id,
                message_id=message.message_id,
                text=message.text.replace('.', '\\.')
            )

            return func(self, message=message)
        return wrapper

    @protect_text
    def test(self, message: BotMessage):
        print(message)


msg = BotMessage(
    chat_id=1,
    message_id=1,
    text='hello.'
)
a = Test()
a.test()