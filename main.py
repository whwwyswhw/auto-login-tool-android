# -*- coding: utf-8 -*-
"""
PK10 Betting Assistant - Flet v3.1 MINIMAL-FULL
Based on v2.0 (proven working) + PK10 features
NO Container, NO bgcolor on page, NO scroll, NO border_radius, NO alignment
Only: Text, Row, ElevatedButton, TextField
"""
import flet as ft

def main(page: ft.Page):
    page.title = "PK10"
    page.theme_mode = ft.ThemeMode.DARK
    
    # State
    selected = set()
    period = ft.Text("期号: --", size=14, color="white")
    code = ft.Text("开奖: --", size=12, color="grey")
    balance = ft.Text("余额: --", size=14, color="green")
    sel = ft.Text("已选: --", size=13, color="yellow")
    amt = ft.TextField(value="10", label="金额", width=100)
    user_in = ft.TextField(label="账号", width=200)
    pwd_in = ft.TextField(label="密码", password=True, width=200)
    log = ft.Text("日志: 等待操作...", size=12, color="white")
    
    def upd_sel():
        sel.value = "已选: " + (",".join(sorted(selected, key=int)) if selected else "--")
        page.update()
    
    def on_ball(n):
        def h(e):
            if n in selected:
                selected.remove(n)
            else:
                selected.add(n)
            upd_sel()
        return h
    
    def on_login(e):
        log.value = f"日志: 登录 {user_in.value}/{pwd_in.value}"
        page.update()
    
    def on_bet(e):
        if not selected:
            log.value = "日志: 请先选号"
        else:
            log.value = f"日志: 投注 {','.join(sorted(selected, key=int))} 金额={amt.value}"
        page.update()
    
    def on_refresh(e):
        period.value = "期号: 20260704001"
        code.value = "开奖: 5 2 8 1 9 3 7 4 10 6"
        balance.value = "余额: 1000.00"
        log.value = "日志: 已刷新"
        page.update()
    
    balls = ft.Row([
        ft.ElevatedButton(str(i), data=i, on_click=on_ball(i)) for i in range(1, 11)
    ])
    
    page.add(
        period, code, balance,
        ft.Divider(),
        ft.Text("选号 (1-10):", size=14, color="white"),
        balls,
        sel,
        amt,
        ft.Divider(),
        user_in, pwd_in,
        ft.Row([
            ft.ElevatedButton("登录", on_click=on_login),
            ft.ElevatedButton("投注", on_click=on_bet),
            ft.ElevatedButton("刷新", on_click=on_refresh),
        ]),
        ft.Divider(),
        log,
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
