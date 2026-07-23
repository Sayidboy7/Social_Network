from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from auth_network.models import User
from .models import Conversation



def start_chat(request, user_id):
	other_user = get_object_or_404(User, id=user_id)
	host_user = User.objects.filter(id=request.session['user_id']).first()
	
	if host_user == other_user:
		return redirect('home')

	conversation = Conversation.objects.filter(participants=host_user).filter(participants=other_user).first()


	if conversation is None:
		conversation = Conversation.objects.create()

		conversation.participants.add(
			host_user,
			other_user
		)

	return redirect('chat_room', conversation_id=conversation.id)



def room(request, conversation_id):
	current_user_id = User.objects.filter(username=request.session['username']).first().id
	conversation = get_object_or_404(
		Conversation,
		id=conversation_id
	)

	other_user = conversation.other_user(current_user_id)
	messages = conversation.messages.select_related("sender")

	return render(
		request,
		"chat/room.html",
		{
			"conversation": conversation,
			"messages": messages,
			"other_user" : other_user
		},
	)

