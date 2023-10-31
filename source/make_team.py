# 나중에 이름을 lobby_mode로 바꿀 예정
# 현재 기능: random으로 경기에 참여할 팀원 결정
# 투수 중 1명 타자 8명, 투수는 항상 player 리스트의 1번 요소일 것
import game_world
import random


def make_team():

    # 파란 팀
    l = len(game_world.hitter_player_list)

    # 투수 랜덤으로 정하기
    game_world.players.append(game_world.pitcher_player_list[random.randint(0, len(game_world.pitcher_player_list)-1)])

    # 타자 랜덤으로 정하기
    r = random.randint(0, l)
    for i in range(0, 9):
        game_world.players.append(game_world.hitter_player_list[(r + i) % l])


    # 빨간 팀
    # 투수 랜덤으로 정하기
    game_world.other_players.append(
        game_world.pitcher_player_list[random.randint(0, len(game_world.pitcher_player_list) - 1)])

    # 타자 랜덤으로 정하기
    r = random.randint(0, l)
    for i in range(0, 9):
        game_world.other_players.append(game_world.hitter_player_list[(r + i) % l])
