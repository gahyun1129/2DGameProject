# 전역 변수 저장
attack_team = []
defence_team = []

ball = None
background = None

progress_bar = None
ui_inning = None
ui_ment = None
ui_judge = None
ui_hitter_info = None
ui_game_info = None
ui_mini_map = None

ui_ball_icon = None
ui_strike_icon = None

out_count = 0
cur_inning = 1
cur_inning_turn = 0 # 0이면 초, 1이면 말

user_score = 1
com_score = 0

cur_hitter = None
cur_pitcher = None

select_pitcher_num = 0
select_hitter_num = 0

team_element = []

selected_pitcher = None
selected_hitter = []

user_team_element = []

prev_list_page = 1
list_page = 1

user_page = 1
prev_user_page = 1

game_status = None
is_end = False

bgm = None

pitcher_ball = 0

gameMgr = None