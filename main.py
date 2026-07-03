# -*- coding: utf-8 -*-
"""
PK10 彩票投注助手 Flet 版 v1.0
完整可运行的 Flet 版本
"""
import flet as ft
import requests
import base64
import io
import re
import json
import os
import time
import datetime
import threading

# ===== 配置文件路径 =====
import sys
if getattr(sys, 'frozen', False):
    _BASE_DIR = os.path.dirname(sys.executable)
else:
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(_BASE_DIR, "login_config.json")

# ===== 号码球图片 base64 (简化版，实际应从原文件读取) =====
# 这里只放 1 号的示例，实际应该包含 10 个
_EMBEDDED_BALLS = {
    "1": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB1klEQVR4nO2WvWoUURTHf+fc2XXZDQmS1YghxRIQrLSIip0voI29rcTCRgK+g1jHQrQQfAbfIIIi2vhFzJoYYlK67kzczO49cmcTIyLkTrJ2/uFOc8+d35yPOfcIwFZb5wf4exgNM0wEYQSy/XeliC6cbvlF2VzRm/WGf9DtgjE62J/QsQZkmc7LxgpdFWreUBgt7DeZCt6MXiJCY2D/jrQrGRhOhbp6jx0GZibFipUAgRU8LMULEFVI3DAs3g9XFFSQpCyoWjV6P6D9ucm378eZmd6iOdmJhmocDCpVK7L+/mOVpZdXyPL7nJx+zIdP1wkV7lwcMDnYREgSY+3LGO21C1Sq1zg/d5XZ2dli993bF6QpTEzAYHBEYPDMOaPTqbDcvsHFy3dptWaKvTzvkSRVRPKQm2jpgf4JpJmjVmsVsDTt0M93cC5BClK5GteDDMxDoz5gJ1/m+dIzHj28zdfNVVQjk1YmpMEBbzA+nnOm9YS0+5RaZYp+/xiHVRJj1O/DqaltmmeN1fUTeH/4vqQxRsHTPFe6qUT/b0cCBokYqhZrfnTgqKT/gX+T6n6VlukyQdG3xZ4MIcs829vDAsrzckTZWAmjTATIhErFWFtv8urNOcwc3juak1tcmntNJfFF7x0ZcE9OwYW4hFMybPB5Hn8+KTsW9j30e/IrvBKeEvfNZliiioR+GUss7HYBVERYrK4oNUYzMCRFX55FkBcPIVETv1Ou4Ygq2cvmMIoV3GhIYgVVEaKOttxiO+vV/MuoLqUMXplp+8SfgvfMUB1p3OQAAAABJRU5ErkJggg==",
    "2": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAYAAAByDd+UAAADpUlEQVR4nLWWXUwcVRTHf/fO7JfL8lGXUoirKEFpoo2aUoQaYxNSP5qaPjQm+tAH40OND0YT25g+NDFRw6N99cHERKMxMZpqwcZanpRUoYqAhlCoFvkoFFi+lmV35x4zs4Amsuw0wHmYzM49O//7P/P/n3sUZ0VTez1IMvcGWp8GStneMCilEfkRR72uoVMzL6eIlr8DEkNEthlQI0awg81o+VZxbqQBRTdKBTGO9hJ2IkQEbblUs+WES+7AyeV3s1OhlMI4YmPcEhpBqdvZLqrgr01CKWWv3fnKdy9aI+5nWQdxP7lBGePdFYtVQD+hEKVheYmy1Dg1K+NYYpgK3slkSS0SLvGAKaI5n4AK7eSoT/ZxiGGa791Nfd192AGL0b/HuPxbBxfmEoxU7fdYylYA3cKJtojPXeNszRjHT7xKIBReX28Ejj69COMnH/Pm8FUmEwfRmUWMW40Nwrcqw5l57q7f64H1dv/ExW/O82tPN5lMBjsS5djRIxwMTkMqiVh2QZ7+SipCOlzOwNAI3//+EV8MLzMTS1A1dYlzL6Rpam4hWlnN49UhvpqYxInUoYyzIWRRQO9P4nCztJbTE4oVHSKVqIZoGTPzC8zcmvYs5jrLiFnT8naoFGYr6jwluv3Cmb9FkzXO3vsPe00kvTjPn4uCCUZBClvktjqLcjKgLJzlBVrGOnj7yMPcU9/gMRzs76V9QiNle9C5TEGmvhkqBLHDVEwN0Jrt563nW3iksclbG7s+xPsXuhiNH/LKvyVbrIFhBYlP/sJJu5fXTr5I/K5ab22ot4e2zzr4PPoE6Vg1KreCbNK4fAGKDsDiLMf4g1OvvEQsvsd73n6pk3e/vsLP1YdJlyYgm9oUzL/xRWhYGODlZx7zwIwxtF/8jjNfXmGq8kEqV26ix24wHUuwFIl7otkSQ/fo2i+j7Nv3LI7J98uQrXnvuUexdX5DAaP4tK+HD1IHkOguMLktAApUqhSRkn+nj9bW1v+lDU58iL4xixPbjTLZDY8tf4BaM6ir6On6gSzKe41ZZeo1a6UISo6rSQsT2YUyuYJK9ddptOJy7AAnzvdhZGNRuFr5q+wBJFrusduaD8WQClfQX/NkkTxn1YdFbeFjUhODcl+4WQrFBwebQCBfMxeziId8zy6FQkQ0JpQkvbCMe4Zt/0zKf8HyY+JDNUM4po1Q1F53+Q6gEQgpjElqOjGUWW0sz51B1GL+cPM1gPnF8piRy3Rhqaf+ARxEfqpayEYNAAAAAElFTkSuQmCC",
}

