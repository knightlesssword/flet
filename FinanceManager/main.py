import flet
from flet import (
    Page,
    Text,
    TextField,
    Dropdown,
    ElevatedButton,
    Column,
    Row,
    DataTable,
    DataColumn,
    DataRow,
    DataCell,
    AlertDialog,
    Image
)
import matplotlib
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import io
import base64

from flet_core import dropdown, TextThemeStyle, MainAxisAlignment, icons, TextButton, colors, FontWeight, \
    Container, border, Alignment, TextAlign, BorderSide, Icon, IconButton, ThemeMode

# In-memory storage for transactions
transactions = []

# Function to add a transaction
def add_transaction(type, description, amount, date):
    transactions.append({
        "type": type,
        "description": description,
        "amount": float(amount),
        "date": date
    })


# Function to filter transactions by month and year
def filter_transactions(month, year):
    filtered = []
    for txn in transactions:
        txn_date = datetime.datetime.strptime(txn["date"], "%Y-%m-%d")
        if txn_date.month == month and txn_date.year == year:
            filtered.append(txn)
    return filtered


# Function to generate a pie chart
def generate_pie_chart(filtered_txns):
    if not filtered_txns:
        return None

    categories = {}
    for txn in filtered_txns:
        if txn["type"] == "Income":
            category = "Income"
        else:
            category = txn["description"]
        categories[category] = categories.get(category, 0) + txn["amount"]

    labels = categories.keys()
    sizes = categories.values()

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64

