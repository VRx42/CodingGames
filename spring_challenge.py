import sys
import math

def find_closer_index_ten(my_pacs_id, y, x, indexes_unused):
    distances = {}
    for i in indexes_unused:
        distances[str(i)] = abs(my_pacs_id['id{0}'.format(i)][0] - y) + abs(my_pacs_id['id{0}'.format(i)][1] - x)
    min_index = list(distances.keys())[list(distances.values()).index(min(distances.values()))]
    # print(min_index, file=sys.stderr)
    return(int(min_index))

def ft_blank(map_blank, height, width):
    for y in range(height):
        inner_list = []
        for x in range(width):
            inner_list.append('.')
        map_blank.append(inner_list)
    return(map_blank)

#renvoie la position des "0" adjacents i.e distance:diag=1 ou line=1
def is_o_around_1(y, x, map1):
    adjacency_1 = [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)]
    for dx, dy in adjacency_1:
        if (map1[y + dy][x + dx] == "o"):
            return((y + dy, x + dx))
    return(False)

# renvoie la position opposée aux pacmans amis ou ennemis en distance diag=1 ou line=2
adjacency_2_line = [(i,j) for i in (-2,0,2) for j in (-2,0,2) if not (i == j == 0)]
adjacency_3_line = [(i,j) for i in (-3,0,3) for j in (-3,0,3) if not (i == j == 0)]
adjacency_1_diag = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
list_pac_names = ['a0', 'a1', 'a2', 'a3', 'a4', 'e0', 'e1', 'e2', 'e3', 'e4']

def is_ae_around_2(y, x, map2, list_pacs_id):
    for dx, dy in adjacency_2_line + adjacency_1_diag + adjacency_3_line:
        if (map2[y + dy][x + dx] in list_pacs_id):
            return((y - dy, x - dx))
    return(False)

#CREATION DE la map_space(carte avec murs) et initialisation de la map_proba
width, height = [int(i) for i in input().split()]
map_space = []
for y in range(height):
    row = input()
    inner_list = list(row)
    map_space.append(inner_list)

#variable globale: donne les infos actualisées à chaque tour sur les points de la map
#pour donner la direction des pacs vers les points
map_pts_proba = []
ft_blank(map_pts_proba, height, width)

# for y in range(height):
#     print("PROBA:\t", *map_pts_proba[y], sep='', file=sys.stderr)