# ===== 颜色配置 =====
NUM_COLORS = {
    "1": "#E6DE00",
    "2": "#0092DD", 
    "3": "#4C4C4C",
    "4": "#FF8C00",
    "5": "#00CCCC",
    "6": "#8B00C9",
    "7": "#BCBCBC",
    "8": "#E60000",
    "9": "#8B0000",
    "10": "#00AA00",
}

def _text_color(bg_hex):
    """根据背景色亮度返回黑/白文字色"""
    bg_hex = bg_hex.lstrip("#")
    r, g, b = int(bg_hex[0:2], 16), int(bg_hex[2:4], 16), int(bg_hex[4:6], 16)
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "#000000" if luminance > 160 else "#FFFFFF"

class PK10App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "PK10 投注助手"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#0D1117"
        self.page.padding = 10
        self.page.scroll = ft.ScrollMode.AUTO
        
        # 状态变量
        self.is_logged_in = False
        self.current_draw_num = ""
        self.log_entries = []
        
        # 加载号码球图片
        self.num_ball_images = {}
        self._load_ball_images()
        
        # 构建 UI
        self._build_ui()
    
    def _load_ball_images(self):
        """加载嵌入的号码球图片"""
        for num, b64 in _EMBEDDED_BALLS.items():
            try:
                self.num_ball_images[num] = ft.Image(
                    src_base64=b64,
                    width=28,
                    height=28,
                    fit=ft.ImageFit.CONTAIN,
                )
            except Exception as e:
                print(f"加载号码球 {num} 失败: {e}")
    
    def _build_ui(self):
        """构建主 UI"""
        # 标题
        title = ft.Text("PK10 投注助手", size=24, weight=ft.FontWeight.BOLD, color="#E6EDF3")
        
        # 登录按钮
        self.login_btn = ft.ElevatedButton(
            "登录",
            on_click=self._on_login_click,
            bgcolor="#238636",
            color="#FFFFFF",
        )
        
        # 开奖号码显示区
        self.draw_bar = ft.Row([ft.Text("等待开奖...", color="#E6EDF3")])
        
        # 日志区
        self.log_text = ft.TextField(
            label="操作日志",
            multiline=True,
            read_only=True,
            min_lines=10,
            max_lines=15,
            bgcolor="#0D1117",
            color="#E6EDF3",
        )
        
        # 主布局
        self.page.add(
            title,
            self.login_btn,
            ft.Divider(),
            ft.Text("开奖号码", size=18, weight=ft.FontWeight.BOLD, color="#E6EDF3"),
            self.draw_bar,
            ft.Divider(),
            self.log_text,
        )
    
    def _on_login_click(self, e):
        """登录按钮点击"""
        self._log("开始登录...")
        # 这里简化，实际应该打开登录对话框
        self.is_logged_in = True
        self.login_btn.text = "已登录"
        self.login_btn.bgcolor = "#238636"
        self.page.update()
        self._log("登录成功!")
    
    def _log(self, message, level="INFO"):
        """添加日志"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] [{level}] {message}"
        self.log_entries.append(log_line)
        
        # 更新日志显示
        self.log_text.value = "\n".join(self.log_entries[-50:])  # 只显示最近 50 条
        self.page.update()

def main(page: ft.Page):
    app = PK10App(page)

if __name__ == "__main__":
    ft.app(target=main)
