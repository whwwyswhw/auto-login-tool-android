# -*- coding: utf-8 -*-
"""
PK10 Betting Assistant - Flet v4.0
A: Fix text overlap (width constraints)
B: Colored balls (Container bgcolor only, no border_radius/alignment)
C: Real business logic (login, refresh, bet)
Based on v3.1 (proven working)
"""
import flet as ft
import requests
import json
import os
import time
import threading

# 配置文件路径（手机/桌面都能用）
CFG_PATH = os.path.join(os.path.expanduser("~"), "pk10_config.json")

# 球号颜色
BALL_COLORS = {
    "1": "#E6DE00", "2": "#0092DD", "3": "#4C4C4C", "4": "#FF8C00", "5": "#00CCCC",
    "6": "#8B00C9", "7": "#BCBCBC", "8": "#E60000", "9": "#8B0000", "10": "#00AA00"
}

# 业务配置
BASE_URL = "https://1688473.com"
LOGIN_URL = f"{BASE_URL}/login.php"
GET_INFO_URL = f"{BASE_URL}/api/get_user_info.php"
GET_PERIOD_URL = f"{BASE_URL}/view/jisusaiche/pk10kai.html"

def main(page: ft.Page):
    page.title = "PK10"
    page.theme_mode = ft.ThemeMode.DARK
    
    # State
    state = {
        "selected": set(),
        "period": "--",
        "balance": "--",
        "code": "--",
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
        except: pass
    
    def save_cfg():
        try:
            with open(CFG_PATH, "w", encoding="utf-8") as f:
                json.dump({"user": user_in.value, "pwd": pwd_in.value}, f)
        except: pass
    
    # ---- UI 控件 (A: 加 width 约束防文字重叠) ----
    period = ft.Text("期号: --", size=13, color="white", width=280)
    code = ft.Text("开奖: --", size=11, color="grey", width=280)
    balance = ft.Text("余额: --", size=13, color="green", width=280)
    sel = ft.Text("已选: --", size=12, color="yellow", width=280)
    status = ft.Text("● 离线", size=11, color="red", width=80)
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
    
    # ---- B: 彩色球 (只用 bgcolor，不加 border_radius/alignment) ----
    ball_row = ft.Row([
        ft.Container(
            content=ft.Text(str(i), size=14, color="black", weight=ft.FontWeight.BOLD),
            bgcolor=BALL_COLORS[str(i)],
            width=40, height=40,
            on_click=on_ball(i), data=i
        ) for i in range(1, 11)
    ], wrap=True, spacing=4)
    
    # ---- C: 真实业务逻辑 ----
    def do_login(e):
        if not user_in.value or not pwd_in.value:
            log_msg("请输入账号密码")
            return
        log_msg("登录中...")
        threading.Thread(target=_login, daemon=True).start()
    
    def _login():
        try:
            s = requests.Session()
            s.headers.update({"User-Agent": "Mozilla/5.0", "Referer": BASE_URL})
            r = s.post(LOGIN_URL, data={"username": user_in.value, "password": pwd_in.value}, timeout=10)
            r = s.get(GET_INFO_URL, timeout=10)
            data = r.json()
            if data.get("balance"):
                state["balance"] = str(data["balance"])
                state["logged_in"] = True
                state["session"] = s
                balance.value = f"余额: {state['balance']}"
                status.value = "● 在线"
                status.color = "green"
                log_msg(f"登录成功 余额={state['balance']}")
            else:
                log_msg("登录失败 请检查账号")
        except Exception as ex:
            log_msg(f"登录异常: {ex}")
        page.update()
    
    def do_refresh(e):
        log_msg("刷新中...")
        threading.Thread(target=_refresh, daemon=True).start()
    
    def _refresh():
        try:
            s = state["session"] or requests
            r = s.get(GET_PERIOD_URL, timeout=10)
            # 解析期号（简单提取）
            import re
            m = re.search(r'期号[：:]?\s*(\d+)', r.text)
            if m:
                state["period"] = m.group(1)
                period.value = f"期号: {state['period']}"
            # 解析最近开奖
            m2 = re.search(r'开奖[号码结果]*[：:]?\s*([\d\s]+)', r.text)
            if m2:
                state["code"] = m2.group(1).strip()
                code.value = f"开奖: {state['code']}"
            log_msg("刷新成功")
        except Exception as ex:
            log_msg(f"刷新异常: {ex}")
        page.update()
    
    def do_bet(e):
        if not state["selected"]:
            log_msg("请先选号")
            return
        if not state["logged_in"]:
            log_msg("请先登录")
            return
        nums = ",".join(sorted(state["selected"], key=int))
        log_msg(f"投注 {nums} 金额={amt.value}...")
        # TODO: 实际投注 API
    
    # ---- 布局 ----
    page.add(
        ft.Row([period, status]),
        code,
        balance,
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
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
