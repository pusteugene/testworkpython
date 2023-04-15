from django.db.migrations import serializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer

class ThreadListCreateView(APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, format=None):
        # ...
        return self.paginator.get_paginated_response(serializer.data)

class ThreadRetrieveUpdateDestroyView(APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, pk, format=None):
        # ...
        return self.paginator.get_paginated_response(serializer.data)

class MessageListCreateView(APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, thread_id, format=None):
        # ...
        return self.paginator.get_paginated_response(serializer.data)

class MessageRetrieveUpdateDestroyView(APIView):
    pagination_class = LimitOffsetPagination

    def get(self, request, pk, format=None):
        # ...
        return self.paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_thread(request):
    participants = request.data.get('participants', None)
    if not participants or len(participants) != 2:
        return Response({'error': 'Invalid number of participants. Thread must have exactly 2 participants.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if thread with the same participants already exists
    thread = Thread.objects.filter(participants__contains=participants).first()
    if thread:
        serializer = ThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = ThreadSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    thread.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class ThreadViewSet(viewsets.ModelViewSet):
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Thread.objects.filter(participants__contains=[self.request.user.id])
        return queryset.order_by('-updated')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_message_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.is_read = True
    message.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages_count(request):
    count = Message.objects.filter(thread__participants__contains=request.user.id, is_read=False).count()
    return Response({'count': count}, status=status.HTTP_200_OK)
