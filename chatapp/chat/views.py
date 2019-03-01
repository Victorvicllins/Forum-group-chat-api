from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from chat.models import User, Topic, Farm, Forum                                                  # Our Message model
from chat.serializers import FarmSerializer, ForumSerializer, UserSerializer, TopicSerializer # Our Serializer Classes
# Users View

class FarmList(generics.ListCreateAPIView):
	lookup_field = 'pk'
	serializer_class = FarmSerializer
	(permissions.IsAuthenticatedOrReadOnly,)

	def get_queryset(self):
		return Farm.objects.all()
    

class TopicList(generics.ListCreateAPIView):
	#lookup_field = 'pk'
	model = Topic
	serializer_class = TopicSerializer
	permissions_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def get_queryset(self):
		queryset = Topic.objects.all()
		topics = self.request.query_params.get('id')
		if topics:
			queryset = queryset.filter(farm=topics)
			return queryset
		return None

class ForumList(generics.ListCreateAPIView):
	#lookup_field = 'pk'
	model = Forum
	serializer_class = ForumSerializer
	permissions_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def get_queryset(self):
		queryset = Forum.objects.all()
		#topics = self.request.query_params.get('id')
		message = self.request.query_params.get('pk')  #messages

		if message:
			queryset = queryset.filter(topic_id=message)
			return queryset
		return None


class Register(generics.CreateAPIView):
    serializer_class = UserSerializer
    permissions_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        # Create new user
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        user = User.objects.create_user(email, first_name, last_name, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        token = Token.objects.create(user=user)
        return Response({'detail': 'User created with token ' + token.key})

'''
	class PassengerList(generics.ListCreateAPIView):
    model = Passenger
    serializer_class = PassengerSerializer

    # Show all of the PASSENGERS in particular WORKSPACE
    # or all of the PASSENGERS in particular AIRLINE
    def get_queryset(self):
        queryset = Passenger.objects.all()
        workspace = self.request.query_params.get('workspace')
        airline = self.request.query_params.get('airline')

        if workspace:
            queryset = queryset.filter(workspace_id=workspace)
        elif airline:
            queryset = queryset.filter(workspace__airline_id=airline)

        return queryset
'''