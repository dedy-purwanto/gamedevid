from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        post = kwargs.pop('post')
        game = super(GameForm, self).save(commit = False)
        game.post = post
        game.save()
        return game
    class Meta:
        model = Game
        fields = (
            'image',
            'download_url',
            'developer',
            'release_date',
            'genre',
            'platform',
        
        )
