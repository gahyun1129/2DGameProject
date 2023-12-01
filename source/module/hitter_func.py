import game_framework
import server
import game_world
from mode import defence_mode, attack_mode
from module import make_team


def set_next_hitter(hitter):
    hitter.strike, hitter.ball = 0, 0
    make_team.search_next_hitter(hitter)
    if server.out_count == 3:
        out_situation()


def out_situation():
    server.out_count = 0
    server.cur_inning_turn += 1
    if server.cur_inning_turn == 0:
        server.cur_inning += 1
    if server.cur_inning == 10:
        print('게임 끝')
        pass # 나중에 여기서 결과 모드로 바꾸면 될 듯
    server.ui_inning.frame = server.cur_inning - 1
    if server.cur_inning_turn == 0:
        server.ui_inning.turn = 3
        game_framework.change_mode(defence_mode)
    else:
        server.ui_inning.turn = 2
        game_framework.change_mode(attack_mode)


def after_hit(hitter, hit):
    if hit > 1:   # hit 성공
        hitter.frame = hitter.frame + 1
        if hitter.frame == 4:                                                       # 배트 돌리는 장면의 frame: 4
            game_world.update_handle_event(('HIT_SUCCESS', 0))                      # 공과 수비수들은 각자의 자리를 향해 뜀
            server.ui_ment.draw_ment_ui('hit')                                      # hit ui 출력
        if hitter.frame == hitter.frame_number:
            hitter.state_machine.handle_event(('HIT_SUCCESS', 0))                   # 타자는 1루를 향해 뜀
    elif hit > 0.4:  # ball의 경우
        hitter.ball += 1                                                            # ball 개수 추가
        server.ui_ment.draw_ment_ui('ball', hitter.ball)                            # ball ui 출력
        if hitter.ball == 4:                                                        # 4 ball인 경우
            hitter.state_machine.handle_event(('FOUR_BALL', 0))                     # 타자는 1루를 향해 뜀
            pass                                                                    # 뛰어야 할 주자가 있다면, 뜀
        hitter.state_machine.handle_event(('HIT_FAIL', 0))
    else:  # strike의 경우
        hitter.strike += 1                                                          # strike 개수 추가
        server.ui_ment.draw_ment_ui('strike', hitter.strike)                        # strike ui 출력
        if hitter.strike == 3:                                                      # 3 스트라이크인 경우
            server.out_count += 1
            server.ui_judge.draw_judge_ui('out', server.out_count)                  # 아웃 ui 출력
            set_next_hitter(hitter)  # 현재 타자 삭제 후 다음 타자 렌더링
        hitter.state_machine.handle_event(('HIT_FAIL', 0))