# GAME LOOP
while True:

    map_pts_new = []
    ft_blank(map_pts_new, height, width)
    
    # for y in range(height):
    #     print("debut tour\t\t", *map_pts[y], sep='', file=sys.stderr)

    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight

   #INITILATION DES PACS  amis + ennemis avece leurs attributs dans un dictionnaire
    a = 0
    e = 0
    my_pac_indexes, ennemy_pac_indexes = 0, 0
    my_pacs_id, ennemy_pacs_id = {}, {}
    for i in range(visible_pac_count):
        pac_id, mine, pos_x, pos_y, type_id, speed_turns_left, ability_cooldown = input().split()
        pac_id = int(pac_id)
        mine = mine != "0"
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        if (mine == True):
            my_pac_indexes += 1
            my_pacs_id['id{0}'.format(a)] = (pos_y, pos_x, 0, 0, pac_id, type_id, ability_cooldown)
            a += 1
        if (mine == False):
            ennemy_pac_indexes += 1
            ennemy_pacs_id['id{0}'.format(e)] = (pos_y, pos_x, 0, 0, pac_id, type_id, ability_cooldown)
            e += 1
        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)
    
    #ACTUALISATION POSITION ENNEMIE ET AMIE
    for y in range(height):
        for x in range(width):
            for key, value in ennemy_pacs_id.items():
                if (y == value[0] and x == value[1]):
                    map_pts_new[y][x] = "e" + str(key[2])
            for key, value in my_pacs_id.items():
                if (y == value[0] and x == value[1]):
                    map_pts_new[y][x] = "a" + str(key[2])

    visible_pellet_count = int(input())  # all pellets in sight
    # print("ICI:", visible_pellet_count, "\t\t", file=sys.stderr)
    still_ten = 0
    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(u) for u in input().split()]
        # décison de la direction simple: on va tous sur le premier (x,y) dont la value = 10
        if (value == 1):
            map_pts_new[y][x] = 'o'
        if (value == 10):
            map_pts_new[y][x] = '*'
            still_ten = 1

    for y in range(height):
        print("NEW X:\t\t", *map_pts_new[y], sep='', file=sys.stderr)

    #ACTUALISATION DE LA MAP PROBA OK
    for y in range(height):
        for x in range(width):
            if (map_pts_proba[y][x] != map_pts_new[y][x]):
                map_pts_proba[y][x] = map_pts_new[y][x]

    for y in range(height):
        print("PROBA:\t", *map_pts_proba[y], sep='', file=sys.stderr)

    #############################################################
    ## REGLES: vont des moins importantes aux plus importantes ##
    #############################################################

    #1ERE REGLE: aller aux pellets adjacents pour chacun des pacs
    for y in range(height):
        for x in range(width):
            for i in range(my_pac_indexes):
                if ((map_pts_new[y][x] == 'a{0}'.format(i)) and (is_o_around_1(y, x, map_pts_new) != False)):
                    target_y, target_x = is_o_around_1(y, x, map_pts_new)
                    my_pacs_id['id{0}'.format(i)] = (pos_y,
                                                    pos_x,
                                                    target_y,
                                                    target_x)

    #2E REGLE: on attribue aux valeurs 10 un PAC le plus proche
    # on y rentre que quand il y a encore des ten
    if (still_ten == 1):
        indexes_unused = {i for i in range(my_pac_indexes)}
        for y in range(height):
            for x in range(width):
                if (map_pts_new[y][x] == "*" and len(indexes_unused) > 0):
                    # print(map ,file=sys.stderr)
                    # print("la 10=", y, x, file=sys.stderr)
                    i = find_closer_index_ten(my_pacs_id, y, x, indexes_unused)
                    # print("index a retirer=", i, type(i),type(indexes_unused),"dans", indexes_unused ,file=sys.stderr)  
                    indexes_unused.remove(i)
                    # indexes_unused
                    # print("dans", indexes_unused ,file=sys.stderr)
                    my_pacs_id['id{0}'.format(i)] = (pos_y,
                                                    pos_x,
                                                    y, x)

    # 3E REGLE: éviter les collisions amies et ennemies (marche pas sur les cotés)
    # Genere ausi un peu d'aléatoire
    for y in range(height - 3):
        for x in range(width - 3):
            for i in range(my_pac_indexes):
                if ((map_pts_new[y][x] == 'a{0}'.format(i)) and (is_ae_around_2(y, x, map_pts_new, list_pac_names) != False)):
                    print("position de mon pac menacé", x, y, file=sys.stderr)
                    target_y, target_x = is_ae_around_2(y, x, map_pts_new, list_pac_names)

    # 4E REGLE: se transformer pour manger si jamais on est a coté d'un ennemi
    # list_pac_ennemies = ['e0', 'e1', 'e2', 'e3', 'e4']
    # for y in range(height):
    #     for x in range(width):
    #         for i in range(my_pac_indexes):
    #             if ((map_pts_new[y][x] == 'a{0}'.format(i))
    #             and (is_ae_around_2(y, x, map_pts_new, list_pac_ennemies) != False)
    #             and test_weakness_pacs(my_pacs_id['id{0}'.format(i)]
    #             ):
                    
    # SWITCH <pacId> <x> <y>
    # if(flag_speed == 1)
    #     res = ''
    #     for key_id, values in my_pacs_id.items():
    #         res += str("MOVE %s %d %d" % (key_id[2], values[3], values[2]))
    #         if (my_pac_indexes != 1):
    #             res += " | "
    #             my_pac_indexes -= 1
    #     print(res)

    # MOVE <pacId> <x> <y>
    res = ''
    for key_id, values in my_pacs_id.items():
        res += str("MOVE %s %d %d" % (key_id[2], values[3], values[2]))
        if (my_pac_indexes != 1):
            res += " | "
            my_pac_indexes -= 1
    print(res)


