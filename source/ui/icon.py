from pico2d import load_image, draw_rectangle
import game_framework
import mode.attack_mode as attack_mode
import game_world
import server
import mode.lobby_mode as lobby_mode
import module.list_element as list_element
from module import make_team
import copy


class Icon:
    def __init__(self, image_name, name, x, y):
        self.image = load_image('resource/image/' + image_name + '.png')
        self.x, self.y = x, y
        self.name = name

    def get_bb(self):
        return self.x - 17, self.y - 17, self.x + 17, self.y + 17

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 35, 35)
        draw_rectangle(*self.get_bb())

    def handle_collide(self):
        match self.name:
            case 'next_page':
                server.prev_list_page = server.list_page
                server.list_page += 1
                lobby_mode.draw_list(server.team_element, 210)
            case 'user_next_page':
                server.prev_list_page = server.list_page
                server.list_page += 1
                lobby_mode.draw_list(server.user_team_element, 600)
            case 'prev_page':
                server.prev_list_page = server.list_page
                server.list_page -= 1
                lobby_mode.draw_list(server.team_element, 210)
            case 'user_prev_page':
                server.prev_list_page = server.list_page
                server.list_page -= 1
                lobby_mode.draw_list(server.user_team_element, 600)
            case 'pitcher_ok':
                # 투수 추가 하기
                server.user_team_element.append(list_element.Element('투수', server.selected_pitcher))
                server.user_team_element[0].set_x_y(600, 430)
                game_world.add_object(server.user_team_element[0], 3)

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
                    game_world.add_object(server.team_element[x], 2)

                self.name = 'hitter_ok'
            case 'hitter_ok':
                print('hitter_ok')
                server.user_team_element.clear()
                server.user_team_element.append(list_element.Element('투수', server.selected_pitcher))
                for o in server.selected_hitter:
                    print(o.name)
                    server.user_team_element.append(list_element.Element('타자', o))

                lobby_mode.draw_list(server.user_team_element, 600)

                if server.select_hitter_num == 9:
                    team_list_ok_icon = Icon('ok_icon', 'user_ok', 740, 50)
                    game_world.add_object(team_list_ok_icon, 2)
                    game_world.remove_object(self)

            case 'user_ok':
                for o in server.user_team_element:
                    make_team.user_players.append(copy.copy(o.player))
                game_framework.change_mode(attack_mode)
