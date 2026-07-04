# -*- coding: utf-8 -*-
"""
PK10 Betting Assistant - Flet v1.9
SIMPLIFIED: No base64 images, use colored containers instead.
Goal: Get a non-black-screen app running on mobile.
"""
import flet as ft

# Ball colors (same as original)
BALL_COLORS = {
    "1": "#E6DE00",  # Yellow
    "2": "#0092DD",  # Blue
    "3": "#4C4C4C",  # Gray
    "4": "#FF8C00",  # Orange
    "5": "#00CCCC",  # Cyan
    "6": "#8B00C9",  # Purple
    "7": "#BCBCBC",  # Light Gray
    "8": "#E60000",  # Red
    "9": "#8B0000",  # Dark Red
    "10": "#00AA00", # Green
}

def _text_color(bg):
    """Return black or white text color depending on background brightness."""
    bg = bg.lstrip("#")
    r, g, b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#000000" if luminance > 0.5 else "#FFFFFF"


def main(page: ft.Page):
    page.title = "PK10 Betting"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0D1117"
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO

    # Store state
    page.selected_nums = {}

    # ---- Callbacks ----
    def toggle_ball(e):
        n = str(e.control.data)
        if n in page.selected_nums:
            del page.selected_nums[n]
        else:
            page.selected_nums[n] = "10"
        update_selected()

    def update_selected():
        if not hasattr(page, "selected_display"):
            return
        if page.selected_nums:
            nums = sorted(page.selected_nums.keys(), key=lambda x: int(x))
            parts = [f"#{n}({page.selected_nums[n]})" for n in nums]
            page.selected_display.value = ", ".join(parts)
        else:
            page.selected_display.value = "--"
        page.update()

    def on_login(e):
        page.log_val.value = (page.log_val.value or "") + "[LOGIN] clicked\n"
        page.update()

    def on_bet(e):
        if not page.selected_nums:
            page.log_val.value = (page.log_val.value or "") + "[BET] No numbers!\n"
        else:
            page.log_val.value = (page.log_val.value or "") + f"[BET] {list(page.selected_nums.keys())}\n"
        page.update()

    # ---- Build ball row (colored containers instead of base64 images) ----
    ball_widgets = []
    for n in range(1, 11):
        key = str(n)
        color = BALL_COLORS[key]
        txt_color = _text_color(color)
        ball = ft.Container(
            content=ft.Text(str(n), size=14, color=txt_color, weight=ft.FontWeight.BOLD),
            bgcolor=color,
            width=36, height=36,
            border_radius=18,
            alignment=ft.alignment.center,
            data=n,
            on_click=toggle_ball,
        )
        ball_widgets.append(ball)

    ball_row = ft.Row(controls=ball_widgets, spacing=4, wrap=True)

    # ---- Status display ----
    page.selected_display = ft.Text("--", size=12, color="#E6EDF3")
    page.log_val = ft.Text("--", size=11, font_family="monospace", color="#8B949E")

    # ---- Bet amount ----
    bet_amount = ft.TextField(value="10", width=80, text_size=14)

    # ---- Main UI ----
    page.controls.clear()
    page.add(
        # Header
        ft.Container(
            content=ft.Column([
                ft.Text("PK10 Betting Assistant", size=16, weight=ft.FontWeight.BOLD, color="#E6EDF3"),
                ft.Row([
                    ft.Text("Period: ", size=12, color="#8B949E"),
                    ft.Text("--", size=13, color="#E6EDF3"),
                    ft.Text("  Code: ", size=12, color="#8B949E"),
                    ft.Text("--", size=13, color="#E6EDF3"),
                ]),
            ]),
            bgcolor="#161B22", padding=10, border_radius=6
        ),
        # Balls
        ft.Container(
            content=ft.Column([
                ft.Text("Select balls (1-10):", size=13, color="#E6EDF3"),
                ball_row,
                ft.Row([
                    ft.Text("Amount:", size=12, color="#8B949E"),
                    bet_amount,
                    ft.Text("  Selected:", size=12, color="#8B949E"),
                    page.selected_display,
                ]),
            ]),
            bgcolor="#161B22", padding=10, border_radius=6
        ),
        # Account
        ft.Container(
            content=ft.Column([
                ft.Text("Account", size=14, weight=ft.FontWeight.BOLD, color="#E6EDF3"),
                ft.Row([
                    ft.Text("Balance:", size=12, color="#8B949E"),
                    ft.Text("--", size=14, color="#E6EDF3"),
                ]),
                ft.Text("Username:", size=11, color="#8B949E"),
                ft.TextField(width=200, text_size=13),
                ft.Text("Password:", size=11, color="#8B949E"),
                ft.TextField(width=200, text_size=13, password=True),
                ft.Row([
                    ft.ElevatedButton("Login", on_click=on_login, width=90),
                    ft.ElevatedButton("Bet", on_click=on_bet, width=90),
                ]),
            ]),
            bgcolor="#161B22", padding=10, border_radius=6
        ),
        # Log
        ft.Container(
            content=ft.Column([
                ft.Text("Log:", size=13, color="#E6EDF3"),
                page.log_val,
            ]),
            bgcolor="#0D1117", padding=10, border_radius=6
        ),
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
