from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db.models import Avg
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import CustomUserCreationForm, ProgramUploadForm, CommentForm, ComplaintForm, EditProfileForm, RatingForm
from .forms import PasswordResetRequestForm, SecretQuestionAnswerForm
from .models import Comment, Complaint, User, Program, Rating


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # Збереження секретного питання та відповіді
            user.secret_question = form.cleaned_data['secret_question']
            user.secret_answer = form.cleaned_data['secret_answer']
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def upload_program(request):
    if request.method == 'POST':
        form = ProgramUploadForm(request.POST, request.FILES)
        if form.is_valid():
            program = form.save(commit=False)
            program.uploaded_by = request.user
            program.save()
            return redirect('program_detail', program_id=program.id)
    else:
        form = ProgramUploadForm()
    return render(request, 'upload_program.html', {'form': form})


def program_detail(request, program_id):
    program = Program.objects.get(id=program_id)
    comments = Comment.objects.filter(program=program)
    complaints = Complaint.objects.filter(program=program)
    average_rating = program.ratings.aggregate(Avg('score'))['score__avg']
    return render(request, 'program_detail.html', {'program': program, 'comments': comments, 'complaints': complaints,
                                                   'average_rating': average_rating})


@login_required
def add_comment(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    user = request.user
    if user.is_blocked:
        messages.error(request, "Ваш обліковий запис заблоковано. Ви не можете додавати коментарі.")
        return redirect('program_detail', program_id=program.id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.program = program
            comment.author = user
            comment.save()
            return redirect('program_detail', program_id=program.id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'program': program})


@login_required
def submit_complaint(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    if request.user.is_blocked:
        messages.error(request, "Ваш обліковий запис заблоковано. Ви не можете подавати скарги.")
        return redirect('program_detail', program_id=program.id)
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.program = program
            complaint.author = request.user
            complaint.save()
            messages.success(request, "Вашу скаргу успішно подано.")
            return redirect('program_detail', program_id=program.id)
    else:
        form = ComplaintForm()
    return render(request, 'submit_complaint.html', {'form': form, 'program': program})


def about_us(request):
    return render(request, 'about_us.html')


def contact(request):
    return render(request, 'contact.html')


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


def home(request):
    programs = Program.objects.all()
    return render(request, 'home.html', {'programs': programs})


def filter_programs(request):
    category_id = request.GET.get('category')
    genre_id = request.GET.get('genre')
    if category_id:
        programs = Program.objects.filter(category_id=category_id)
    elif genre_id:
        programs = Program.objects.filter(genre_id=genre_id)
    else:
        programs = Program.objects.all()
    return render(request, 'home.html', {'programs': programs})


@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})


