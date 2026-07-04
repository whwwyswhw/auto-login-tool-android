# -*- coding: utf-8 -*-
"""
PK10 Betting Assistant - Flet v4.1
- 开奖/游戏选择工作（真实 API）
- 颜色框缩小 40x40 -> 32x32
- 文字居中（测试 alignment 兼容性）
"""
import flet as ft
import requests
import json
import os
import time
import threading

# 配置文件路径
CFG_PATH = os.path.join(os.path.expanduser("~"), "pk10_config.json")

# 球号颜色（标准 PK10）
BALL_COLORS = {
    "1": "#E6DE00", "2": "#0092DD", "3": "#4C4C4C", "4": "#FF8C00", "5": "#00CCCC",
    "6": "#8B00C9", "7": "#BCBCBC", "8": "#E60000", "9": "#8B0000", "10": "#00AA00"
}

# 游戏配置
GAMES = {
    "极速赛车": {"lotCode": "10001", "lottery_url_code": "jisusaiche"},
    "幸运飞艇": {"lotCode": "10002", "lottery_url_code": "xingyunfeiting"},
}

# 开奖 API
DRAW_API = "https://api.api68.com/pks/getLotteryPksInfo.do"

def main(page: ft.Page):
    page.title = "PK10"
    page.theme_mode = ft.ThemeMode.DARK
    
    # State
    state = {
        "selected": set(),
        "current_game": "极速赛车",
        "draw_data": None,
        "logged_in": False,
        "session": None
    }
    
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
                json.dump({
                    "user": user_in.value,
                    "pwd": pwd_in.value,
                    "game": game_dd.value
                }, f)
        except: pass
    
    # ---- UI 控件 ----
    game_dd = ft.Dropdown(
        label="游戏",
        width=120,
        options=[ft.dropdown.Option(k) for k in GAMES.keys()],
        value="极速赛车",
        on_change=lambda e: [save_cfg(), setattr(state, 'current_game', e.data)]
    )
    period = ft.Text("期号: --", size=12, color="white", width=200)
    code = ft.Text("开奖: --", size=11, color="grey", width=320)
    next_issue = ft.Text("下期: --", size=11, color="cyan", width=200)
    status = ft.Text("● 离线", size=11, color="red", width=80)
    sel = ft.Text("已选: --", size=12, color="yellow", width=280)
    amt = ft.TextField(value="10", label="金额", width=100, text_size=13)
    user_in = ft.TextField(label="账号", width=280, text_size=13, on_change=lambda _: save_cfg())
    pwd_in = ft.TextField(label="密码", password=True, can_reveal_password=True, width=280, text_size=13, on_change=lambda _: save_cfg())
    log = ft.Text("日志: 等待操作...", size=11, color="white", width=320)
    
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
    
    # ---- 彩色球：32x32，文字居中（测试 alignment）----
    ball_row = ft.Row([
        ft.Container(
            content=ft.Text(str(i), size=12, color="black", weight=ft.FontWeight.BOLD),
            bgcolor=BALL_COLORS[str(i)],
            width=32, height=32,
            alignment=ft.alignment.center,  # 文字居中
            on_click=on_ball(i), data=i
        ) for i in range(1, 11)
    ], wrap=True, spacing=4)
    
    # ---- 开奖获取（真实 API）----
    def do_refresh(e=None):
        log_msg("获取开奖中...")
        threading.Thread(target=_fetch_draw, daemon=True).start()
    
    def _fetch_draw():
        try:
            lot_code = GAMES[state["current_game"]]["lotCode"]
            r = requests.get(
                DRAW_API,
                params={"lotCode": lot_code},
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0", "Referer": "https://kj.1689683.com/"}
            )
            if r.status_code != 200:
                log_msg(f"HTTP {r.status_code}")
                return
            
            data = r.json()
            draw_data = data.get("result", {}).get("data", {})
            if not draw_data:
                log_msg("暂无开奖数据")
                return
            
            state["draw_data"] = draw_data
            issue = draw_data.get("preDrawIssue", "--")
            codes = draw_data.get("preDrawCode", "")
            next_iss = draw_data.get("drawIssue", "--")
            draw_time = draw_data.get("drawTime", "")[11:16] if draw_data.get("drawTime") else ""
            
            period.value = f"期号: {issue}"
            code.value = f"开奖: {codes}" if codes else "开奖: --"
            next_issue.value = f"下期: {next_iss} ({draw_time})" if draw_time else f"下期: {next_iss}"
            log_msg(f"开奖更新 {issue}")
            page.update()
            
        except Exception as ex:
            log_msg(f"获取失败: {ex}")
    
    # ---- 登录（占位）----
    def do_login(e):
        log_msg("登录功能待实现")
    
    def do_bet(e):
        if not state["selected"]:
            log_msg("请先选号")
            return
        log_msg(f"投注 {','.join(sorted(state['selected'], key=int))} 金额={amt.value}")
    
    # ---- 布局 ----
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
    
    # 启动时自动获取一次开奖
    do_refresh(None)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
