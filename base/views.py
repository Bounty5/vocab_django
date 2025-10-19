from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vocab, Group, FriendRequest
from django.contrib.auth.models import User
from django.contrib.auth import login
import random
import json
# Create your views here.
def add(request):
    if request.method == "POST":
        source = request.POST.get('source_word')
        target = request.POST.get('target_word')
        group = request.POST.get('group')

        if source and target and group:
            Vocab.objects.create(
                user=request.user,
                source_word=source,
                target_word=target,
                group=group
            )
            return redirect('add_vocab')

    return render(request, 'add_vocab.html')

def show_vocab(request):
    if request.user.is_authenticated:
        vocabs = Vocab.objects.filter(user=request.user)
    else:
        vocabs = Vocab.objects.all()
    return render(request, "show_vocab.html", {"vocabs":vocabs})

@login_required
def toggle_learned(request, vocab_id):
    vocab = get_object_or_404(Vocab, id=vocab_id, user=request.user)
    vocab.is_learned = not vocab.is_learned
    vocab.save()
    return redirect("show_vocab")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            return render(request, "register.html", {"error": "Passwörter stimmen nicht überein."})
        
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username existiert bereits."})
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)  # gleich einloggen
        return redirect("home")
    
    return render(request, "register.html")

@login_required
def group_list(request):
    groups = Group.objects.filter(user=request.user)
    return render(request, "group_list.html", {"groups": groups})

def add_group(request):
    if request.method == "POST":
        name = request.POST.get("name")
        source_language = request.POST.get("source_language")
        target_language = request.POST.get("target_language")
        if name and source_language and target_language:
            Group.objects.create(user=request.user, name=name, source_language=source_language, target_language=target_language)
            return redirect("group_list")
    return render(request, "add_group.html")
    
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)
    vocabs = group.vocabs.all()
    return render(request, "group_detail.html", {"group": group, "vocabs": vocabs})

@login_required
def add_vocab_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)
    if request.method == "POST":
        source = request.POST.get("source_word")
        target = request.POST.get("target_word")
        action = request.POST.get("action")

        if source and target:
            Vocab.objects.create(
                user=request.user,
                source_word=source,
                target_word=target,
                group=group
            )

            if action == "save":
                return redirect("group_detail", group_id=group.id)
            else:
                return redirect("add_vocab_to_group", group_id=group.id)
        
    return render(request, "add_vocab_to_group.html", {"group": group})

@login_required
def toggle_learned_group(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)
    group.is_learned = not group.is_learned
    group.save()
    return redirect("group_detail", group_id=group.id)

@login_required
def toggle_learned_vocab_in_group(request, vocab_id):
    vocab = get_object_or_404(Vocab, id=vocab_id, user=request.user)
    vocab.is_learned = not vocab.is_learned
    vocab.save()
    return redirect("group_detail", group_id=vocab.group.id)

@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)

    if request.method == "POST":
        group.delete()
        return redirect("group_list")

    return render(request, "confirm_delete.html", {"group": group})

@login_required
def delete_vocab(request, vocab_id):
    vocab = get_object_or_404(Vocab, id=vocab_id, user=request.user)
    group = vocab.group

    if request.method == "POST":
        vocab.delete()
        return redirect("group_detail", group_id=group.id)

    return render(request, "delete_vocab.html", {"vocab": vocab})

@login_required
def vocab_test(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)
    all_vocabs = list(group.vocabs.all())
    num_questions = min(len(all_vocabs), 15)
    questions = random.sample(all_vocabs, num_questions)

    if request.method == "POST":
            score = 0
            results = []
            for vocab in questions:
                answer = request.POST.get(f"vocab_{vocab.id}")
                correct = answer.strip().lower() == vocab.target_word.lower()
                results.append({
                    "source": vocab.source_word,
                    "target": vocab.target_word,
                    "answer": answer,
                    "correct": correct
                })
                if correct:
                    score += 1

            return render(request, "vocab_test_result.html", {
                "group": group,
                "results": results,
                "score": score,
                "total": num_questions
            })
    return render(request, "vocab_test.html", {
        "group": group,
        "questions": questions
    })

@login_required
def vocab_flashcard(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)
    vocabs = list(group.vocabs.values("source_word", "target_word"))
    vocabs_json = json.dumps(vocabs)  # <-- sorgt für korrektes JSON
    return render(request, "flashcard.html", {"group": group, "vocabs": vocabs_json})

@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    if to_user != request.user:
        FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    return redirect("friends_list")

@login_required
def accept_friend_request(request, request_id):
    f_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    f_request.status = "accepted"
    f_request.save()
    return redirect("friends_list")

@login_required
def reject_friend_request(request, request_id):
    f_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.id)
    f_request.status = "rejected"
    f_request.save()
    return redirect("friends_list")

@login_required
def friends_list(request):
    recieved = FriendRequest.objects.filter(to_user=request.user, status="pending")
    sent = FriendRequest.objects.filter(from_user=request.user)
    friends = User.objects.filter(
        id__in=[
            f.to_user.id for f in FriendRequest.objects.filter(from_user=request.user, status="accepted")]
            + [
            f.from_user.id for f in FriendRequest.objects.filter(to_user=request.user, status="accepted")
                ]
        )
    return render(request, "friends.html", {
        "recieved": recieved,
        "sent": sent,
        "friends": friends
        })

@login_required
def find_friends(request):
    # Alle Nutzer außer dir selbst
    users = User.objects.exclude(id=request.user.id)

    # Bereits gesendete oder empfangene Anfragen holen
    sent = FriendRequest.objects.filter(from_user=request.user)
    received = FriendRequest.objects.filter(to_user=request.user)

    # IDs von Leuten, an die du schon was gesendet hast oder von denen du was bekommen hast
    sent_ids = [f.to_user.id for f in sent]
    received_ids = [f.from_user.id for f in received]

    # IDs deiner akzeptierten Freunde
    accepted_sent = FriendRequest.objects.filter(from_user=request.user, status='accepted')
    accepted_received = FriendRequest.objects.filter(to_user=request.user, status='accepted')
    friend_ids = [f.to_user.id for f in accepted_sent] + [f.from_user.id for f in accepted_received]

    # Nutzer herausfiltern, die du schon kennst (Anfragen oder Freunde)
    users = users.exclude(id__in=sent_ids + received_ids + friend_ids)

    return render(request, 'find_friends.html', {
        'users': users
    })
