import flet as ft

def main(page: ft.Page):
    page.title = "PK10 投注助手"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 780
    page.padding = 10

    page.add(
        ft.Text("PK10 投注助手", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("正在加载完整代码...", size=16, color=ft.Colors.GREY),
        ft.ProgressRing(),
    )

if __name__ == "__main__":
    ft.app(target=main)
