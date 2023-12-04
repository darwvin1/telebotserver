from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from fuzzywuzzy import fuzz
import datetime
import requests


def send_messages_to_system(messages):
    # Replace the following URL with the actual endpoint of your system
    system_endpoint = 'https://dashboard.iran-tarabar.ir/api/botData1'

    # Example of sending messages using the requests library
    for message in messages:
        payload = {'message': message}
        response = requests.post(system_endpoint, data=payload)

        if response.status_code == 200:
            print(f"Message '{message}' sent successfully to the system.")
        else:
            print(f"Failed to send message '{message}' to the system. Status code: {response.status_code}")


def cleanup_old_messages():
    ten_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=10)
    old_messages = Message.objects.filter(created_at__lt=ten_minutes_ago)
    old_messages.delete()


class MessageView(APIView):
    def post(self, request, *args, **kwargs):
        received_messages = request.data.get('data', [])

        # Remove duplicates based on fuzzy matching
        unique_messages = []
        for msg in received_messages:
            exists = any(fuzz.ratio(msg.text, existing_msg) > 80 for existing_msg in Message.objects.all())
            if not exists:
                unique_messages.append(msg.text)

        send_messages_to_system(unique_messages)
        # Save unique messages to the database
        serializer = MessageSerializer(data=[{'text': msg.text} for msg in unique_messages], many=True)
        if serializer.is_valid():
            serializer.save()

        # Delete old messages from the database
        cleanup_old_messages()

        return Response(serializer.data, status=status.HTTP_200_OK)
