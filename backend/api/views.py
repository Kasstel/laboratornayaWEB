import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatMessageSerializer

OPENROUTER_API_KEY = '' # КЛЮЧ СЮДА


@api_view(['POST'])
def chat_api(request):
    serializer = ChatMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_message = serializer.validated_data['message']

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": [  # ПРОМТ ВОТ ТУТ МОЖЕШЬ ДОБАВИТЬ ЕСЛИ ХОЧЕШЬ
            {"role": "system", "content": "Ты бот поддержки магазина электроники. Так что отвечай соответственно. Если будут вопросы не по теме - пытайся вернуть пользователя в нужное русло. Если пользователь просит конкретные товары или их цены, говори что их можно посмотреть на главной странице сайта."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        return Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({"reply": reply})
