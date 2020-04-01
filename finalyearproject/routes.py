from finalyearproject import app
from flask import render_template, request, url_for, redirect
from werkzeug.utils import secure_filename

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

from finalyearproject.forms import MapForm
from finalyearproject.models import Course, Venue

chosen_day = None


@app.route('/')
def home():
    form = MapForm()
    return render_template('home.html', form=form)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    global chosen_day
    if request.method == 'POST':
        data = request.form
        chosen_day = data['weekday']
        f = request.files['timetable']
        f.save(secure_filename('timetable.pdf'))
        return redirect(url_for('location'))


def extract_pdf():
    fp = open("timetable.pdf", 'rb')    #extract data from PDF

    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    parser.set_document(doc)
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = ''

    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text() + ","
    return extracted_text


def get_course_codes():
    pdf_data = extract_pdf()
    all_course_codes = []
    course_codes = []
    get_timetable_year = True
    for line in pdf_data.split(","):
        if get_timetable_year:
            courses = Course.query.filter_by(modYear=int(line[0]))
            get_timetable_year = False
            all_course_codes = [course.modCode for course in courses]
        words = line.split(" ")
        for word in words:
            if word in all_course_codes:
                if word not in course_codes:
                    course_codes.append(word)
    return course_codes


def get_co_ordinates():
    courses = get_course_codes()
    co_ordinates = []
    for course in courses:
        for entry in Venue.query.filter_by(course_modCode=course, day=chosen_day):
            co_ordinates.append((entry.venue, entry.course_modCode, entry.longitude, entry.latitude, entry.capacity,
                                 entry.floorNo, entry.day, entry.time))
    return co_ordinates


@app.route("/location")
def location():
    co_ordinates = get_co_ordinates()
    colours = ['blue', 'red', 'green', 'yellow', 'cyan', 'magenta', 'black', 'white', 'orange']
    icons = []
    colour_index = 0
    for co_ordinate in co_ordinates:
        icons.append([co_ordinate[0], co_ordinate[1], co_ordinate[2], co_ordinate[3], co_ordinate[4], co_ordinate[5],
                      co_ordinate[6], co_ordinate[7], colours[colour_index]])
        if colour_index == len(colours)-1:
            colour_index = 0
        else:
            colour_index += 1
    return render_template("location.html", icons=icons)


