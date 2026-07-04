# -*- coding: utf-8 -*-
"""
PK10 Betting Assistant - Flet v4.3
- 用 padding 手动居中文字（不用 Container.alignment 或 Column.alignment）
- 32x32 色块 + 手动 padding 居中
"""
import flet as ft
import requests
import json
import os
import threading

CFG_PATH = os.path.join(os.path.expanduser("~"), "pk10_config.json")
BALL_COLORS = {
    "1": "#E6DE00", "2": "#0092DD", "3": "#4C4C4C", "4": "#FF8C00", "5": "#00CCCC",
    "6": "#8B00C9", "7": "#BCBCBC", "8": "#E60000", "9": "#8B0000", "10": "#00AA00"
}
GAMES = {
    "极速赛车": {"lotCode": "10001"},
    "幸运飞艇": {"lotCode": "10002"},
}
DRAW_API = "https://api.api68.com/pks/getLotteryPksInfo.do"

def main(page: ft.Page):
    page.title = "PK10"
    page.theme_mode = ft.ThemeMode.DARK
    
    state = {"selected": set(), "current_game": "极速赛车", "draw_data": None}
    
    game_dd = ft.Dropdown(label="游戏", width=120,
        options=[ft.dropdown.Option(k) for k in GAMES.keys()],
        value="极速赛车",
        on_change=lambda e: setattr(state, 'current_game', e.data))
    period = ft.Text("期号: --", size=12, color="white")
    code = ft.Text("开奖: --", size=11, color="grey")
    next_issue = ft.Text("下期: --", size=11, color="cyan")
    status = ft.Text("● 离线", size=11, color="red")
    sel = ft.Text("已选: --", size=12, color="yellow")
    amt = ft.TextField(value="10", label="金额", width=100, text_size=13)
    user_in = ft.TextField(label="账号", width=280, text_size=13)
    pwd_in = ft.TextField(label="密码", password=True, can_reveal_password=True, width=280, text_size=13)
    log = ft.Text("日志: 等待操作...", size=11, color="white")
    
    # Load config
    if os.path.exists(CFG_PATH):
        try:
            with open(CFG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                user_in.value = cfg.get("user", "")
                pwd_in.value = cfg.get("pwd", "")
                game_dd.value = cfg.get("game", "极速赛车")
                state["current_game"] = game_dd.value
        except: pass
    
    def save_cfg():
        try:
            with open(CFG_PATH, "w", encoding="utf-8") as f:
                json.dump({"user": user_in.value, "pwd": pwd_in.value, "game": game_dd.value}, f)
        except: pass
    
    user_in.on_change = lambda _: save_cfg()
    pwd_in.on_change = lambda _: save_cfg()
    
    def log_msg(msg):
        log.value = f"日志: {msg}"
        page.update()
    
    def upd_sel():
        sel.value = "已选: " + (",".join(sorted(state["selected"], key=int)) if state["selected"] else "--")
        page.update()
    
    def on_ball(n):
        def h(e):
            if n in state["selected"]:
                state["selected"].remove(n)
            else:
                state["selected"].add(n)
            upd_sel()
        return h
    
    # v4.3: 用 Container + padding 手动居中（不用 alignment）
    # 32x32 的 Container，文字大小 12，手动算 padding
    # 数字 1-9: ~8px 宽，数字 10: ~14px 宽，文字高 ~14px
    # 水平居中: padding_left = (32 - text_width) / 2 ≈ 12 for 1-digit, 9 for 2-digit
    # 垂直居中: padding_top = (32 - text_height) / 2 ≈ 9
    # 用 approximate padding，接受微小偏差
    def make_ball(i):
        txt = str(i)
        # 1-digit: padding_left=12, 2-digit: padding_left=9
        pad_left = 9 if len(txt) == 2 else 12
        return ft.Container(
            content=ft.Text(txt, size=12, color="black", weight=ft.FontWeight.BOLD),
            bgcolor=BALL_COLORS[str(i)],
            width=32, height=32,
            padding=ft.padding.only(top=9, left=pad_left, right=4, bottom=4),
            on_click=on_ball(i), data=i
        )
    
    ball_row = ft.Row([make_ball(i) for i in range(1, 11)], wrap=True, spacing=4)
    
    def do_refresh(e=None):
        log_msg("获取开奖中...")
        threading.Thread(target=_fetch_draw, daemon=True).start()
    
    def _fetch_draw():
        try:
            r = requests.get(DRAW_API, params={"lotCode": GAMES[state["current_game"]]["lotCode"]},
                            timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code != 200:
                log_msg(f"HTTP {r.status_code}")
                return
            data = r.json()
            d = data.get("result", {}).get("data", {})
            if not d:
                log_msg("暂无开奖数据")
                return
            state["draw_data"] = d
            period.value = f"期号: {d.get('preDrawIssue', '--')}"
            code.value = f"开奖: {d.get('preDrawCode', '--')}"
            next_issue.value = f"下期: {d.get('drawIssue', '--')}"
            log_msg(f"开奖更新成功")
            page.update()
        except Exception as ex:
            log_msg(f"获取失败: {ex}")
    
    def do_login(e):
        log_msg("登录功能待实现")
    
    def do_bet(e):
        if not state["selected"]:
            log_msg("请先选号")
            return
        log_msg(f"投注 {','.join(sorted(state['selected'], key=int))} 金额={amt.value}")
    
    page.add(
        ft.Row([game_dd, period, status]),
        code,
        next_issue,
        ft.Divider(),
        ft.Text("选号 (1-10):", size=13, color="white"),
        ball_row,
        sel,
        amt,
        ft.Divider(),
        user_in,
        pwd_in,
        ft.Row([
            ft.ElevatedButton("登录", on_click=do_login, width=80),
            ft.ElevatedButton("投注", on_click=do_bet, width=80),
            ft.ElevatedButton("刷新", on_click=do_refresh, width=80),
        ], spacing=6),
        ft.Divider(),
        log,
    )
    
    do_refresh(None)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
