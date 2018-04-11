from rest_framework import serializers

from gamesapi.users.models import User
from gamesapi.games.models import GameCategory
from gamesapi.games.models import Game
from gamesapi.games.models import Player
from gamesapi.games.models import PlayerScore
from gamesapi.games.api import views

class GameCategorySerializer(serializers.HyperlinkedModelSerializer):
    games = serializers.HyperlinkedRelatedField(
	    many=True,
		read_only=True,
		view_name='game-detail')
	
	
    class Meta:
	    model = GameCategory
	    fields = (
		    'url',
			'pk',
			'name',
			'games')

class GameSerializer(serializers.HyperlinkedModelSerializer):
    # Display the owner username (read-only)
	owner = serializers.ReadOnlyField(source='owner.username')
	# Display the game category's name instead of the id
	game_category = serializers.SlugRelatedField(
	    queryset=GameCategory.objects.all(),
		slug_field='name')
	
		
	class Meta:
	    model = Game
	    depth = 4
	    fields = ('url',
		          'owner',
                  'name',
                  'release_date',
                  'game_category',
                  'played')


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    # Display all the details for the game
	game = GameSerializer()
	
	
	# Player field excluded as game is nested in the player
	class Meta:
	    model = PlayerScore
	    fields = (
		    'url',
			'pk',
			'score',
			'score_date',
			'game',
		    )
			

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    scores = ScoreSerializer( many=True, read_only=True)
    gender = serializers.ChoiceField(
	    choices=Player.GENDER_CHOICES)
    gender_description = serializers.CharField(
	    source='get_gender_display',
		read_only=True)
	
	
    class Meta:
	    model = Player
	    fields = (
		'url',
		'name',
		'gender',
		'gender_description',
		'scores',
		)
		

class PlayerScoreSerializer(serializers.ModelSerializer):
    # Display the name instead of the id
	player = serializers.SlugRelatedField(
	    queryset=Player.objects.all(),
		slug_field='name')
	game = serializers.SlugRelatedField(
	    queryset=Game.objects.all(),
		slug_field='name')
	
	
	class Meta:
	    model = PlayerScore
	    fields = (
		'url',
		'pk',
		'score',
		'score_date',
		'player',
		'game',
		)


class UserGameSerializer(serializers.HyperlinkedModelSerializer):
    
	
	class Meta:
	    model = Game
	    fields = (
		    'url',
			'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    games = UserGameSerializer(many=True, read_only=True)
	
	
    class Meta:
	    model = User
	    fields = (
		    'url',
			'pk',
			'username',
			'games')