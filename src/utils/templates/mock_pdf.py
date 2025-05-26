# type: ignore
import io
import logging
import os

import fitz
import img2pdf
from fpdf import FPDF
from fpdf.fonts import FontFace
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


logger = logging.getLogger("docs.generate")


def generate_pdf_version_0(data: dict, path: str) -> None:  # type: ignore
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    pdf.output(path)


def generate_pdf_version_1(data: dict, path: str) -> None:  # type: ignore
    logger.debug("⚙️ generate_pdf_version_1: старт")
    logger.debug(f"➡️ path: {path}")
    logger.debug(f"➡️ h: {data.get('h')}")
    try:
        TABLE_DATA_0 = (
            (data["p_0_1__1"], data["p_0_1__2"]),
            (data["p_0_2__1"], data["p_0_2__2"]),
            (data["p_0_3__1"], data["p_0_3__2"]),
            (data["p_0_4__1"], data["p_0_4__2"]),
            (data["p_0_5__1"], data["p_0_5__2"]),
            (data["p_0_6__1"], data["p_0_6__2"]),
            (data["p_0_7__1"], data["p_0_7__2"]),
        )

        TABLE_DATA_1 = (
            (data["p_1_1__1"], data["p_1_1__2"], data["p_1_1__3"], data["p_1_1__4"]),
            (data["p_1_2__1"], data["p_1_2__2"], data["p_1_2__3"], data["p_1_2__4"]),
            (data["p_1_3__1"], data["p_1_3__2"], data["p_1_3__3"], data["p_1_3__4"]),
            (data["p_1_4__1"], data["p_1_4__2"], data["p_1_4__3"], data["p_1_4__4"]),
            (data["p_1_5__1"], data["p_1_5__2"], data["p_1_5__3"], data["p_1_5__4"]),
            (data["p_1_6__1"], data["p_1_6__2"], data["p_1_6__3"], data["p_1_6__4"]),
            (data["p_1_7__1"], data["p_1_7__2"], data["p_1_7__3"], data["p_1_7__4"]),
            (data["p_1_8__1"], data["p_1_8__2"], data["p_1_8__3"], data["p_1_8__4"]),
            (data["p_1_9__1"], data["p_1_9__2"], data["p_1_9__3"], data["p_1_9__4"]),
        )

        TABLE_DATA_2 = (
            (data["p_2_1__1"], data["p_2_1__2"], data["p_2_1__3"], data["p_2_1__4"]),
            (data["p_2_2__1"], data["p_2_2__2"], data["p_2_2__3"], data["p_2_2__4"]),
            (data["p_2_3__1"], data["p_2_3__2"], data["p_2_3__3"], data["p_2_3__4"]),
        )

        TABLE_DATA_3 = (
            (data["p_3_1__1"], data["p_3_1__2"], data["p_3_1__3"], data["p_3_1__4"]),
            (data["p_3_2__1"], data["p_3_2__2"], data["p_3_2__3"], data["p_3_2__4"]),
            (data["p_3_3__1"], data["p_3_3__2"], data["p_3_3__3"], data["p_3_3__4"]),
        )

        TABLE_DATA_4 = (
            (data["p_4_1__1"], data["p_4_1__2"], data["p_4_1__3"], data["p_4_1__4"]),
            (data["p_4_2__1"], data["p_4_2__2"], data["p_4_2__3"], data["p_4_2__4"]),
            (data["p_4_3__1"], data["p_4_3__2"], data["p_4_3__3"], data["p_4_3__4"]),
            (data["p_4_4__1"], data["p_4_4__2"], data["p_4_4__3"], data["p_4_4__4"]),
            (data["p_4_5__1"], data["p_4_5__2"], data["p_4_5__3"], data["p_4_5__4"]),
        )

        TABLE_DATA_5 = (
            (data["p_5_1__1"], data["p_5_1__2"], data["p_5_1__3"], data["p_5_1__4"]),
            (data["p_5_2__1"], data["p_5_2__2"], data["p_5_2__3"], data["p_5_2__4"]),
            (data["p_5_3__1"], data["p_5_3__2"], data["p_5_3__3"], data["p_5_3__4"]),
            (data["p_5_4__1"], data["p_5_4__2"], data["p_5_4__3"], data["p_5_4__4"]),
            (data["p_5_5__1"], data["p_5_5__2"], data["p_5_5__3"], data["p_5_5__4"]),
        )

        TABLE_DATA_6 = (
            (data["p_6_1__1"], data["p_6_1__2"], data["p_6_1__3"], data["p_6_1__4"]),
            (data["p_6_2__1"], data["p_6_2__2"], data["p_6_2__3"], data["p_6_2__4"]),
            (data["p_6_3__1"], data["p_6_3__2"], data["p_6_3__3"], data["p_6_3__4"]),
            (data["p_6_4__1"], data["p_6_4__2"], data["p_6_4__3"], data["p_6_4__4"]),
            (data["p_6_5__1"], data["p_6_5__2"], data["p_6_5__3"], data["p_6_5__4"]),
            (data["p_6_6__1"], data["p_6_6__2"], data["p_6_6__3"], data["p_6_6__4"]),
            (data["p_6_7__1"], data["p_6_7__2"], data["p_6_7__3"], data["p_6_7__4"]),
        )

        TABLE_DATA_7 = (
            (data["p_7_1__1"], data["p_7_1__2"], data["p_7_1__3"]),
            (data["p_7_2__1"], data["p_7_2__2"], data["p_7_2__3"]),
            (data["p_7_3__1"], data["p_7_3__2"], data["p_7_3__3"]),
            (data["p_7_4__1"], data["p_7_4__2"], data["p_7_4__3"]),
            (data["p_7_5__1"], data["p_7_5__2"], data["p_7_5__3"]),
            (data["p_7_6__1"], data["p_7_6__2"], data["p_7_6__3"]),
            (data["p_7_7__1"], data["p_7_7__2"], data["p_7_7__3"]),
        )

        TABLE_DATA_8 = (
            (data["p_8_1__1"], data["p_8_1__2"], data["p_8_1__3"]),
            (data["p_8_2__1"], data["p_8_2__2"], data["p_8_2__3"]),
            (data["p_8_3__1"], data["p_8_3__2"], data["p_8_3__3"]),
            (data["p_8_4__1"], data["p_8_4__2"], data["p_8_4__3"]),
            (data["p_8_5__1"], data["p_8_5__2"], data["p_8_5__3"]),
        )

        TABLE_DATA_9 = (
            (data["p_9_1__1"], data["p_9_1__2"], data["p_9_1__3"]),
            (data["p_9_2__1"], data["p_9_2__2"], data["p_9_2__3"]),
            (data["p_9_3__1"], data["p_9_3__2"], data["p_9_3__3"]),
            (data["p_9_4__1"], data["p_9_4__2"], data["p_9_4__3"]),
            (data["p_9_5__1"], data["p_9_5__2"], data["p_9_5__3"]),
            (data["p_9_6__1"], data["p_9_6__2"], data["p_9_6__3"]),
            (data["p_9_7__1"], data["p_9_7__2"], data["p_9_7__3"]),
            (data["p_9_8__1"], data["p_9_8__2"], data["p_9_8__3"]),
            (data["p_9_9__1"], data["p_9_9__2"], data["p_9_9__3"]),
            (data["p_9_10__1"], data["p_9_10__2"], data["p_9_10__3"]),
            (data["p_9_11__1"], data["p_9_11__2"], data["p_9_11__3"]),
        )

        TABLE_DATA_10 = (
            (data["p_10_1__1"], data["p_10_1__2"], data["p_10_1__3"]),
            (data["p_10_2__1"], data["p_10_2__2"], data["p_10_2__3"]),
            (data["p_10_3__1"], data["p_10_3__2"], data["p_10_3__3"]),
            (data["p_10_4__1"], data["p_10_4__2"], data["p_10_4__3"]),
            (data["p_10_5__1"], data["p_10_5__2"], data["p_10_5__3"]),
        )

        grey_style = FontFace(emphasis="BOLD", fill_color=(200, 200, 200))
        headings_style = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(0, 94, 184))

        font_path = "src/utils/fonts"

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("DejaVu", style="", fname=rf"{font_path}/DejaVuSansCondensed.ttf")
        pdf.add_font("DejaVu", style="B", fname=rf"{font_path}/DejaVuSansCondensed-Bold.ttf")

        pdf.set_font("DejaVu", "B", size=10)
        pdf.cell(w=0, h=10, txt=str(data["h"]).upper(), ln=1, align="C")

        pdf.set_font("DejaVu", size=10)
        for data_row in TABLE_DATA_0:
            if data_row[0] != "":
                pdf.cell(txt=data_row[0], ln=0, align="L")
            else:
                pdf.cell(txt=" ", ln=0, align="L")
            if data_row[1] != "":
                pdf.cell(txt=data_row[1], ln=1, align="L")
            else:
                pdf.cell(txt=" ", ln=1, align="L")

        pdf.cell(txt=" ", ln=1, align="L")

        with pdf.table(
            repeat_headings=0,
            line_height=pdf.font_size,
            text_align=("CENTER", "LEFT", "CENTER", "CENTER"),
            padding=1,
            width=190,
            col_widths=(5, 25, 25, 12),
        ) as table:
            row = table.row()
            row.cell(data["h_0__1"], style=headings_style)
            row.cell(data["h_0__2"], style=headings_style)
            row.cell(data["h_0__3"], style=headings_style)
            row.cell(data["h_0__4"], style=headings_style)

            for data_row in TABLE_DATA_1:
                if data_row[0] != "":
                    row = table.row()
                    row.cell(data["h_1__1"], colspan=4, style=grey_style)
                    break
            for data_row in TABLE_DATA_1:
                if data_row[0] == "":
                    continue
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

            for data_row in TABLE_DATA_2:
                if data_row[0] != "":
                    row = table.row()
                    row.cell(data["h_2__1"], colspan=4, style=grey_style)
                    break
            for data_row in TABLE_DATA_2:
                if data_row[0] == "":
                    continue
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

            for data_row in TABLE_DATA_3:
                if data_row[0] != "":
                    row = table.row()
                    row.cell(data["h_3__1"], colspan=4, style=grey_style)
                    break
            for data_row in TABLE_DATA_3:
                if data_row[0] == "":
                    continue
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

            for data_row in TABLE_DATA_4:
                if data_row[0] != "":
                    row = table.row()
                    row.cell(data["h_4__1"], colspan=4, style=grey_style)
                    break
            for data_row in TABLE_DATA_4:
                if data_row[0] == "":
                    continue
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

            for data_row in TABLE_DATA_5:
                if data_row[0] != "":
                    row = table.row()
                    row.cell(data["h_5__1"], colspan=4, style=grey_style)
                    break
            for data_row in TABLE_DATA_5:
                if data_row[0] == "":
                    continue
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

            for data_row in TABLE_DATA_6:
                if data_row[0] != "":
                    row = table.row()
                    row.cell(data["h_6__1"], colspan=4, style=grey_style)
                    break
            for data_row in TABLE_DATA_6:
                if data_row[0] == "":
                    continue
                row = table.row()
                for datum in data_row:
                    row.cell(datum)

            row = table.row()
            row.cell(data["h_7__1"], colspan=4, style=grey_style)

            for data_row in TABLE_DATA_7:
                row = table.row()
                row.cell(data_row[0])
                row.cell(data_row[1], colspan=2)
                row.cell(data_row[2])

            row = table.row()
            row.cell(data["h_8__1"], colspan=4, style=grey_style)

            for data_row in TABLE_DATA_8:
                row = table.row()
                row.cell(data_row[0])
                row.cell(data_row[1], colspan=2)
                row.cell(data_row[2])

            row = table.row()
            row.cell(data["h_9__1"], colspan=4, style=grey_style)

            for data_row in TABLE_DATA_9:
                row = table.row()
                row.cell(data_row[0])
                row.cell(data_row[1], colspan=2)
                row.cell(data_row[2])

            row = table.row()
            row.cell(data["h_10__1"], colspan=4, style=grey_style)

            for data_row in TABLE_DATA_10:
                row = table.row()
                row.cell(data_row[0])
                row.cell(data_row[1], colspan=2)
                row.cell(data_row[2])

        pdf.write(h=10, text="\n\n\n\n")

        pdf.output(path)

        image_name_list = []

        doc = fitz.open(path)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=100)
            page_name = path + f"_page_{i}.png"
            pix.save(page_name)
            image_name_list.append(page_name)

        f = open(path, "wb")
        f.write(img2pdf.convert(image_name_list))
        f.close()

        for im in image_name_list:
            if os.path.isfile(im):
                os.remove(im)

        font_file = os.path.abspath("src/utils/fonts/DejaVuSansCondensed.ttf")
        assert os.path.exists(font_file), f"❌ Шрифт не найден по пути: {font_file}"
        pdfmetrics.registerFont(TTFont("DejaVu", font_file))
        logger.info(f"✅ Зарегистрирован шрифт DejaVu: {font_file}")

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)

        try:
            can.setFont("DejaVu", 10)
        except Exception as font_err:
            logger.error(f"❌ Ошибка при установке шрифта DejaVu: {font_err}")
            raise

        can.drawString(20, 20, "id:Проверка шрифта")  # Явно вставляем кириллицу
        can.save()
        packet.seek(0)

        new_pdf = PdfReader(packet)
        file = open(path, "rb")
        existing_pdf = PdfReader(file)
        output = PdfWriter()

        for page in existing_pdf.pages:
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

        file.close()

        output_stream = open(path, "wb")
        output.write(output_stream)
        output_stream.close()
    except Exception as e:
        logger.error(f'Ошибка при генерации: {e}', exc_info=True)
