from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Students, Semester, AdminData, Subjects, Course, Tutorials, PollSubmitted, Polls, ContactQueries
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

def index(request):
	if request.session.has_key('username'):
		return redirect('/home/')
	else:
		return redirect('/login/')

def terms(request):
	return render(request, 'main/terms.html')

def home(request):
	if request.session.has_key('username'):
		username = request.session['username']
		no_of_semesters = len(Semester.objects.all()) + 1
		no_of_tutorials = len(Tutorials.objects.all())
		data = {
			'username': username,
			'no_of_tutorials': no_of_tutorials,
			'no_of_semesters': no_of_semesters
		}
		return render(request, 'main/home.html', data)
	else:
		return redirect('/login/')

def polls(request):
	if request.session.has_key('username'):
		username = request.session['username']

		submitted_by_user = []
		all_submitted_polls = PollSubmitted.objects.all()
		for polls in all_submitted_polls:
			print(polls)
			if polls.username == Students.objects.get(username=username):
				print(f"POLL ID : {polls.poll_id}")
				submitted_by_user.append(int(polls.poll_id))

		print(f"Submitted by user {submitted_by_user}")
		available_polls = []
		all_polls = Polls.objects.order_by('-datetime')
		for polls in all_polls:
			if polls.id not in submitted_by_user:
				available_polls.append(polls)

		no_of_polls = len(available_polls)

		data = {
			'username': username,
			'all_polls': available_polls,
			'no_of_polls': no_of_polls,
		}
		return render(request, 'main/polls.html', data)
	else:
		return redirect('/login/')
		

def poll_voting(request, poll_id, poll_topic):
	if request.session.has_key('username'):
		username = request.session['username']
		try:
			poll_to_vote = Polls.objects.get(id=poll_id)
		except:
			return redirect('/polls/')
		all_submitted_polls = PollSubmitted.objects.all()
		for submit_poll in all_submitted_polls:
			if submit_poll.username == Students.objects.get(username=username) and submit_poll.poll_topic == poll_to_vote.poll_topic:
				return redirect('/polls/')
		data = {
			'username': username,
			'poll_to_vote': poll_to_vote,
		}

		if request.method == 'POST':
			poll_choice = request.POST['poll_choice']
			print(poll_choice)

			username_instance = Students.objects.get(username=username)
			submit_poll = PollSubmitted(
							poll_id=poll_id,
							poll_topic=poll_topic,
							username=username_instance,
							option_selected=poll_choice,
							datetime=datetime.now(),
						)
			print("Poll Submitted!!")

			submit_poll.save()

			poll_to_vote.submitted = str(int(poll_to_vote.submitted)+1)
			option_scores = [0,0,0,0]
			for submit_poll in all_submitted_polls:
				if submit_poll.poll_topic == poll_topic:
					if submit_poll.option_selected == poll_to_vote.option_1:
						option_scores[0] += 1
					elif submit_poll.option_selected == poll_to_vote.option_2:
						option_scores[1] += 1
					elif submit_poll.option_selected == poll_to_vote.option_3:
						option_scores[2] += 1
					elif submit_poll.option_selected == poll_to_vote.option_4:
						option_scores[3] += 1
			max_score = max(option_scores)

			print(option_scores)
			print(max_score)
			leading_option_text = ""

			if max_score != 0:
				if option_scores[0] == max_score:
					leading_option_text += f"{poll_to_vote.option_1} / "
				if option_scores[1] == max_score:
					leading_option_text += f"{poll_to_vote.option_2} / "
				if option_scores[2] == max_score:
					leading_option_text += f"{poll_to_vote.option_3} / "
				if option_scores[3] == max_score:
					leading_option_text += f"{poll_to_vote.option_4} / "

			poll_to_vote.leading_option = leading_option_text

			poll_to_vote.save()
			return redirect('/polls/')

		return render(request, 'main/poll_voting.html', data)
	else:
		return redirect('/login/')

def my_account(request):
	if request.session.has_key('username'):
		username = request.session['username']

		student_details = Students.objects.get(username=username)
		data = {
			'username': username,
			'student': student_details,
		}
		return render(request, 'main/account.html', data)
	else:
		return redirect('/login/')

def about(request):
	if request.session.has_key('username'):
		username = request.session['username']
		data = {
			'username': username
		}
		return render(request, 'main/about.html', data)
	else:
		return redirect('/login/')