@login_required
def manage_programs(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden()
    programs = Program.objects.all()
    return render(request, 'manage_programs.html', {'programs': programs})


@login_required
def view_complaints(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    complaints = Complaint.objects.all()
    if search_query:
        complaints = complaints.filter(program__title__icontains=search_query)
    if status_filter == 'resolved':
        complaints = complaints.filter(resolved=True)
    elif status_filter == 'unresolved':
        complaints = complaints.filter(resolved=False)
    return render(request, 'view_complaints.html', {'complaints': complaints})


@login_required
def edit_program(request, program_id):
    program = Program.objects.get(id=program_id)
    if request.user != program.uploaded_by and not request.user.is_superuser and not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProgramUploadForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            form.save()
            return redirect('program_detail', program_id=program.id)
    else:
        form = ProgramUploadForm(instance=program)
    return render(request, 'edit_program.html', {'form': form, 'program': program})


@login_required
def delete_program(request, program_id):
    program = Program.objects.get(id=program_id)
    if request.user != program.uploaded_by and not request.user.is_superuser:
        return HttpResponseForbidden()
    program.delete()
    return redirect('home')


@login_required
def resolve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "У вас немає прав на вирішення цієї скарги.")
        return redirect('view_complaints')
    complaint.resolved = True
    complaint.save()
    messages.success(request, "Скарга була успішно вирішена.")
    return redirect('view_complaints')


def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def manage_moderators(request):
    users = User.objects.all()
    query = request.GET.get('username')
    user_filter = request.GET.get('user_filter')
    if query:
        users = users.filter(username__icontains=query)
    if user_filter == 'staff':
        users = users.filter(is_staff=True)
    elif user_filter == 'users':
        users = users.filter(is_staff=False, is_superuser=False)
    return render(request, 'manage_moderators.html', {'users': users})


@login_required
@user_passes_test(is_superuser)
def add_moderator(request, user_id):
    return change_moderator_status(request, user_id, True)


@login_required
@user_passes_test(is_superuser)
def remove_moderator(request, user_id):
    return change_moderator_status(request, user_id, False)


def change_moderator_status(request, user_id, is_adding):
    if request.method == 'POST':
        admin_password = request.POST.get('admin_password')
        if check_password(admin_password, request.user.password):
            user = User.objects.get(id=user_id)
            user.is_staff = is_adding
            user.save()
            return HttpResponseRedirect(reverse('manage_moderators'))
        else:
            messages.error(request, 'Неправильний пароль')
            return redirect('manage_moderators')
    else:
        return HttpResponseForbidden()


@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    user_programs = Program.objects.filter(uploaded_by=user)
    return render(request, 'user_profile.html', {'user': user, 'programs': user_programs})


def search(request):
    query = request.GET.get('q', '')
    if query:
        programs = Program.objects.filter(title__icontains=query)
        users = User.objects.filter(username__icontains=query)
    else:
        programs = Program.objects.all()
        users = User.objects.none()
    return render(request, 'search.html', {'programs': programs})


@login_required
def block_user(request, user_id):
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "У вас немає прав на виконання цієї дії.")
        return redirect('user_list')
    user_to_block = get_object_or_404(User, id=user_id)
    if user_to_block.is_superuser or user_to_block == request.user:
        messages.error(request, "Цю дію неможливо виконати.")
        return redirect('user_list')
    user_to_block.is_blocked = True
    user_to_block.save()
    messages.success(request, f"Користувач {user_to_block.username} був успішно заблокований.")
    return redirect('user_list')


def rules(request):
    return render(request, 'rules.html')


def change_theme(request):
    return render(request, 'change_theme.html')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def logout_view(request):
    logout(request)
    return redirect('home')


def user_programs(request, username):
    programs = Program.objects.filter(uploaded_by__username=username)
    return render(request, 'user_programs.html', {'programs': programs})


@login_required
def rate_program(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.get_or_create(
                program=program,
                user=request.user,
                defaults={'score': form.cleaned_data['score']}
            )
            if not created:
                rating.score = form.cleaned_data['score']
                rating.save()
            return redirect('program_detail', program_id=program.id)
    else:
        form = RatingForm()
    return render(request, 'rate_program.html', {'form': form, 'program': program})


def user_list(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden()
    username_query = request.GET.get('username', '')
    users = User.objects.filter(username__icontains=username_query, is_staff=False, is_superuser=False)
    return render(request, 'user_list.html', {'users': users})


@login_required
def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "У вас немає прав на виконання цієї дії.")
        return redirect('user_list')
    user.is_blocked = False
    user.save()
    messages.success(request, f"Користувач {user.username} був успішно розблокований.")
    return redirect('user_list')

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                request.session['user_id_for_reset'] = user.id  # Зберігаємо ID користувача в сесії
                return redirect('secret_question')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'password_reset_request.html', {'form': form})

def secret_question(request):
    user_id = request.session.get('user_id_for_reset')
    if not user_id:
        return redirect('password_reset_request')  # Перенаправлення, якщо ID не в сесії
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = SecretQuestionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['answer'] == user.secret_answer:
                return redirect('set_new_password')
            else:
                # Якщо відповідь неправильна, показати помилку (використовуйте Django messages або JavaScript для модального вікна)
                pass
    else:
        form = SecretQuestionForm()
    return render(request, 'secret_question.html', {'form': form, 'question': user.secret_question})

def set_new_password(request):
    user_id = request.session.get('user_id_for_reset')
    if not user_id:
        return redirect('password_reset_request')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['new_password1'] == form.cleaned_data['new_password2']:
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                # Очистити сесію після зміни паролю
                del request.session['user_id_for_reset']
                return redirect('login')
            else:
                # Повідомлення про помилку, що паролі не співпадають
                pass
    else:
        form = SetNewPasswordForm()
    return render(request, 'set_new_password.html', {'form': form})

