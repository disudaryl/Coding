import traceback

import flet as ft

# ---------- FIXED FEE RULES ----------
RATE_PER_UNIT = 487
MISC_FEE = 3700
MIN_DOWN_PAYMENT = 3500
MIN_UNITS, MAX_UNITS = 1, 25

# Share of the remaining balance paid at each exam
EXAMS = [
    ("Prelim", 0.15),
    ("1st Grading", 0.25),
    ("2nd Grading", 0.15),
    ("Midterm", 0.30),
    ("Finals", 0.15),
]


def money(amount):
    return f"{amount:,.2f}"


def build(page: ft.Page):
    page.title = "Tuition Fee Calculator"
    page.padding = 0

    # Follow the phone's light / dark setting automatically
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)

    # Theme colors with transparency, so glass works in light AND dark mode
    glass_fill = ft.Colors.with_opacity(0.45, ft.Colors.SURFACE)
    field_fill = ft.Colors.with_opacity(0.35, ft.Colors.SURFACE)

    # ----- small helpers -----
    def glass(content):
        return ft.Container(
            content=content,
            padding=20,
            border_radius=24,
            bgcolor=glass_fill,
            blur=ft.Blur(20, 20),
        )

    def heading(text):
        return ft.Text(text, size=16, weight=ft.FontWeight.BOLD)

    def field(label, value=""):
        return ft.TextField(
            label=label,
            value=value,
            keyboard_type=ft.KeyboardType.NUMBER,
            filled=True,
            bgcolor=field_fill,
            border=ft.InputBorder.NONE,
            border_radius=14,
        )

    def line(label, amount, bold=False):
        weight = ft.FontWeight.BOLD if bold else ft.FontWeight.NORMAL
        return ft.Row(
            [
                ft.Text(label, weight=weight, expand=True),
                ft.Text(money(amount), weight=weight),
            ]
        )

    # ----- inputs -----
    lab_rate = field("Lab fee per subject", "0")
    hands_rate = field("Hands-on fee per subject", "0")
    units = field(f"Total units enrolled ({MIN_UNITS}-{MAX_UNITS})")
    lab = field("Number of subjects with LAB", "0")
    hands_on = field("Total number of hands-on subjects", "0")
    down = field(f"Down payment (min {MIN_DOWN_PAYMENT})", str(MIN_DOWN_PAYMENT))

    error = ft.Text(color=ft.Colors.ERROR)
    results = ft.Column(spacing=6)
    results_card = glass(results)
    results_card.visible = False

    def fail(message):
        error.value = message
        page.update()

    def calculate(e):
        error.value = ""
        results.controls.clear()
        results_card.visible = False
        try:
            try:
                lab_fee_rate = float(lab_rate.value or 0)
                hands_fee_rate = float(hands_rate.value or 0)
                unit_count = int(units.value)
                lab_count = int(lab.value or 0)
                hands_count = int(hands_on.value or 0)
                down_pay = float(down.value or 0)
            except ValueError:
                return fail("Please enter numbers only.")

            if lab_fee_rate < 0 or hands_fee_rate < 0:
                return fail("Rates cannot be negative.")
            if not MIN_UNITS <= unit_count <= MAX_UNITS:
                return fail(f"Units must be from {MIN_UNITS} to {MAX_UNITS}.")
            if lab_count < 0 or hands_count < 0:
                return fail("Subject counts cannot be negative.")

            # ----- assessment -----
            tuition = RATE_PER_UNIT * unit_count
            lab_fee = lab_fee_rate * lab_count
            hands_fee = hands_fee_rate * hands_count
            total = tuition + MISC_FEE + lab_fee + hands_fee

            if down_pay < MIN_DOWN_PAYMENT:
                return fail(f"Down payment must be at least {MIN_DOWN_PAYMENT}.")
            if down_pay > total:
                return fail("Down payment cannot be more than the total assessment.")

            balance = total - down_pay

            results.controls.extend(
                [
                    heading("Assessment"),
                    line(f"Tuition ({unit_count} x {RATE_PER_UNIT})", tuition),
                    line("Miscellaneous fee", MISC_FEE),
                    line(f"Laboratory fee ({lab_count} x {money(lab_fee_rate)})", lab_fee),
                    line(f"Hands-on fee ({hands_count} x {money(hands_fee_rate)})", hands_fee),
                    ft.Divider(),
                    line("TOTAL ASSESSMENT", total, bold=True),
                    ft.Divider(),
                    heading("Payment breakdown"),
                    line("Down payment", down_pay),
                    line("Remaining balance", balance, bold=True),
                ]
            )
            for name, share in EXAMS:
                results.controls.append(line(f"{name} ({share:.0%})", balance * share))

            results_card.visible = True
            page.update()
        except Exception as ex:
            fail(f"Something went wrong: {ex}")

    # ----- background: soft gradient + two blurred-looking color blobs -----
    background = ft.Container(
        left=0,
        top=0,
        right=0,
        bottom=0,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[
                ft.Colors.PRIMARY_CONTAINER,
                ft.Colors.SECONDARY_CONTAINER,
                ft.Colors.TERTIARY_CONTAINER,
            ],
        ),
    )
    blob_one = ft.Container(
        width=240,
        height=240,
        border_radius=120,
        bgcolor=ft.Colors.with_opacity(0.55, ft.Colors.PRIMARY),
        left=-70,
        top=80,
    )
    blob_two = ft.Container(
        width=280,
        height=280,
        border_radius=140,
        bgcolor=ft.Colors.with_opacity(0.45, ft.Colors.TERTIARY),
        right=-90,
        bottom=140,
    )

    # ----- content layer (scrolls over the background) -----
    content = ft.Container(
        left=0,
        top=0,
        right=0,
        bottom=0,
        padding=20,
        content=ft.SafeArea(
            content=ft.Column(
                [
                    ft.Text("Tuition Fee Calculator", size=26, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Enter the details below",
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    glass(
                        ft.Column(
                            [heading("Fee rates"), lab_rate, hands_rate],
                            spacing=12,
                        )
                    ),
                    glass(
                        ft.Column(
                            [
                                heading("Student details"),
                                units,
                                lab,
                                hands_on,
                                down,
                                ft.Row(
                                    [
                                        ft.FilledButton(
                                            "Compute",
                                            on_click=calculate,
                                            expand=True,
                                            height=48,
                                        )
                                    ]
                                ),
                                error,
                            ],
                            spacing=12,
                        )
                    ),
                    results_card,
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=16,
            )
        ),
    )

    page.add(ft.Stack([background, blob_one, blob_two, content], expand=True))


def main(page: ft.Page):
    # If anything goes wrong while building the screen, show the error as
    # text instead of leaving a blank page.
    try:
        build(page)
    except Exception:
        page.add(ft.Text(traceback.format_exc(), selectable=True))
        page.update()


ft.run(main)
