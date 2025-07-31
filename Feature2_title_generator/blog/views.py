from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TitleRequestSerializer, TitleResponseSerializer
from .title_generator import suggest_titles

class TitleSuggestionView(APIView):
    """
    POST /api/suggest-titles/
    {
      "content": "<blog post text…>"
    }
    ➔
    {
      "titles": ["…", "…", "…"]
    }
    """
    def post(self, request):
        req_ser = TitleRequestSerializer(data=request.data)
        if not req_ser.is_valid():
            return Response(req_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        content = req_ser.validated_data['content']
        try:
            suggestions = suggest_titles(content, n=3)
        except Exception as e:
            return Response(
                {"detail": f"Model error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        res_ser = TitleResponseSerializer({"titles": suggestions})
        return Response(res_ser.data, status=status.HTTP_200_OK)
