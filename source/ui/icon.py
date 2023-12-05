from pico2d import load_image, draw_rectangle
import game_framework
import mode.attack_mode as attack_mode
import game_world
import server
import mode.lobby_mode as lobby_mode
import mode.result_mode as result_mode
import module.list_element as list_element
from module import make_team
import copy


class Icon:
    def __init__(self, image_name, name, x, y, size_x=35, size_y=35):
        self.image = load_image('resource/image/' + image_name + '.png')
        self.x, self.y = x, y
        self.name = name
        self.is_draw = True
        self.size_x, self.size_y = size_x, size_y

    def get_bb(self):
        return self.x - self.size_x // 2, self.y - self.size_y // 2, self.x + self.size_x // 2, self.y + self.size_y // 2

    def update(self):
        pass

    def draw(self):
        if self.is_draw:
            self.image.draw(self.x, self.y, self.size_x, self.size_y)
            # draw_rectangle(*self.get_bb())

    def handle_collide(self):
        match self.name:
            case 'next_page':
                server.prev_list_page = server.list_page
                server.list_page += 1
                lobby_mode.draw_list(server.team_element, 210)
            case 'prev_page':
                server.prev_list_page = server.list_page
                server.list_page -= 1
                lobby_mode.draw_list(server.team_element, 210)
            case 'user_next_page':
                server.prev_user_page = server.user_page
                server.user_page += 1
                lobby_mode.draw_list_user(server.user_team_element, 600)
            case 'user_prev_page':
                server.prev_user_page = server.user_page
                server.user_page -= 1
                lobby_mode.draw_list_user(server.user_team_element, 600)
            case 'pitcher_ok':
                # 투수 추가 하기
                server.user_team_element.append(list_element.Element('투수', server.selected_pitcher))
                server.user_team_element[0].set_x_y(600, 430)
                game_world.add_object(server.user_team_element[0], 1)

                # 투수 element 삭제 하기
                for x in range((server.list_page - 1) * 4, server.list_page * 4):
                    game_world.remove_object(server.team_element[x])

                server.list_page = 1
                server.team_element.clear()

                # 타자 element 만들기
                # 타자 목록 읽기
                server.team_element = [list_element.Element('타자', p) for p in make_team.hitters]

                for x in range((server.list_page - 1) * 4, server.list_page * 4):
                    server.team_element[x].set_x_y(210, 430 - x * 100)
                    game_world.add_object(server.team_element[x], 0)

                self.name = 'hitter_ok'
            case 'hitter_ok':
                server.user_team_element.clear()
                server.user_team_element.append(list_element.Element('투수', server.selected_pitcher))
                # hitter list에서 선택 중
                for o in server.selected_hitter:
                    server.user_team_element.append(list_element.Element('타자', copy.copy(o)))

                lobby_mode.draw_list_user(server.user_team_element, 600)

                if server.select_hitter_num == 9:
                    team_list_ok_icon = Icon('ok_icon', 'user_ok', 740, 50)
                    game_world.add_object(team_list_ok_icon, 0)
                    game_world.remove_object(self)

            case 'user_ok':
                # 팀 구성 완료
                for o in server.user_team_element:
                    player = copy.copy(o)
                    player.set_team_color('파랑')
                    make_team.user_players.append(player)
                game_framework.change_mode(attack_mode)

            case 'exit':
                server.game_status = 'quit'
                game_framework.pop_mode()

            case 'retry':
                game_framework.change_mode(lobby_mode)

            case 'stop':
                server.game_status = 'stop'
                game_framework.pop_mode()
            case 'ball':
                if self.is_draw:
                    server.ui_ball_icon.is_draw = False
                    server.ui_strike_icon.is_draw = False
                    server.cur_pitcher.state_machine.handle_event(('PLAY_NOW', 'ball'))
            case 'strike':
                if self.is_draw:
                    server.ui_ball_icon.is_draw = False
                    server.ui_strike_icon.is_draw = False
                    server.cur_pitcher.state_machine.handle_event(('PLAY_NOW', 'strike'))
