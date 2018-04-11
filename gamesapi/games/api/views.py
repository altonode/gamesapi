from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import filterset
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter

from gamesapi.games.api.permissions import IsOwnerOrReadOnly
from gamesapi.users.models import User
from gamesapi.games.models import GameCategory
from gamesapi.games.models import Game
from gamesapi.games.models import Player
from gamesapi.games.models import PlayerScore
from gamesapi.games.api.serializers import UserSerializer
from gamesapi.games.api.serializers import GameCategorySerializer
from gamesapi.games.api.serializers import GameSerializer
from gamesapi.games.api.serializers import PlayerSerializer
from gamesapi.games.api.serializers import PlayerScoreSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
	
	
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'
    throttle_scope = 'game-categories'
    throttle_classses = (ScopedRateThrottle,)
    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name',)
	
	
class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'
    throttle_scope = 'game-categories'
    throttle_classses = (ScopedRateThrottle,)
	

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
    permission_classes = (
	    permissions.IsAuthenticatedOrReadOnly,
		IsOwnerOrReadOnly)
    filter_fields = (
	    'name',
		'game_category',
		'release_date',
		'played',
		'owner',
		)
    search_fields = (
	    '^name',
		)
    ordering_fields =  (
	    'name',
		'release_date',
		)
		
    def perform_create(self, serializer):
	    # Pass an additional owner field to the create method
		# To set the owner field to the user received in the request
        serializer.save(owner=self.request.user)
	

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    permission_classes = (
	    permissions.IsAuthenticatedOrReadOnly,
		IsOwnerOrReadOnly)
    
	
class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'
    filter_fields = (
	    'name',
		'gender',
		)
    search_fields = (
	    '^name',
		)
    ordering_fields = (
	    'name',
	    )
	
	
class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'
	
	
class PlayerScoreFilter(filterset.FilterSet):
    min_score = NumberFilter(name='score', lookup_expr='gte')
    max_score = NumberFilter(name='score', lookup_expr='lte')
    from_score_date = DateTimeFilter(name='score_date', lookup_expr='gte')
    to_score_date = DateTimeFilter(name='score_date', lookup_expr='lte')
    player_name = AllValuesFilter(name='player__name')
    game_name = AllValuesFilter(name='game__name')
	
	
    class Meta:
	    model = PlayerScore
	    fields = (
		    'score',
			'from_score_date',
			'to_score_date',
			'min_score',
			'max_score',
			#player__name will be accessed as player_name
			'player_name',
			#game__name will be accessed as game_name
			'game_name',
			)


class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name =  'playerscore-list'
    filter_class = PlayerScoreFilter
    ordering_fields = (
	    'score',
		'score_date',
		)	    
	
class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'
	
	
class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
	    return Response({
		    'players': reverse(PlayerList.name, request=request),
			'game-categories': reverse(GameCategoryList.name, request=request),
			'games': reverse(GameList.name, request=request),
			'scores': reverse(PlayerScoreList.name, request=request),
			'users': reverse(UserList.name, request=request),
		    })