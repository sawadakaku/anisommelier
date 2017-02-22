# -*- coding: utf-8 -*-
import os
import random
import binascii
import logging
import webapp2
from webapp2_extras import sessions
from google.appengine.ext import ndb
from modules import mydb
from modules import functions

questions = [
    u"あなたの性別は？",
    u"どちらが好き？",
    u"好きな食べ物は？",
    u"今日の天気は？",
    u"お腹すいた",
    u"腰痛い"
]
answers = [
    (u"男",u"女"),
    (u"ゆゆ式",u"きんもざ"),
    (u"りんご",u"ごりら"),
    (u"晴れ",u"雨"),
    (u"わかる",u"わからない"),
    (u"痛い",u"痛くない")
]
animetitle = [
    u"ゼロの使い魔",
    u"化物語",
    u"今日の5の2"
]

# セッションを導入する(無視して良い)
class SessionEnabledHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

# 最初のページ(無視して良い)
class MainPage(SessionEnabledHandler):
    def get(self):
        functions.dorender(self, '/main.html')


class DotJsonHandler(SessionEnabledHandler):
    def get(self):
        json_file = os.path.join(os.path.dirname(__file__), 'templates', 'dot.json')
        f = open(json_file,'r')
        json_data = f.read()
        f.close
        self.response.headers['Content-type'] = 'application/json'
        self.response.out.write(json_data)


"""
前回までの質問から今回の質問を生成する部分(ここの実装をおねがいします)
"""
class QuestionHandler(SessionEnabledHandler):
    # 最初の質問を決定する
    def get(self):
        sessionID = binascii.hexlify(os.urandom(8))
        self.session['sessionID'] = sessionID
        ques = {'questions':questions, 'answers':answers, 'questionNum':0}          # 最初の質問はとりあえず0で決め打ち
        functions.dorender(self, '/question.html', ques)

    # 2回目以降の質問を決定する
    def post(self):
        sessionID = self.session.get('sessionID')
        personal_answer = mydb.Personalanswer(parent=ndb.Key('User', sessionID))
        question = self.request.arguments()[0]         # 前回の質問の番号 (文字列型)
        answer = self.request.get(question)             # 前回の回答(0or1) (文字列型)
        personal_answer.question = question
        personal_answer.answer = answer
        personal_answer.put()
        """
        この場所にすごいアルゴリズムを書く
        今までの質問と答えの組から，終了か続行かを決定し
        続行ならば次の質問の番号を求め
        終了ならば目的のアニメを求める
        """
        answer_query = mydb.Personalanswer.query(ancestor=ndb.Key('User', sessionID))
        personal_answers = answer_query.fetch(limit=100)        # 前回までの質問と答えの組(イテレータ)
        for qanda in personal_answers:
            logging.info(qanda.question)                                    # 質問の番号(文字列型)
            logging.info(questions[int(qanda.question)])
            logging.info(qanda.answer)                                      # 答え(0or1)(文字列型)
            logging.info(answers[int(qanda.question)][int(qanda.answer)])

        length = len(personal_answers)
        logging.info(length)
        # 終了する場合
        if length>5:            #終了条件，とりあえず全ての質問を終えたときに設定
            titleNum = random.randint(0,2)          # 目的のアニメの番号，とりあえずランダムに
            ques = {'animetitle':animetitle, 'titleNum':titleNum}
            functions.dorender(self, '/result.html', ques)
        # 続行する場合
        else:
            questionNum = int(question)+1           # 次の質問の番号，とりあえず前回の質問番号＋１にする
            ques = {'questions':questions, 'answers':answers, 'questionNum':questionNum}
            functions.dorender(self, '/question.html', ques)

config = {}
config['webapp2_extras.sessions'] = {
        'secret_key' : 'my-secret-key'
        }
logging.getLogger().setLevel(logging.DEBUG)
app = webapp2.WSGIApplication([('/getdot', DotJsonHandler),
                               ('/nextquestion', QuestionHandler),
                               ('/.*', MainPage),],
                               config=config,
                               debug=True)
