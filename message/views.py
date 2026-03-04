from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.contrib.auth.models import User
from .models import Message
from item.models import Item


@login_required
def message_list(request):
    # Message list page | 消息列表页面

    # Get all conversations of the current user | 获取当前用户的所有对话
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver', 'item').order_by('-created_at')

    # Group conversations and keep only the latest message for each user | 对对话进行分组，每个用户只保留最新的一条消息
    user_latest_messages = {}
    for msg in conversations:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        if other_user.id not in user_latest_messages:
            user_latest_messages[other_user.id] = {
                'message': msg,
                'other_user': other_user,
                'unread_count': 0
            }

    # Get unread message count | 获取未读消息数量
    unread_messages = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).values('sender').annotate(count=Count('id'))

    # Update unread message count | 更新未读消息数量
    for unread in unread_messages:
        sender_id = unread['sender']
        if sender_id in user_latest_messages:
            user_latest_messages[sender_id]['unread_count'] = unread['count']

    return render(request, 'message/message_list.html', {
        'conversations': user_latest_messages.values(),
        'total_unread': Message.objects.filter(receiver=request.user, is_read=False).count()
    })


@login_required
def message_send_message(request):
    # Send a message | 发送消息
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        item_id = request.POST.get('item_id')
        content = request.POST.get('content')

        if not content:
            return JsonResponse({'status': 'error', 'message': 'Message content cannot be empty'})

        try:
            receiver = User.objects.get(id=receiver_id)
            item = Item.objects.get(id=item_id) if item_id else None

            # Create message | 创建消息
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                item=item,
                content=content,
                is_read=False
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Message sent successfully',
                'data': {
                    'message_id': message.id,
                    'created_at': message.created_at.strftime('%Y-%m-%d %H:%M')
                }
            })

        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Receiver does not exist'})
        except Item.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item does not exist'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Send failed: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Request method not allowed'})


@login_required
def message_get_unread_count(request):
    # Get unread message count | 获取未读消息数量
    try:
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
        return JsonResponse({'status': 'success', 'count': count})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def message_chat_history(request):
    # Get chat history with a specific user | 获取与特定用户的聊天历史
    try:
        user_id = request.GET.get('user_id')
        other_user = get_object_or_404(User, id=user_id)

        # Get all messages between both users | 获取双方之间的所有消息
        messages = Message.objects.filter(
            (Q(sender=request.user, receiver=other_user) |
             Q(sender=other_user, receiver=request.user))
        ).order_by('created_at')

        # Format messages into JSON | 将消息格式化为JSON
        message_list = [{
            'content': msg.content,
            'is_sent': msg.sender == request.user,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M'),
            'item': {
                'id': msg.item.id,
                'title': msg.item.title
            } if msg.item else None
        } for msg in messages]

        return JsonResponse({
            'status': 'success',
            'messages': message_list
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


@login_required
def message_mark_as_read(request):
    # Mark all unread messages from a specific user as read | 将与特定用户的所有未读消息标记为已读
    try:
        sender_id = request.POST.get('sender_id')
        if sender_id:

            # Mark all unread messages from the sender as read | 将来自特定发送者的所有未读消息标记为已读
            Message.objects.filter(
                sender_id=sender_id,
                receiver=request.user,
                is_read=False
            ).update(is_read=True)

            return JsonResponse({'status': 'success'})

        return JsonResponse({'status': 'error', 'message': 'Missing sender ID'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})