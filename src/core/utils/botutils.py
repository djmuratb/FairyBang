# -*- coding: utf-8 -*-
from src.models import session, User, GirlsFilter, ExtendedGirlsFilter, Services


class BotUtils:
    @staticmethod
    def write_changes(obj, attr=None, value=None, only_commit=True):
        if attr and value:
            obj.__setattr__(attr, value)

        if not only_commit:
            session.add(obj)

        session.commit()

    @staticmethod
    def create_user(username):
        user = session.query(User).filter_by(username=username).first()
        if not user:
            user = User(username)
            user.girls_filter = GirlsFilter()
            user.extended_girls_filter = ExtendedGirlsFilter()
            user.services = Services()
            BotUtils.write_changes(user, only_commit=False)

        return user

    @staticmethod
    def get_message_data(obj, callback=False):
        """
        :param obj: message or call object
        :param callback: if param is callback query data
        :return: username, chat_id, message_id, text of object.
        """
        if callback:
            data = (obj.message.chat.username, obj.message.chat.id, obj.message.message_id, obj.data)
        else:
            data = (obj.chat.username, obj.chat.id, obj.message_id, obj.text)

        return data
