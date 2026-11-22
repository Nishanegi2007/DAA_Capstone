"""Build the Mini Courier Planner capstone report DOCX."""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "phase5_final" / "Mini_Courier_Planner_Report.docx"


def shade(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_borders(cell, color="D9D9D9", size="6") -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = "w:" + edge
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def set_cell_margins(cell, top=100, start=120, bottom=100, end=120) -> None:
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    margins = tc_pr.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        tc_pr.append(margins)
    for m, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = margins.find(qn("w:" + m))
        if node is None:
            node = OxmlElement("w:" + m)
            margins.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def format_table(table, header=True, widths=None) -> None:
    table.autofit = False
    for row_idx, row in enumerate(table.rows):
        for col_idx, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if widths:
                cell.width = Inches(widths[col_idx])
            set_cell_borders(cell)
            set_cell_margins(cell)
            if header and row_idx == 0:
                shade(cell, "24476B")
            elif row_idx % 2 == 0:
                shade(cell, "F1F5F9")
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_after = Pt(1)
                paragraph.paragraph_format.space_before = Pt(1)
                for run in paragraph.runs:
                    run.font.name = "Aptos"
                    run.font.size = Pt(9.2)
                    if header and row_idx == 0:
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)


def add_table(doc, headers, rows, widths=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    for i, text in enumerate(headers):
        table.rows[0].cells[i].text = str(text)
    for row in rows:
        cells = table.add_row().cells
        for i, text in enumerate(row):
            cells[i].text = str(text)
    format_table(table, header=True, widths=widths)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Mini Courier Planner  |  ")
    run.font.name = "Aptos"
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(100, 110, 120)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    paragraph._p.append(field)


def body(doc, text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.line_spacing = 1.08
    return p


def heading(doc, text, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.add_run(text)
    return p


def main():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.72)
    section.right_margin = Inches(0.72)

    normal = doc.styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor(35, 42, 48)
    normal.paragraph_format.space_after = Pt(7)
    for style_name, size in (("Title", 28), ("Heading 1", 17), ("Heading 2", 12)):
        style = doc.styles[style_name]
        style.font.name = "Aptos Display" if style_name != "Heading 2" else "Aptos"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_before = Pt(12 if style_name != "Title" else 0)
        style.paragraph_format.space_after = Pt(5)
    # Remove the default Title style's decorative paragraph rule.
    title_ppr = doc.styles["Title"]._element.get_or_add_pPr()
    title_border = title_ppr.find(qn("w:pBdr"))
    if title_border is not None:
        title_ppr.remove(title_border)

    add_page_number(section.footer.paragraphs[0])

    kicker = doc.add_paragraph()
    kicker.paragraph_format.space_after = Pt(7)
    run = kicker.add_run("DESIGN & ANALYSIS OF ALGORITHMS  |  ETCCDA302")
    run.font.name = "Aptos"
    run.font.size = Pt(9)
    run.font.bold = True
    run.font.color.rgb = RGBColor(73, 92, 108)

    p = doc.add_paragraph(style="Title")
    p.add_run("Mini Courier Planner")
    title_paragraph_ppr = p._p.get_or_add_pPr()
    direct_title_border = title_paragraph_ppr.find(qn("w:pBdr"))
    if direct_title_border is not None:
        title_paragraph_ppr.remove(direct_title_border)
    subtitle = doc.add_paragraph()
    subtitle.paragraph_format.space_after = Pt(12)
    sr = subtitle.add_run("Capstone Project Report")
    sr.font.name = "Aptos"
    sr.font.size = Pt(15)
    sr.font.color.rgb = RGBColor(73, 92, 108)
    body(doc, "A Python prototype that prioritizes parcels, selects a load within vehicle capacity, and plans a delivery route over a weighted road network. This report documents the design, algorithms, demonstration results, performance measurements, and project run instructions.")
    add_table(doc, ["Course", "Programme", "Institution", "Faculty"], [[
        "Design & Analysis of Algorithms (ETCCDA302)",
        "B.Tech CSE & Specializations",
        "K.R. Mangalam University, Gurugram",
        "Dr. Shweta Agarwal",
    ]], widths=[1.85, 1.65, 1.8, 1.35])

    heading(doc, "1  Project Overview")
    body(doc, "The planner integrates four algorithmic components from the capstone assignment. Merge Sort orders parcels by deadline and priority. Dynamic programming selects a high-value set of parcels that fits the van. Dijkstra computes shortest paths between locations. A nearest-neighbor heuristic chooses the order in which delivery locations are visited.")
    body(doc, "The supplied sample contains 60 parcels, 20 customer locations, and 34 undirected road connections. The vehicle starts and ends at Warehouse. Multiple parcels for the same customer are delivered in one stop.")

    heading(doc, "2  Data and System Design")
    add_table(doc, ["Parcel field", "Meaning"], [
        ("id", "Unique parcel identifier"),
        ("destination", "Customer location for delivery"),
        ("weight_g", "Positive whole-number parcel weight in grams"),
        ("priority", "Urgency rank: 1 is highest, 3 is lowest"),
        ("deadline_days", "Days remaining until the deadline"),
        ("value", "Benefit score maximized by knapsack"),
    ], widths=[1.5, 5.15])
    body(doc, "Road data in data/roads.csv stores start location, end location, and distance_km. The graph is represented as an adjacency list and treats each road as bidirectional. All road distances are positive whole kilometers.")
    body(doc, "Processing flow: read CSV data → sort parcels → select a feasible load → compute shortest road paths → choose delivery stops → expand the route to road-by-road locations → display totals and performance evidence.")

    heading(doc, "3  Algorithms")
    add_table(doc, ["Algorithm", "Role in the planner", "Complexity"], [
        ("Merge Sort", "Sort by deadline, then priority, then parcel ID.", "O(n log n) time; O(n) extra space"),
        ("0/1 Knapsack DP", "Maximize total value without exceeding capacity W.", "O(nW) time and space"),
        ("Dijkstra with min-heap", "Find shortest paths over nonnegative road weights.", "O((V + E) log V)"),
        ("Nearest-neighbor TSP", "Choose the closest unvisited customer, then return to the depot.", "O(k²) over k stops, plus shortest-path calculations"),
    ], widths=[1.4, 3.5, 1.75])
    body(doc, "Sorting and packing answer different questions. Sorting provides an urgency order; knapsack chooses a value-maximizing combination and does not simply take the first parcels in that order. The sample values are demonstration scores and should be replaced by a documented business rule in a real system.")

    heading(doc, "4  Parcel Selection Results")
    body(doc, "At a vehicle capacity of 10,000 g (10 kg), the dynamic-programming selection contains 11 parcels with a combined weight of 9,914 g and total value 967. The load remains 86 g below capacity.")
    add_table(doc, ["Result", "Value"], [
        ("Vehicle capacity", "10,000 g"),
        ("Selected parcel count", "11"),
        ("Total selected weight", "9,914 g"),
        ("Total selected value", "967"),
        ("Remaining capacity", "86 g"),
    ], widths=[3.2, 3.45])
    body(doc, "Selected parcel IDs: P040, P052, P002, P014, P026, P042, P013, P041, P053, P015, and P039.")

    doc.add_page_break()
    heading(doc, "5  Road Network and Delivery Route")
    body(doc, "The diagram shows all 21 locations and the distance on each road. Red edges and nodes trace the current 10,000 g delivery plan; gray edges are other roads available to Dijkstra. The graph is an abstract network and is not drawn to geographic scale.")
    graph_image = EVIDENCE / "phase3_routes" / "road_network_10000g.png"
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(graph_image), width=Inches(6.7))
    caption = doc.add_paragraph("Figure 1. Road network and selected 10,000 g delivery route. Road labels are distances in kilometers.")
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.paragraph_format.space_after = Pt(8)
    for run in caption.runs:
        run.italic = True
        run.font.size = Pt(8.5)

    body(doc, "The nearest-neighbor order is expanded into connected road segments. The corrected route starts with Warehouse → Customer_01 → Customer_02 → Customer_07, continues through Customer_06, Customer_11, Customer_12, Customer_13, Customer_14, Customer_15, Customer_20, Customer_19, Customer_18, Customer_17, and Customer_16, then returns to Warehouse. Customer_01 is both a selected destination and the shortest first leg from the warehouse to Customer_02.")
    add_table(doc, ["Route result", "Value"], [
        ("Shortest path example", "Warehouse → Customer_16 → Customer_17 → Customer_18"),
        ("Example path distance", "14 km"),
        ("Full delivery route distance", "78 km"),
    ], widths=[2.0, 4.65])
    body(doc, "Nearest neighbor is an approximation: every individual leg uses a shortest road path, but the overall tour is not guaranteed to be the globally shortest route.")

    doc.add_page_break()
    heading(doc, "6  Performance Measurements")
    body(doc, "The benchmark uses deterministic generated inputs and averages repeated runs with time.perf_counter(). Merge Sort and Dijkstra use five repeats; knapsack and route planning use three. The measurements below are specific to the computer and Python environment used for this run.")
    add_table(doc, ["Component and input", "Average runtime"], [
        ("Merge Sort, 20 parcels", "0.110 ms"),
        ("Merge Sort, 200 parcels", "0.472 ms"),
        ("Knapsack, 20 parcels, capacity 5,000", "13.872 ms"),
        ("Knapsack, 200 parcels, capacity 5,000", "205.706 ms"),
        ("Dijkstra, 20 graph nodes", "0.042 ms"),
        ("Dijkstra, 200 graph nodes", "0.245 ms"),
        ("Route, 5 stops on 20-node graph", "0.385 ms"),
        ("Route, 5 stops on 200-node graph", "3.540 ms"),
    ], widths=[4.5, 2.15])
    body(doc, "Knapsack takes longer because its DP work depends on both parcel count and capacity. Dijkstra runs quickly on these small sparse graphs and appears nearly flat on the shared linear chart scale. The route benchmark keeps the stop count at five while increasing graph size. Very short Merge Sort timings vary between runs, so the small non-monotonic differences are measurement noise.")
    chart_image = EVIDENCE / "phase4_performance" / "runtime_chart.png"
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(chart_image), width=Inches(6.65))
    caption = doc.add_paragraph("Figure 2. Average runtime by component. Input-size units differ by component; see the CSV for exact measurements.")
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in caption.runs:
        run.italic = True
        run.font.size = Pt(8.5)

    heading(doc, "7  Limitations and Improvements")
    body(doc, "The route heuristic can produce a longer tour than an exact TSP solution. Knapsack uses integer capacity in grams, so very large capacities increase its memory and runtime costs. The value scores are illustrative. Future work could define operational value scores, compare route heuristics, and benchmark larger sparse road networks with multiple stop counts.")

    heading(doc, "8  Running the Project")
    body(doc, "From the project root, install the chart dependency and launch the command-line app:")
    code = doc.add_paragraph()
    code.paragraph_format.left_indent = Inches(0.25)
    code.paragraph_format.space_after = Pt(8)
    r = code.add_run("python -m pip install -r requirements.txt\npython main.py")
    r.font.name = "Consolas"
    r.font.size = Pt(9.5)
    heading(doc, "Conclusion")
    body(doc, "The prototype integrates parcel prioritization, capacity-aware selection, shortest-path computation, and approximate multi-stop routing. The corrected 10,000 g demonstration selects a feasible 9,914 g load and produces a connected 78 km route over the supplied road network. The project includes source code, sample data, runtime evidence, and a route diagram for demonstration.")

    doc.core_properties.title = "Mini Courier Planner Capstone Project Report"
    doc.core_properties.subject = "Design and Analysis of Algorithms capstone"
    doc.core_properties.author = ""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
