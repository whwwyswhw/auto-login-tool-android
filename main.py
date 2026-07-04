# -*- coding: utf-8 -*-
"""
PK10 Betting Assistant - Flet v3.0 FULL
Base: v2.0 (proven working) + real PK10 features
Balls: colored circles (NO base64, NO images)
"""
import flet as ft

# Ball colors
BALL_COLORS = {
    "1": "#E6DE00",  "2": "#0092DD",  "3": "#4C4C4C",  "4": "#FF8C00",  "5": "#00CCCC",
    "6": "#8B00C9",  "7": "#BCBCBC",  "8": "#E60000",  "9": "#8B0000",  "10": "#00AA00",
}
TEXT_BLACK = "#000000"
TEXT_WHITE = "#FFFFFF"

def _text_color(bg):
    bg = bg.lstrip("#")
    r, g, b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
    lum = (0.299*r + 0.587*g + 0.114*b) / 255
    return TEXT_BLACK if lum > 0.5 else TEXT_WHITE

def main(page: ft.Page):
    page.title = "PK10"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0D1117"
    page.padding = 8
    page.scroll = ft.ScrollMode.AUTO

    # State
    state = {"selected": {}, "period": "--", "code": "--", "balance": "--", "username": "", "password": "", "amount": "10"}

    def update_selected():
        if state["selected"]:
            nums = sorted(state["selected"].keys(), key=lambda x: int(x))
            sel.value = " ".join(nums)
        else:
            sel.value = "--"
        page.update()

    def on_ball(e):
        n = str(e.control.data)
        if n in state["selected"]:
            del state["selected"][n]
        else:
            state["selected"][n] = state["amount"]
        update_selected()

    def on_login(e):
        log.value = (log.value or "") + f"[登录] 账号={state['username']}\n"
        page.update()

    def on_bet(e):
        if not state["selected"]:
            log.value = (log.value or "") + "[投注] 未选号\n"
        else:
            log.value = (log.value or "") + f"[投注] {list(state['selected'].keys())} 金额={state['amount']}\n"
        page.update()

    def on_refresh(e):
        log.value = (log.value or "") + "[刷新] 获取期号/余额...\n"
        state["period"] = "20260704001"
        state["code"] = "5 2 8 1 9 3 7 4 10 6"
        state["balance"] = "1000.00"
        period.value = state["period"]
        code.value = state["code"]
        balance.value = state["balance"]
        page.update()

    def on_amt_change(e):
        state["amount"] = e.control.value or "10"
        page.update()

    # ---- Header ----
    period = ft.Text("--", size=14, color="#E6EDF3", weight=ft.FontWeight.BOLD)
    code = ft.Text("--", size=12, color="#8B949E")
    balance = ft.Text("--", size=14, color="#00FF00", weight=ft.FontWeight.BOLD)

    header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("期号:", size=12, color="#8B949E"),
                period,
                ft.Container(width=20),
                ft.Text("开奖:", size=12, color="#8B949E"),
            ]),
            ft.Row([code], wrap=True),
            ft.Row([
                ft.Text("余额:", size=12, color="#8B949E"),
                balance,
            ]),
        ]),
        bgcolor="#161B22", padding=10, border_radius=6
    )

    # ---- Balls ----
    sel = ft.Text("--", size=12, color="#E6EDF3")
    amt = ft.TextField(value="10", width=80, text_size=14, on_change=on_amt_change)

    ball_row = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text(str(i), size=14, color=_text_color(BALL_COLORS[str(i)]), weight=ft.FontWeight.BOLD),
                bgcolor=BALL_COLORS[str(i)],
                width=36, height=36, border_radius=18,
                alignment=ft.alignment.center, data=i, on_click=on_ball,
            ) for i in range(1, 11)
        ],
        spacing=4, wrap=True
    )

    balls = ft.Container(
        content=ft.Column([
            ft.Text("选号 (1-10):", size=13, color="#E6EDF3"),
            ball_row,
            ft.Row([
                ft.Text("金额:", size=12, color="#8B949E"),
                amt,
                ft.Container(width=20),
                ft.Text("已选:", size=12, color="#8B949E"),
                sel,
            ]),
        ]),
        bgcolor="#161B22", padding=10, border_radius=6
    )

    # ---- Account ----
    user_in = ft.TextField(width=200, text_size=13, on_change=lambda e: state.update({"username": e.control.value}))
    pwd_in = ft.TextField(width=200, text_size=13, password=True, on_change=lambda e: state.update({"password": e.control.value}))

    account = ft.Container(
        content=ft.Column([
            ft.Text("账号", size=14, weight=ft.FontWeight.BOLD, color="#E6EDF3"),
            ft.Text("用户名:", size=11, color="#8B949E"),
            user_in,
            ft.Text("密码:", size=11, color="#8B949E"),
            pwd_in,
            ft.Row([
                ft.ElevatedButton("登录", on_click=on_login, width=80, height=40),
                ft.ElevatedButton("投注", on_click=on_bet, width=80, height=40),
                ft.ElevatedButton("刷新", on_click=on_refresh, width=80, height=40),
            ], spacing=6),
        ]),
        bgcolor="#161B22", padding=10, border_radius=6
    )

    # ---- Log ----
    log = ft.Text("-- 等待操作 --", size=11, font_family="monospace", color="#8B949E")
    log_box = ft.Container(
        content=ft.Column([
            ft.Text("运行日志:", size=12, color="#E6EDF3"),
            log,
        ]),
        bgcolor="#0D1117", padding=10, border_radius=6
    )

    # ---- Layout ----
    page.add(header, balls, account, log_box)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
