# 나중에 이름을 lobby_mode로 바꿀 예정
# 현재 기능: random으로 경기에 참여할 팀원 결정
# 투수 중 1명 타자 8명, 투수는 항상 player 리스트의 1번 요소일 것
import game_world
import random

def make_team():
    game_world.player.append(game_world.pitcher_player_list[random.randint(0, len(game_world.pitcher_player_list)-1)])
    for _ in range(0, 8):
        game_world.player.append(
            game_world.hitter_player_list[random.randint(0, len(game_world.hitter_player_list) - 1)])

    for p in game_world.player:
        print(p.name)