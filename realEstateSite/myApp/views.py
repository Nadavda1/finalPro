from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CustomerRegistrationForm, ProfessionalRegistrationForm, AnswerForm, JobDetailForm, AnswerJobForm
from django.contrib.auth import login, authenticate
from .models import JobDetail, JobApproval, Customer, Professional, Answer, Question, AnswerJob, Specialization
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    return render(request, 'home.html')


def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect after successful registration
            return redirect('customer_login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer_register.html', {'form': form})


def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            customer = Customer.objects.get(username=username)
            if customer is not None and password == customer.password:
                # Password matches, set session and redirect to customer_home
                request.session['customer_id'] = customer.id
                return redirect('customer_home')
            else:
                # Password doesn't match, handle invalid credentials error
                return render(request, 'customer_login.html', {'error_message': 'Invalid password'})
        except ObjectDoesNotExist:
            # Handle case where customer does not exist
            return render(request, 'customer_login.html', {'error_message': 'Customer does not exist'})

    return render(request, 'customer_login.html')


def professional_register(request):
    if request.method == 'POST':
        form = ProfessionalRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect after successful registration
            return redirect('professional_login')
    else:
        form = ProfessionalRegistrationForm()
    return render(request, 'professional_register.html', {'form': form})


def professional_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            professional = Professional.objects.get(username=username)
            if professional is not None and password == professional.password:
                # Password matches, set session and redirect to customer_home
                request.session['professional_id'] = professional.id
                return redirect('professional_home')
            else:
                # Password doesn't match, handle invalid credentials error
                return render(request, 'professional_login.html', {'error_message': 'Invalid password'})
        except ObjectDoesNotExist:
            # Handle case where customer does not exist
            return render(request, 'professional_login.html', {'error_message': 'professional does not exist'})

    return render(request, 'professional_login.html')


