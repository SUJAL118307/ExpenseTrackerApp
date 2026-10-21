
import flet as ft
import database
from decimal import Decimal, InvalidOperation


def main(page: ft.Page):
    database.initialize_database()

    page.title = "Expense Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0B0E14"
    page.padding = 24
    page.scroll = ft.ScrollMode.AUTO

    balance = ft.Text(size=32, weight=ft.FontWeight.BOLD)
    income_text = ft.Text(size=22)
    expense_text = ft.Text(size=22)
    transaction_list = ft.Column(spacing=4)
    status_text = ft.Text()

    title_field = ft.TextField(label="Transaction name")
    amount_field = ft.TextField(
        label="Amount (₹)",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    type_dropdown = ft.Dropdown(
        label="Type",
        value="Expense",
        options=[
            ft.dropdown.Option("Expense"),
            ft.dropdown.Option("Income"),
        ],
    )

    category_dropdown = ft.Dropdown(
        label="Category",
        value="Food",
        options=[
            ft.dropdown.Option(c)
            for c in [
                "Food", "Travel", "Education",
                "Shopping", "Bills", "Other"
            ]
        ],
    )

    def money(paise):
        return f"₹{paise / 100:,.2f}"

    def update_dashboard():
        items = database.get_transactions()

        total_income = sum(
            item["amount_paise"] for item in items
            if item["transaction_type"] == "Income"
        )
        total_expenses = sum(
            item["amount_paise"] for item in items
            if item["transaction_type"] == "Expense"
        )

        balance.value = money(total_income - total_expenses)
        income_text.value = money(total_income)
        expense_text.value = money(total_expenses)

        transaction_list.controls.clear()

        if not items:
            transaction_list.controls.append(
                ft.Text("No transactions yet.")
            )

        for item in items:
            is_income = item["transaction_type"] == "Income"

            def delete_handler(e, transaction_id=item["id"]):
                database.delete_transaction(transaction_id)
                status_text.value = "Transaction deleted."
                update_dashboard()

            transaction_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.TRENDING_UP
                        if is_income else ft.Icons.TRENDING_DOWN
                    ),
                    title=ft.Text(item["title"]),
                    subtitle=ft.Text(
                        f'{item["transaction_type"]} • '
                        f'{item["category"]} • {item["created_at"]}'
                    ),
                    trailing=ft.Row(
                        controls=[
                            ft.Text(
                                ("+" if is_income else "-")
                                + money(item["amount_paise"])
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                tooltip="Delete transaction",
                                on_click=delete_handler,
                            ),
                        ],
                        tight=True,
                    ),
                )
            )

        page.update()

    def add_transaction(e):
        name = (title_field.value or "").strip()
        raw_amount = (amount_field.value or "").strip()

        if not name:
            status_text.value = "Enter a transaction name."
            page.update()
            return

        try:
            amount = Decimal(raw_amount)
            if not amount.is_finite() or amount <= 0:
                raise InvalidOperation

            paise = amount * 100

            if paise != paise.to_integral_value():
                status_text.value = "Use at most 2 decimal places."
                page.update()
                return

            amount_paise = int(paise)

        except (InvalidOperation, ValueError):
            status_text.value = "Enter a valid positive amount."
            page.update()
            return

        database.add_transaction(
            name,
            amount_paise,
            type_dropdown.value,
            category_dropdown.value,
        )

        title_field.value = ""
        amount_field.value = ""
        status_text.value = "Transaction saved successfully."
        update_dashboard()

    page.add(
        ft.Row([
            ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=32),
            ft.Text(
                "EXPENSE TRACKER",
                size=24,
                weight=ft.FontWeight.BOLD,
            ),
        ]),
        ft.Text("Your personal finance dashboard"),
        ft.Container(
            content=ft.Column([
                ft.Text("AVAILABLE BALANCE"),
                balance,
            ]),
            bgcolor="#192536",
            padding=24,
            border_radius=16,
        ),
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("INCOME", color="#75E0B2"),
                    income_text,
                ]),
                bgcolor="#17271F",
                padding=16,
                border_radius=12,
                expand=True,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("EXPENSES", color="#FF8D9A"),
                    expense_text,
                ]),
                bgcolor="#2A1B22",
                padding=16,
                border_radius=12,
                expand=True,
            ),
        ]),
        ft.Divider(),
        ft.Text("ADD TRANSACTION", size=18, weight=ft.FontWeight.BOLD),
        title_field,
        amount_field,
        type_dropdown,
        category_dropdown,
        status_text,
        ft.Button(
            "Save Transaction",
            icon=ft.Icons.ADD,
            on_click=add_transaction,
        ),
        ft.Divider(),
        ft.Text("TRANSACTION HISTORY", size=18, weight=ft.FontWeight.BOLD),
        transaction_list,
    )

    update_dashboard()


ft.run(main)
