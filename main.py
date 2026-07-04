# -*- coding: utf-8 -*-
"""
PK10 Betting Assistant - Flet v1.9 MINIMAL TEST
Only a text widget - prove the app can start on mobile.
"""
import flet as ft

def main(page: ft.Page):
    page.title = "PK10 Test"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0D1117"
    page.add(
        ft.Text("PK10 App v1.9 - TEST", size=20, color="#E6EDF3", weight=ft.FontWeight.BOLD),
        ft.Text("If you see this, the app started OK!", size=14, color="#00FF00"),
        ft.ElevatedButton("Click me", on_click=lambda e: page.add(ft.Text("Clicked!", color="#FF6600"))),
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