def semesters(request):
	if request.session.has_key('username'):
		username = request.session['username']

		all_semesters = Semester.objects.all()

		data = {
			'username' : username,
			'semesters': all_semesters,
		}

		return render(request, 'main/semesters.html', data)
	else:
		return redirect('/login/')

def subjects(request, semester):
	if request.session.has_key('username'):
		username = request.session['username']
		semester_instance = Semester.objects.get(semester_number=semester)
		subjects = Subjects.objects.filter(semester=semester_instance).all()
		coming_soon = False
		if len(subjects) == 0:
			coming_soon = True
		data = {
			'username': username,
			'subjects': subjects,
			'semester': semester,
			'coming_soon': coming_soon,
		}
		return render(request, 'main/subjects.html', data)
	else:
		return redirect('/login/')

def tutorials(request, subject):
	if request.session.has_key('username'):
		username = request.session['username']
		subject_instance = Subjects.objects.get(subject_code=subject)
		all_tutorials = Tutorials.objects.filter(subject=subject_instance).all()
		coming_soon = False
		if len(all_tutorials) == 0:
			coming_soon = True
		data = {
			'username': username,
			'tutorials': all_tutorials,
			'subject': subject_instance.subject_name,
			'subject_code': subject,
			'coming_soon': coming_soon,
		}
		return render(request, 'main/tutorials.html', data)
	else:
		return redirect('/login/')


def login(request):
	if request.session.has_key('username'):
		return redirect('/home/')
	elif request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		try:
			find_user = Students.objects.get(username=username)
			user_password = find_user.password
		except:
			find_user = None

		if find_user != None and check_password(password, user_password):
			print("user logged in")
			request.session['username'] = find_user.username
			return redirect('/home/')

		elif find_user != None and user_password != password:
			messages.info(request, 'Incorrect Password!')

		else:
			messages.info(request, 'Username not Found!')

		return redirect('/login/')

	else:
		return render(request, 'main/login.html')


def register(request):
	if request.session.has_key('username'):
		return redirect('/home/')

	elif request.method == 'POST':
		fullname = request.POST['fullname']
		username = request.POST['username']
		email = request.POST['email']
		gender = request.POST['gender']
		course = request.POST['course']
		admission_id= request.POST['admission_id']
		password = request.POST['password']
		course_year = request.POST['course_year']

		data = {
			'username' : username,
			'email' : email,
			'fullname' : fullname,
		}

		valid_username = True
		invalid_characters = ".! #$%^&*()<>?/;:'=+-[]|\""

		for char in username:
			if(char in invalid_characters):
				valid_username = False

		if valid_username == False:
			messages.warning(request, 'Special Characters not allowed in Username!')
			return render(request, 'main/register.html', data)


		email_pre_exists = False
		username_pre_exists = False
		valid_password = True
		admission_id_pre_exists = False

		data_from_database = Students.objects.all()

		for user in data_from_database:
			if(user.email == email):
				email_pre_exists = True
				messages.warning(request, 'Email already exists!')
				return render(request, 'main/register.html', data)

		for user in data_from_database:
			if(user.username == username):
				username_pre_exists = True
				messages.warning(request, 'Username not available!')
				return render(request, 'main/register.html', data)

		for user in data_from_database:
			if(user.admission_no == admission_id):
				admission_id_pre_exists = True
				messages.warning(request, 'Admission Id is already registered!')
				return render(request, 'main/register.html', data)

		password_invalidity = 0

		length_of_password = len(password)
		if(length_of_password < 6):
			password_invalidity+=1

		if(password_invalidity!=0):
			valid_password = False
			messages.warning(request, 'Password length must be 6 or more!')
			return render(request, 'main/register.html', data)

		encrypted_password = make_password(password)
		registering_user = Students(
									username=username,
									email=email,
									fullname=fullname,
									gender=gender,
									course=course,
									admission_no=admission_id,
									password=encrypted_password,
									datetime=datetime.now(),
									course_year=course_year,
									)
		registering_user.save()
		print("user registered!!")
		request.session['username'] = username
		return redirect('/home/')
	return render(request, 'main/register.html')


def logout(request):
	if request.session.has_key('username'):
		try:
			del request.session['username']
			return redirect('/login/')
		except:
			pass
	return redirect('/')


def error_404(request, exception):
	data = {}
	return render(request, 'main/404.html', data)

def error_500(request):
	data = {}
	return render(request, 'main/500.html', data)