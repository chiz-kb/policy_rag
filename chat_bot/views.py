# from django.shortcuts import render, redirect, get_object_or_404
# from app import get_rag_service

# # Create your views here.


# import json
# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from .models import Conversation, Message


# def new_chat_view(request):
#     new_conversation = Conversation.objects.create(title="New Chat")
#     return redirect('chat_view', chat_id=new_conversation.id)

# def chat_view(request, chat_id):
#     conversation = get_object_or_404(Conversation, id=chat_id)

#     # POST request from JavaScript fetch()
#     if request.method == "POST":
#         data = json.loads(request.body)
#         user_query = data.get("message", "")


#         first_message = not conversation.messages.exists()
#         if first_message or conversation.title == "New Chat":
#             # Take the first line and trim to 35 characters
#             first_line = user_query.split("\n")[0]
#             new_title = (first_line[:35] + "…") if len(first_line) > 35 else first_line
#             conversation.title = new_title
#             conversation.save(update_fields=["title"])
#         # 1. Save User Message
#         Message.objects.create(
#             conversation=conversation,
#             content=user_query,
#             is_bot=False
#         )

#         # 2. Call your RAG pipeline here (LangChain, LlamaIndex, Ollama, etc.)
#         bot_response = get_rag_service().ask(user_query)

#         # 3. Save Bot Message
#         Message.objects.create(
#             conversation=conversation,
#             content=bot_response,
#             is_bot=True
#         )

#         return JsonResponse({"reply": bot_response})
        
#     # messages = conversation.messages.order_by("timestamp")
#     # GET request: load page and previous messages
#     all_conversations = Conversation.objects.order_by("-id")
#     messages = conversation.messages.order_by("timestamp")
#     return render(request, "chat/room.html", {
#         "conversation": conversation,
#         "messages": messages,
#         "all_conversations": all_conversations,
#         "model_name": "UAV policy"  # You can change this to your model's name,
#     })



import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from langchain_core.messages import HumanMessage, AIMessage

from app import get_rag_service


def chat_page(request):
    return render(request, "chat/index.html")


@require_POST
def chat_api(request):
    try:
        data = json.loads(request.body)

        question = data.get("question", "").strip()

        if not question:
            return JsonResponse(
                {"error": "Please enter a question."},
                status=400
            )

        # Get conversation history from Django session
        history_data = request.session.get("chat_history", [])

        # Convert stored messages into LangChain messages
        chat_history = []

        for message in history_data:
            if message["role"] == "human":
                chat_history.append(
                    HumanMessage(content=message["content"])
                )
            elif message["role"] == "ai":
                chat_history.append(
                    AIMessage(content=message["content"])
                )

        # Get existing RAG service
        rag = get_rag_service()

        # Generate answer
        answer = rag.ask(
            question,
            chat_history=chat_history
        )

        # Update conversation history
        history_data.append({
            "role": "human",
            "content": question
        })

        history_data.append({
            "role": "ai",
            "content": answer
        })

        # Keep the last 10 exchanges
        request.session["chat_history"] = history_data[-20:]

        return JsonResponse({
            "question": question,
            "answer": answer
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON request."},
            status=400
        )

    except Exception as e:
        print("RAG error:", str(e))

        return JsonResponse(
            {"error": "Something went wrong while generating the answer."},
            status=500
        )


def clear_chat(request):
    request.session.pop("chat_history", None)

    return JsonResponse({
        "message": "Conversation cleared successfully."
    })
