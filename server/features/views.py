from concurrent.futures import thread
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from features.serializers import NewGroupSerializer
from .models import Thread, NewGroup
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.core.serializers import serialize
from django.http import JsonResponse


from features.serializers import CustomRegistrationSerializer, ThreadSerializer
from features.models import User


class CustomRegistration(generics.GenericAPIView):
    serializer_class = CustomRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,  status= status.HTTP_200_OK)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        print(request.data)
        users = User.objects.all()
        serializer = CustomRegistrationSerializer(users, many = True)
        return Response(serializer.data)

    def put(self, request, pk):
        user_obj = User.objects.get(pk = pk)
        serializer = CustomRegistrationSerializer(user_obj, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            print("Serailizer data", serializer.data)
            return Response(serializer.data,  status= status.HTTP_200_OK)
        print("Error", serializer.errors)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


class CustomLogin(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):

        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        print("Ayo", user)
        if not user:
            return Response({"result": {"token": None}}, status= status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"result": {'token': token.key, 'username': user.username,
                            "id": user.id,
                            'created': token.created,
                            'is_admin': user.is_staff
        } })
        

class NewGroupView(generics.GenericAPIView):
    serializer_class = NewGroupSerializer
    # permission_classes = (IsAuthenticated,)


    def post(self, request, *args, **kwargs): 
        print("Dayta", request.data)
        serializer = self.get_serializer(data = request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            print("Serailizer data post", serializer.data)
            return Response(serializer.data,  status= status.HTTP_200_OK)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
    

        user_id = self.kwargs.get('userfk', None)
        print('user id', user_id)

        groups = NewGroup.objects.filter(user_fk = user_id)
        serializer = NewGroupSerializer(groups, many = True)

        return Response(serializer.data)


class ThreadView(generics.GenericAPIView):

    serializer_class = ThreadSerializer
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs): 


        print("Dayta", request.data)
        serializer = self.get_serializer(data = request.data)

        user1 = request.data['user1']
        user2 = request.data['user2']

        print("views user1", user1)
        print("views user2", user2)
      

        lookup1 = Q(user1=user1) & Q(user2=user2)
        lookup2 = Q(user1=user2) & Q(user2=user1)
        print("lookup1", lookup1)
        print("lookup2", lookup2)
        lookup = Q(lookup1 | lookup2)


        qs = Thread.objects.filter(lookup)
        print("Qs", qs)
        print("Qs first", qs.first())

        
        if qs.exists():
            existing = qs.first()
            return Response(ThreadSerializer(existing).data, status=status.HTTP_200_OK)
        
        if serializer.is_valid():
            
            serializer.save()
            print("Serailizer data post", serializer.data)
            return Response(serializer.data,  status= status.HTTP_200_OK)
        else:
            print("Error", serializer.errors)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def messages_view(request, userid):
    user = User.objects.get(id = userid)
    threads = Thread.objects.by_user(user = user).prefetch_related('chatmessage_thread').order_by('timestamp')

    threads_json = serialize("json", threads)

    print("Threads in view", threads_json)

    return JsonResponse({'result': {'Threads': threads_json}},  status= status.HTTP_200_OK)