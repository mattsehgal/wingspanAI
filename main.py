from src.game import game_loop, player_prompter

players = player_prompter.Prompter().get_players()
game_loop.GameLoop(players).play()
