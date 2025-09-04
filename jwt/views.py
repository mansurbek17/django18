from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from .make_token import *

class ActorAll(APIView):
    def get(self, request):
        actor = Actor.objects.all()
        serializer = ActorSerializers(actor, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    
class ActorCreate(APIView):
    @swagger_auto_schema(request_body=ActorSerializers)
    def post(self, request):
        serializer = ActorSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
class ActorUpdate(APIView):
    @swagger_auto_schema(request_body=ActorSerializers)
    def put(self, request, pk):
        actor = get_object_or_404(Actor, pk=pk)
        serializer = ActorSerializers(actor, data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class ActorDelete(APIView):
    @swagger_auto_schema(request_body=ActorSerializers)
    def delete(self, request, pk):
        actor = get_object_or_404(Actor, pk=pk)
        actor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MovieAll(APIView):
    def get(self, request):
        movie = Movie.objects.all()
        serializer = MovieSerializers(movie, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class MovieCreate(APIView):
    @swagger_auto_schema(request_body=MovieSerializers)
    def post(self, request):
        serializer = MovieSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class MovieUpdate(APIView):
    @swagger_auto_schema(request_body=MovieSerializers)
    def put(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializers(movie, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
class MovieDelete(APIView):
    @swagger_auto_schema(request_body=MovieSerializers)
    def delete(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MoviesByYearView(APIView):
    def get(self, request, year):
        movies = Movie.objects.filter(year=year)
        serializer = MovieSerializers(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class MoviesByYearRangeView(APIView):
        def get(self, request):
            start_year = request.query_params.get('start')
            end_year = request.query_params.get('end')

            if not start_year or not end_year:
                return Response({"error": "start va end yillarni kiriting"}, status=status.HTTP_400_BAD_REQUEST)

            movies = Movie.objects.filter(year__range=(start_year, end_year))
            serializer = MovieSerializers(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
class MoviesWithLessActorsView(APIView):
    def get(self, request):
        movies = Movie.objects.annotate(actor_count=Count('actor')).filter(actor_count__lt=3)
        serializer = MovieSerializers(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommitMovieAll(APIView):
    def get(self, request):
        commit = CommitMovie.objects.filter(author=request.user)
        serializer = CommitMoviesSerializers(commit, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class CommitMovieCreate(APIView):
    @swagger_auto_schema(request_body=CommitMoviesSerializers)
    def post(self, request):
        response = {"success":True}
        serializer = CommitMoviesSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            response['data'] = serializer.data
            return Response(data=response)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
class CommitMovieUpdate(APIView):
    @swagger_auto_schema(request_body=CommitMoviesSerializers)
    def put(self, request, pk):
        commit = get_object_or_404(CommitMovie, pk=pk)
        serializer = CommitMoviesSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class CommitMovieDelete(APIView):
    @swagger_auto_schema(request_body=CommitMoviesSerializers)  
    def delete(self, request, pk):
        commit = get_object_or_404(CommitMovie, pk=pk)
        commit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Login(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.validated_data.get("username"))
        print (user)
        token = get_tokens_for_user(user)
        return Response(data=token, status=status.HTTP_200_OK)