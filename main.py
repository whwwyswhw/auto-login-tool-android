# -*- coding: utf-8 -*-
"""
PK10 Betting Assistant - Kivy version v1.0
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import requests
import json
import os
import threading

# 球号颜色（标准 PK10）
BALL_COLORS = {
    "1": "#E6DE00", "2": "#0092DD", "3": "#4C4C4C", "4": "#FF8C00", "5": "#00CCCC",
    "6": "#8B00C9", "7": "#BCBCBC", "8": "#E60000", "9": "#8B0000", "10": "#00AA00"
}
BALL_COLORS_KIVY = {k: get_color_from_hex(v) for k, v in BALL_COLORS.items()}

GAMES = {
    "极速赛车": "10001",
    "幸运飞艇": "10002",
}
DRAW_API = "https://api.api68.com/pks/getLotteryPksInfo.do"
CFG_PATH = os.path.join(os.path.expanduser("~"), "pk10_config.json")


class PK10App(App):
    def build(self):
        self.selected = set()
        self.current_game = "极速赛车"
        self.session = requests.Session()

        root = BoxLayout(orientation="vertical", padding=8, spacing=4)

        # 顶栏：游戏选择 + 期号 + 在线状态
        top = BoxLayout(orientation="horizontal", size_hint_y=None, height=36)
        self.game_spinner = Spinner(
            text="极速赛车", values=list(GAMES.keys()),
            size_hint_x=None, width=120
        )
        self.game_spinner.bind(text=self._on_game_change)
        self.period_lbl = Label(text="期号: --", size_hint_x=1)
        self.status_lbl = Label(text="● 离线", color=(1, 0, 0, 1),
                               size_hint_x=None, width=80)
        top.add_widget(self.game_spinner)
        top.add_widget(self.period_lbl)
        top.add_widget(self.status_lbl)
        root.add_widget(top)

        # 开奖信息
        self.code_lbl = Label(text="开奖: --", size_hint_y=None, height=28)
        self.next_lbl = Label(text="下期: --", size_hint_y=None, height=28)
        root.add_widget(self.code_lbl)
        root.add_widget(self.next_lbl)

        # 选号区
        root.add_widget(Label(text="选号 (1-10):", size_hint_y=None, height=28,
                              halign="left"))
        balls = GridLayout(cols=5, spacing=4, size_hint_y=None, height=68)
        self.ball_btns = {}
        for i in range(1, 11):
            btn = Button(
                text=str(i),
                background_normal="",
                background_color=BALL_COLORS_KIVY[str(i)],
                color=(0, 0, 0, 1),
                bold=True,
                on_press=self._on_ball_press
            )
            btn._num = i
            self.ball_btns[i] = btn
            balls.add_widget(btn)
        root.add_widget(balls)

        # 已选 + 金额
        self.sel_lbl = Label(text="已选: --", size_hint_y=None, height=28)
        self.amt_in = TextInput(text="10", size_hint_y=None, height=36,
                                multiline=False, hint_text="金额")
        root.add_widget(self.sel_lbl)
        root.add_widget(self.amt_in)

        # 账号/密码
        self.user_in = TextInput(hint_text="账号", size_hint_y=None, height=36,
                                 multiline=False)
        self.pwd_in = TextInput(hint_text="密码", password=True,
                                size_hint_y=None, height=36, multiline=False)
        root.add_widget(self.user_in)
        root.add_widget(self.pwd_in)

        # 按钮行
        btn_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=44, spacing=6)
        for txt, cb in [("登录", self._on_login), ("投注", self._on_bet),
                        ("刷新", self._on_refresh)]:
            btn_row.add_widget(Button(text=txt, on_press=cb))
        root.add_widget(btn_row)

        # 日志
        self.log_lbl = Label(text="日志: 等待操作...",
                             size_hint_y=None, height=48)
        root.add_widget(self.log_lbl)

        # 加载配置 + 自动刷新
        self._load_cfg()
        Clock.schedule_once(lambda dt: self._do_refresh(), 2)
        return root

    # ── 配置 ──
    def _load_cfg(self):
        try:
            with open(CFG_PATH) as f:
                cfg = json.load(f)
            self.user_in.text = cfg.get("user", "")
            self.pwd_in.text = cfg.get("pwd", "")
            g = cfg.get("game", "极速赛车")
            if g in GAMES:
                self.game_spinner.text = g
                self.current_game = g
        except Exception:
            pass

    def _save_cfg(self):
        try:
            with open(CFG_PATH, "w") as f:
                json.dump({"user": self.user_in.text,
                           "pwd": self.pwd_in.text,
                           "game": self.game_spinner.text}, f)
        except Exception:
            pass

    # ── 选号 ──
    def _on_ball_press(self, btn):
        n = btn._num
        if n in self.selected:
            self.selected.remove(n)
            btn.background_color = BALL_COLORS_KIVY[str(n)]
        else:
            self.selected.add(n)
            btn.background_color = (0, 0.7, 0, 1)  # 选中变绿色
        self.sel_lbl.text = "已选: " + (",".join(map(str, sorted(self.selected)))
                                        if self.selected else "--")

    # ── 开奖 ──
    def _on_game_change(self, spinner, text):
        self.current_game = text
        self._save_cfg()

    def _on_refresh(self, *a):
        self.log_lbl.text = "日志: 获取开奖中..."
        threading.Thread(target=self._fetch_draw, daemon=True).start()

    def _fetch_draw(self):
        try:
            r = self.session.get(
                DRAW_API, params={"lotCode": GAMES[self.current_game]},
                timeout=10, headers={"User-Agent": "Mozilla/5.0"}
            )
            d = r.json().get("result", {}).get("data", {})
            if not d:
                self.log_lbl.text = "日志: 暂无数据"
                return
            self.period_lbl.text = f"期号: {d.get('preDrawIssue', '--')}"
            self.code_lbl.text = f"开奖: {d.get('preDrawCode', '--')}"
            self.next_lbl.text = f"下期: {d.get('drawIssue', '--')}"
            self.log_lbl.text = "日志: 开奖更新成功"
        except Exception as e:
            self.log_lbl.text = f"日志: 获取失败 {e}"

    # ── 登录/投注（占位）──
    def _on_login(self, *a):
        self.log_lbl.text = "日志: 登录功能对接中..."
        self._save_cfg()

    def _on_bet(self, *a):
        if not self.selected:
            self.log_lbl.text = "日志: 请先选号"
            return
        nums = ",".join(map(str, sorted(self.selected)))
        self.log_lbl.text = f"日志: 投注 {nums} 金额={self.amt_in.text}"

    def _do_refresh(self):
        self._on_refresh()


if __name__ == "__main__":
    PK10App().run()
