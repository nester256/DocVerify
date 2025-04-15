from fpdf import FPDF


# Mock
def generate_pdf_from_data(data: dict, output_path: str) -> None:  # type: ignore
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.output(output_path)