# Main Flet application
def main(page: Page):
    page.title = "Personal Finance Manager"
    page.theme_mode = ThemeMode.DARK
    page.window.width = 850
    page.window.height = 700
    page.padding = 20

    # Input fields
    type_dropdown = Dropdown(
        label="Type",
        options=[
            dropdown.Option("Income"),
            dropdown.Option("Expense"),
        ],
        width=200,
        value="Expense"
    )

    description_field = TextField(label="Description", width=200)
    amount_field = TextField(label="Amount", width=200, value="")
    date_field = TextField(label="Date (YYYY-MM-DD)", width=200, value=datetime.date.today().isoformat())
    add_btn = ElevatedButton("Add Transaction", icon=icons.ADD_ROUNDED)

    # Table to display transactions
    txn_table = DataTable(
        columns=[
            DataColumn(Text("Type")),
            DataColumn(Text("Description")),
            DataColumn(Text("Amount")),
            DataColumn(Text("Date")),
            DataColumn(Text("Delete"))
        ],
        rows=[]
    )

    # Report section
    report_month_field = TextField(label="Month (1-12)", width=100, value=str(datetime.date.today().month))
    report_year_field = TextField(label="Year", width=100, value=str(datetime.date.today().year))
    generate_report_btn = ElevatedButton("Generate Report", width=200)
    report_output = Column()

    # Function to delete a transaction
    def delete_transaction(index):
        transactions.pop(index)
        refresh_table()
        page.update()

    # Function to refresh the transaction table
    def refresh_table():
        txn_table.rows = [
            DataRow(cells=[
                DataCell(Text(txn["type"])),
                DataCell(Text(txn["description"])),
                DataCell(Text(f"${txn['amount']:.2f}")),
                DataCell(Text(txn["date"])),
                DataCell(IconButton(  # Add a delete button
                    icon=icons.CLOSE,
                    icon_color=colors.RED,
                    on_click=lambda e, i=index: delete_transaction(i)
                ))
            ]) for index, txn in enumerate(transactions)
        ]
        page.update()

    # Event handler for adding a transaction
    def on_add_click(e):
        type = type_dropdown.value
        description = description_field.value.strip()
        amount = amount_field.value.strip()
        date = date_field.value.strip()

        # Basic validation
        if not description or not amount or not date:
            dialog = AlertDialog(
                title=Text("Error"),
                content=Text("Please fill in all fields."),
                actions=[ElevatedButton("OK", on_click=lambda e: page.close(dialog))]
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            return

        try:
            # Validate amount
            float(amount)
            # Validate date
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            dialog = AlertDialog(
                title=Text("Error"),
                content=Text("Invalid amount or date format."),
                actions=[ElevatedButton("OK", on_click=lambda e: page.close(dialog))]
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            return

        add_transaction(type, description, amount, date)
        refresh_table()

        # Clear input fields
        description_field.value = ""
        amount_field.value = ""
        date_field.value = datetime.date.today().isoformat()
        page.update()

    add_btn.on_click = on_add_click

    # Event handler for generating report
    def on_generate_report(e):

        try:
            month = int(report_month_field.value)
            year = int(report_year_field.value)
            if not (1 <= month <= 12):
                raise ValueError
        except ValueError:
            dialog = AlertDialog(
                title=Text("Error"),
                content=Text("Please enter a valid month (1-12) and year."),
                actions=[ElevatedButton("OK", on_click=lambda e: page.close(dialog))]
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            return

        filtered_txns = filter_transactions(month, year)
        total_income = sum(txn["amount"] for txn in filtered_txns if txn["type"] == "Income")
        total_expenses = sum(txn["amount"] for txn in filtered_txns if txn["type"] == "Expense")
        balance = total_income - total_expenses

        chart_image = generate_pie_chart(filtered_txns)  # Added handling for no transactions

        report_controls = [
            Text(f"Report for {month}/{year}", style=TextThemeStyle.HEADLINE_MEDIUM),
            Text(f"Total Income: ${total_income:.2f}"),
            Text(f"Total Expenses: ${total_expenses:.2f}"),
            Text(f"Balance: ${balance:.2f}"),
        ]

        if chart_image:  # Added condition to check if chart_image exists
            report_controls.extend([
                Text("Expense Breakdown:"),
                Image(src_base64=chart_image, width=300, height=300),  # Changed to src_base64
            ])
        else:
            report_controls.append(Text("No transactions to display in the pie chart."))

        report_output.controls = report_controls
        page.update()

    generate_report_btn.on_click = on_generate_report

    def save_pdf_report(e):
        # Add report details to the PDF
        report_month = report_month_field.value
        report_year = report_year_field.value

        pdf_name = f"{report_month}-{report_year}.pdf"
        c = canvas.Canvas(pdf_name, pagesize=pagesizes.A4)
        width, height = pagesizes.A4

        filtered_txns = filter_transactions(int(report_month), int(report_year))
        total_income = sum(txn["amount"] for txn in filtered_txns if txn["type"] == "Income")
        total_expenses = sum(txn["amount"] for txn in filtered_txns if txn["type"] == "Expense")
        balance = total_income - total_expenses

        # Adding text to the PDF
        c.drawString(150, height - 90, f"Report for {report_month}/{report_year}")
        c.drawString(100, height - 120, f"Total Income: ${total_income:.2f}")
        c.drawString(100, height - 140, f"Total Expenses: ${total_expenses:.2f}")
        c.drawString(100, height - 160, f"Balance: ${balance:.2f}")

        # Generate the chart if there are transactions
        chart_image = generate_pie_chart(filtered_txns)
        if chart_image:
            # Decode the base64 image and save it as a temporary file
            chart_img_path = "chart_image.png"
            with open(chart_img_path, "wb") as img_file:
                img_file.write(base64.b64decode(chart_image))

            # Add the image to the PDF
            c.drawImage(chart_img_path, 100, height - 500, width=300, height=300)

        # Save the PDF
        c.showPage()
        c.save()

        # Notify user about the saved report
        dialog = AlertDialog(
            title=Text("Report Saved"),
            content=Text(f"Report saved as {pdf_name}"),
            actions=[TextButton("OK", on_click=lambda e: page.close(dialog))]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def view_report_output(e):
        dialog = AlertDialog(
            modal=True,
            title=Text("Report View"),
            content=report_output,
            actions=[
                TextButton("OK", on_click=lambda e: page.close(dialog), icon=icons.DONE),
                TextButton("Save", on_click=lambda e: save_pdf_report(e), icon=icons.SAVE)
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def toggle_night_mode(e):
        if page.theme_mode == ThemeMode.LIGHT:
            page.theme_mode = ThemeMode.DARK
            page.bg_color = colors.BLACK
            e.control.icon = icons.BRIGHTNESS_5
        else:
            page.theme_mode = ThemeMode.LIGHT
            page.bg_color = colors.LIGHT_BLUE
            e.control.icon = icons.BRIGHTNESS_3
        page.update()

    # Assemble the UI
    page.add(
        Container(
            content=Text(
                "Personal Finance Manager",
                style=TextThemeStyle.HEADLINE_LARGE,
                color=colors.ORANGE,
                weight=FontWeight.BOLD,
            ),
            alignment=Alignment(0,0),
            border=border.only(None, None, None, BorderSide(1)),
            padding=20,
        ),

    Container(
            Row(
                [
                    Container(
                        Column([
                            Container(
                                Column(
                                    [
                                        Container(Text("Add Income/Expense", style=TextThemeStyle.HEADLINE_SMALL),
                                                  alignment=Alignment(0, 0)),
                                        type_dropdown,
                                        description_field,
                                        amount_field,
                                        date_field,
                                        add_btn,
                                    ],
                                    alignment=MainAxisAlignment.CENTER
                                ),
                                alignment=Alignment(0, 0),
                            ),
                            Row(),
                            Container(
                                Column(
                                    [
                                        Text("Generate Report", style=TextThemeStyle.HEADLINE_SMALL, text_align=TextAlign.CENTER),
                                        Row(), Row(),
                                        Row([
                                                report_month_field,
                                                report_year_field,
                                        ],
                                        alignment=MainAxisAlignment.CENTER),
                                        ElevatedButton(
                                            text="View Report",
                                            icon=icons.LENS_ROUNDED,
                                            icon_color=colors.RED,
                                            on_click=lambda e: [on_generate_report(e), view_report_output(e)],
                                        )
                                    ],
                                    alignment=MainAxisAlignment.CENTER
                                ),
                                expand=True,
                                border=border.only(None, BorderSide(1), None, None),
                            )
                        ]),
                    ),
                    Container(border=border.only(BorderSide(0),BorderSide(0),BorderSide(1),BorderSide(0),)),
                    Container(Column([
                                Container(Text("Transactions", style=TextThemeStyle.HEADLINE_MEDIUM), alignment=Alignment(0,0)),
                                Container(txn_table, alignment=Alignment(0,-1))
                            ]),
                        expand=True,
                    ),
                ]
            ),
            expand=True,
        ),
        Container(
            Row(
                [
                    Container(expand=True),
                    Row(
                    [
                                Text("Made with"),
                                Icon(name=icons.FAVORITE, color=colors.RED, size=13),
                                Text("in Flet by Abu Bakr."),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    Row(expand=True),
                    IconButton(
                                icon=icons.LIGHT_MODE,
                                on_click=lambda e: toggle_night_mode(e),
                                icon_color=colors.YELLOW,
                    ),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN
            ),
        )
    )

if __name__ == '__main__':
    flet.app(target=main)
