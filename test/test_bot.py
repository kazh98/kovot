#! /usr/bin/env python
# coding:utf-8


import unittest
from typing import Callable, Iterator, Optional
from kovot import Bot
from kovot import Response
from kovot import Message
from kovot import Speaker


class EchoMod:
    def generate_responses(self, bot, message):
        res = Response(score=1.0,
                       text=message.text)
        return [res]


class SilentMod:
    def generate_responses(self, bot, message):
        return []


class StubStream(object):
    def __init__(self, callback: Optional[Callable[[Response], bool]] = None):
        self.callback = callback
        self.callback_num = 0

    def __iter__(self) -> Iterator[Message]:
        return iter([Message(text="テスト", speaker=Speaker(name="話し✋"))])

    def post(self, response: Response) -> bool:
        if self.callback:
            self.callback_num += 1
            return self.callback(response)
        return True


class BotTest(unittest.TestCase):
    def test_talk(self):
        msg = Message(text="テスト",
                      speaker=Speaker(name="話し✋"))
        bot = Bot(mods=[EchoMod()])

        res = bot.talk(msg)
        self.assertEqual(res, Response(score=1.0, text="テスト"))

    def test_talk_nocandidate(self):
        msg = Message(text="テスト",
                      speaker=Speaker(name="話し✋"))
        bot = Bot(mods=[SilentMod()])

        res = bot.talk(msg)
        self.assertIsNone(res)

    def test_talk_multimod(self):
        msg = Message(text="テスト",
                      speaker=Speaker(name="話し✋"))
        bot = Bot(mods=[EchoMod(), SilentMod()])

        res = bot.talk(msg)
        self.assertEqual(res, Response(score=1.0, text="テスト"))

    def test_run(self):
        def cb(res):
            self.assertEqual(res, Response(score=1.0, text="テスト"))
            return True
        bot = Bot(mods=[EchoMod()])
        stream = StubStream(callback=cb)
        bot.run(stream=stream)
        self.assertEqual(stream.callback_num, 1)

    def test_run_nocandidate(self):
        def cb(res):
            self.fail()
            return True
        bot = Bot(mods=[SilentMod()])
        stream = StubStream(callback=cb)
        bot.run(stream=stream)
        self.assertEqual(stream.callback_num, 0)

    def test_run_multimod(self):
        def cb(res):
            self.assertEqual(res, Response(score=1.0, text="テスト"))
            return True
        bot = Bot(mods=[EchoMod(), SilentMod()])
        stream = StubStream(callback=cb)
        bot.run(stream=stream)
        self.assertEqual(stream.callback_num, 1)