def user_type(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user_type = request.POST.get('user_type')
        if action == 'register':
            if user_type == 'professional':
                # Redirect to professional registration page
                return redirect('professional_register')
            elif user_type == 'customer':
                # Redirect to customer registration page
                return redirect('customer_register')
            else:
                # Handle invalid user type
                return HttpResponse("Invalid user type selected.")
        elif action == 'login':
            if user_type == 'professional':
                # Redirect to professional login page
                return redirect('professional_login')
            elif user_type == 'customer':
                # Redirect to customer login page
                return redirect('customer_login')
            else:
                # Handle invalid user type
                return HttpResponse("Invalid user type selected.")
        else:
            # Handle invalid action
            return HttpResponse("Invalid action.")
    else:
        # Handle GET request method if needed
        return HttpResponse("No action specified.")


def customer_home(request):
    if 'customer_id' in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(id=customer_id)
        return render(request, 'customer_home.html', {'customer': customer})
    return render(request, 'customer_home.html')


def get_best_pro(professional, ans_job_special):
    score = 0
    answer = Answer.objects.filter(professional=professional)
    for ans in answer:
        ans_job = ans_job_special.get(question=ans.question)
        if ans.answer_value == ans_job.answer_value:
            score += 2
        elif abs(ans.answer_value - ans_job.answer_value) == 1:
            score += 1

    return score


def get_matching_professionals(new_job_detail):
    available_professionals = Professional.objects.filter(is_available=False)
    answer_jobs = AnswerJob.objects.filter(jobDetail=new_job_detail)
    professionals = []
    best_professional = None
    specializations = [tag.name for tag in Specialization]
    for specialization in specializations:
        best_score = 0
        #    ans_job_special = answer_jobs.filter(question__specialization=specialization)
        for professional in available_professionals.filter(specialization=specialization):

            score = get_best_pro(professional, answer_jobs)
            if best_score < score:
                best_score = score
                best_professional = professional
        # need to check if professional exists
        professionals.append(best_professional.full_name)

    return professionals


def job_create(request):
    questions = Question.objects.all()
    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        job_form = JobDetailForm(request.POST)
        if job_form.is_valid():
            new_job_detail = job_form.save(commit=False)
            customer_id = request.session['customer_id']
            customer = Customer.objects.get(id=customer_id)
            new_job_detail.customer = customer
            new_job_detail.save()

            for question in questions:
                form = AnswerJobForm(request.POST, prefix=str(question.id))
                answer = form.save(commit=False)
                answer.question = question
                answer.jobDetail = new_job_detail
                answer.save()
            professionals = get_matching_professionals(new_job_detail)
            request.session['matching_professionals'] = list(professionals)
            request.session['new_job_detail_id'] = new_job_detail.id
            return redirect('choose_pro')  # Redirect to a success page
    else:
        job_form = JobDetailForm()
        answer_forms = [(question, AnswerJobForm(prefix=str(question.id))) for question in questions]
    answer_forms = [(question, AnswerJobForm(prefix=str(question.id))) for question in questions]
    return render(request, 'job_create.html',
                  {'job_form': job_form, 'answer_forms': answer_forms, 'customer': customer})


def job_detail(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = get_object_or_404(JobDetail, pk=job_id)

        approved_professionals = JobApproval.objects.filter(job_detail=job, approved=True)
        pending_professionals = JobApproval.objects.filter(job_detail=job, approved=False)

        return render(request, 'job_details.html', {'job': job, 'approved_professionals': approved_professionals,
                                                    'pending_professionals': pending_professionals})

    else:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(id=customer_id)
        customer_jobs = JobDetail.objects.filter(customer=customer)
        return render(request, 'job_details.html', {'jobs': customer_jobs, 'customer': customer})


def get_detail_professional(request):
    professional_id = request.session.get('professional_id')
    professional = Professional.objects.get(id=professional_id)
    specialization = professional.specialization

    questions = Question.objects.filter(specialization=specialization)

    forms = [(question, AnswerForm(prefix=str(question.id))) for question in questions]

    if request.method == 'POST':
        for question in questions:
            form = AnswerForm(request.POST, prefix=str(question.id))
            if form.is_valid():
                answer = form.save(commit=False)
                answer.professional = professional
                answer.question = question
                answer.save()
        return redirect('professional_home')

    return render(request, 'get_detail_professional.html', {'forms': forms})


def professional_home(request):
    if 'professional_id' in request.session:
        professional_id = request.session['professional_id']
        professional = Professional.objects.get(id=professional_id)
        return render(request, 'professional_home.html', {'professional': professional})
    return render(request, 'professional_home.html')


def choose_pro(request):
    if request.method == 'POST':
        selected_professionals_ids = request.POST.getlist('professional_ids')
        new_job_detail_id = request.session.get('new_job_detail_id')
        new_job_detail = JobDetail.objects.get(id=new_job_detail_id)

        for professional_id in selected_professionals_ids:
            professional = Professional.objects.get(id=professional_id)
            JobApproval.objects.create(job_detail=new_job_detail, professional=professional)

        # Redirect to a success page or wherever needed
        return redirect('customer_home')
    else:
        matching_professionals = request.session.get('matching_professionals', [])
        professionals_details = []
        for professional_name in matching_professionals:
            professional = Professional.objects.get(full_name=professional_name)
            professionals_details.append(professional)
        return render(request, 'choose_pro.html', {'professionals_details': professionals_details})


def job_offers(request):
    professional_id = request.session.get('professional_id')
    job_approvals = JobApproval.objects.filter(professional_id=professional_id, approved=False)

    if request.method == 'POST':
        selected_job_approval_ids = request.POST.getlist('job_approval_ids')

        for job_approval_id in selected_job_approval_ids:
            job_approval = JobApproval.objects.get(id=job_approval_id)
            job_approval.approved = True
            professional = Professional.objects.get(id=professional_id)
            professional.is_available = True
            professional.save()
            job_approval.save()

        # Redirect to a success page or wherever needed
        return redirect('professional_home')

    return render(request, 'job_offers.html', {'job_approvals': job_approvals})
