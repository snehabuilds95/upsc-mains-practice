#from django.shortcuts import render




#def upload_view(request):
 #   return render(request, 'upload.html')  # ✅

#def practice_view(request, id):
 #   return render(request, 'practice.html')  # ✅


from django.shortcuts import render, redirect, get_object_or_404
from .models import UserSession, Question, Answer
from .forms import UploadForm, AnswerForm
import pytesseract
from PIL import Image
import re
from PyPDF2 import PdfReader
import tempfile

def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            session = form.save()
            file = session.uploaded_file
            extract_questions_from_file(file, session)
            return redirect('practice', id=session.questions.first().id)
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})

def extract_questions_from_file(file, session):
    text = ""
    if file.name.endswith('.pdf'):
        reader = PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
    elif file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
        with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
            temp_file.write(file.read())
            image = Image.open(temp_file.name)
            text = pytesseract.image_to_string(image)

    print("DEBUG TEXT:\n", text[:1000])  # optional: to inspect the first 1000 characters

    question_blocks = re.findall(r"(\d+)\.\s+(.*?)(?=\d+\.\s+|$)", text, re.DOTALL)

    for number, qtext in question_blocks:
        # Try to extract marks from the end of the question
        marks_match = re.search(r"(\d{1,2}½|\d{1,2})\s*$", qtext)
        marks = 0
        if marks_match:
            raw_marks = marks_match.group(1)
            if '½' in raw_marks:
                marks = float(raw_marks.replace('½', '.5'))
            else:
                marks = int(raw_marks)
        Question.objects.create(
            session=session,
            number=int(number),
            text=qtext.strip(),
            marks=marks
        )



def practice_view(request, id):
    question = get_object_or_404(Question, id=id)
    form = AnswerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        answer = form.save(commit=False)
        answer.question = question
        # time can be added here later
        answer.save()
        next_q = Question.objects.filter(session=question.session, number__gt=question.number).order_by('number').first()
        if next_q:
            return redirect('practice', id=next_q.id)
        return render(request, 'complete.html')  # Show end message
    return render(request, 'practice.html', {'question': question, 'form': form})
