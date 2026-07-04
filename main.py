# -*- coding: utf-8 -*-
"""
PK10 Betting Assistant - Flet v2.0 PLAIN
NO images, NO base64, NO colors - just text and buttons.
Prove the app can start on mobile.
"""
import flet as ft

def main(page: ft.Page):
    page.title = "PK10"
    page.theme_mode = ft.ThemeMode.DARK
    
    page.add(
        ft.Text("PK10 Betting App v2.0", size=20, weight=ft.FontWeight.BOLD),
        ft.Text("If you see this, the app works!", size=16, color="green"),
        ft.Divider(),
        ft.Text("Ball selection (tap numbers):", size=14),
        ft.Row([
            ft.ElevatedButton(str(i), data=i, on_click=lambda e: page.add(ft.Text(f"Selected: {e.control.data}")))
            for i in range(1, 6)
        ]),
        ft.Divider(),
        ft.TextField(label="Username", width=200),
        ft.TextField(label="Password", password=True, width=200),
        ft.ElevatedButton("Login", on_click=lambda e: page.add(ft.Text("Login clicked!"))),
        ft.ElevatedButton("Refresh", on_click=lambda e: page.update()),
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
