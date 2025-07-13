import tempfile
from .utils import extract_questions_from_text  # ✅ Use OCR parser
from .forms import UploadForm, AnswerForm
from django.shortcuts import render, redirect, get_object_or_404
from .utils import extract_text_from_pdf


def upload_view(request):
    if request.method == 'POST' and 'preview' in request.POST:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['uploaded_file']

            # ✅ Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            # ✅ Run OCR on saved file
            raw_text = extract_text_from_pdf(tmp_path)

            # ✅ Extract questions from OCR text
            questions = extract_questions_from_text(raw_text)

            # Save in session for preview
            request.session['question_data'] = questions
            request.session['user_info'] = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email']
            }

            return render(request, 'preview.html', {'questions': questions})

    elif request.method == 'POST' and 'confirm' in request.POST:
        questions = request.session.get('question_data', [])
        user_info = request.session.get('user_info', {})

        if not questions or not user_info:
            return redirect('upload')

        session = UserSession.objects.create(
            name=user_info['name'],
            email=user_info['email']
        )

        for q in questions:
            Question.objects.create(
                session=session,
                number=q['number'],
                text=q['text'],
                marks=q['marks']
            )

        del request.session['question_data']
        del request.session['user_info']

        return redirect('practice', id=session.questions.first().id)

    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})



def practice_view(request, id):
    question = get_object_or_404(Question, id=id)
    form = AnswerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        answer = form.save(commit=False)
        answer.question = question
        answer.save()
        next_q = Question.objects.filter(
            session=question.session,
            number__gt=question.number
        ).order_by('number').first()
        if next_q:
            return redirect('practice', id=next_q.id)
        return render(request, 'complete.html')
    return render(request, 'practice.html', {'question': question, 'form': form})
