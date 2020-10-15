def check_message(message, pos):
    # 判断自己是不是第一手出牌
    if message['greaterPos'] == pos or message['greaterPos'] == -1:
        # 考虑如果对手的牌均大于5张的情况
        if message['publicInfo'][1]['rest'] > 5 and message['publicInfo'][3]['rest'] > 5:
            # 优先级1：顺子
            range = -1
            for own_choose_straight in message['actionList']:
                range += 1
                if own_choose_straight[0] == 'Straight':
                    # 遍历来判断顺子中的牌是否可拆
                    ok = 1;
                    for is_break_card in own_choose_straight[2]:
                        cnt = 0
                        # 遍历判断对子的情况
                        for own_check_pair in message['actionList']:
                            if own_check_pair[0] == 'Pair':
                                if is_break_card == own_check_pair[2][0] or is_break_card == own_check_pair[2][1]:
                                    cnt += 1
                        # 遍历判断三张的情况
                        for own_check_trips in message['actionList']:
                            if own_check_trips[0] == 'Trips':
                                if is_break_card == own_check_trips[2][0] or is_break_card == own_check_trips[2][
                                    1] or is_break_card == own_check_trips[2][2]:
                                    cnt += 1
                        if cnt > 2:
                            ok = 0
                            break
                        # 判断是否拆了炸弹
                        for own_check_bomb in message['actionList']:
                            if own_check_bomb == 'Bomb':
                                for own_check_bomb_factor in own_check_bomb[2]:
                                    if is_break_card == own_check_bomb_factor:
                                        ok = 0
                                        break
                        # 判断是否拆了同花顺
                        for own_check_flush in message['actionList']:
                            if own_check_flush == 'StraightFlush':
                                for own_check_flush_factor in own_check_flush[2]:
                                    if is_break_card == own_check_flush_factor:
                                        ok = 0
                                        break
                    if ok == 0:
                        continue
                    else:
                        message['indexRange'] = range
                        return message
            # 优先级2：小单张
            range = -1
            for own_choose_single in message['actionList']:
                range += 1
                if own_choose_single[0] == 'Single':
                    # 判断该单张是否可拆【下面两行效果不好】
                    # if own_choose_single[1] == '8' or '9' or '10' or 'A' or 'J' or 'Q' or 'K':
                    #    continue
                    ok = 1;
                    is_break_card = own_choose_single[2][0]
                    # 遍历判断对子的情况
                    for own_check_pair in message['actionList']:
                        if own_check_pair[0] == 'Pair':
                            if is_break_card == own_check_pair[2][0] or is_break_card == own_check_pair[2][1]:
                                ok = 0
                                break
                    # 遍历判断三张的情况
                    for own_check_trips in message['actionList']:
                        if own_check_trips[0] == 'Trips':
                            if is_break_card == own_check_trips[2][0] or is_break_card == own_check_trips[2][
                                1] or is_break_card == own_check_trips[2][2]:
                                ok = 0
                                break
                    # 判断是否拆了炸弹
                    for own_check_bomb in message['actionList']:
                        if own_check_bomb == 'Bomb':
                            for own_check_bomb_factor in own_check_bomb[2]:
                                if is_break_card == own_check_bomb_factor:
                                    ok = 0
                                    break
                    # 判断是否拆了同花顺
                    for own_check_flush in message['actionList']:
                        if own_check_flush == 'StraightFlush':
                            for own_check_flush_factor in own_check_flush[2]:
                                if is_break_card == own_check_flush_factor:
                                    ok = 0
                                    break
                    if ok == 0:
                        continue
                    else:
                        message['indexRange'] = range
                        return message
                        # 优先级3：对子
            range = -1
            for own_choose_pair in message['actionList']:
                range += 1
                if own_choose_pair[0] == 'Pair':
                    # 判断该牌是否可拆【下面两行效果不好】
                    # if own_choose_pair[1] == '8' or '9' or '10' or 'A' or 'J' or 'Q' or 'K':
                    #    continue
                    ok = 1;
                    is_break_card = own_choose_pair[2][0]
                    # 遍历判断三张的情况
                    for own_check_trips in message['actionList']:
                        if own_check_trips[0] == 'Trips':
                            if is_break_card == own_check_trips[2][0] or is_break_card == own_check_trips[2][
                                1] or is_break_card == own_check_trips[2][2]:
                                ok = 0
                                break
                    # 判断是否拆了炸弹
                    for own_check_bomb in message['actionList']:
                        if own_check_bomb == 'Bomb':
                            for own_check_bomb_factor in own_check_bomb[2]:
                                if is_break_card == own_check_bomb_factor:
                                    ok = 0
                                    break
                    # 判断是否拆了同花顺
                    for own_check_flush in message['actionList']:
                        if own_check_flush == 'StraightFlush':
                            for own_check_flush_factor in own_check_flush[2]:
                                if is_break_card == own_check_flush_factor:
                                    ok = 0
                                    break
                    if ok == 0:
                        continue
                    else:
                        message['indexRange'] = range
                        return message
                        # 优先级4：三张
            range = -1
            for own_choose_trips in message['actionList']:
                range += 1
                if own_choose_trips[0] == 'Trips':
                    # 判断该牌是否可拆
                    ok = 1;
                    is_break_card = own_choose_trips[2][0]
                    # 判断是否拆了炸弹
                    for own_check_bomb in message['actionList']:
                        if own_check_bomb == 'Bomb':
                            for own_check_bomb_factor in own_check_bomb[2]:
                                if is_break_card == own_check_bomb_factor:
                                    ok = 0
                                    break
                    # 判断是否拆了同花顺
                    for own_check_flush in message['actionList']:
                        if own_check_flush == 'StraightFlush':
                            for own_check_flush_factor in own_check_flush[2]:
                                if is_break_card == own_check_flush_factor:
                                    ok = 0
                                    break
                    if ok == 0:
                        continue
                    else:
                        message['indexRange'] = range
                        return message
    else:
        # 先判断现在要接哪一家的牌，如果是己家的，可以适当接手
        if message['greaterPos'] == (pos + 2) % 4:
            own_side_action = message['greaterAction'][0]
            own_side_point = message['greaterAction'][1]
            if own_side_action == 'Bomb':
                message['actionList'] = [['PASS', 'PASS', 'PASS']]
                message['indexRange'] = 0
            elif own_side_action == 'Single' or own_side_action == 'Pair' or own_side_action == 'Trips' or own_side_action == 'ThreeWithTwo':
                if own_side_point == 'J' or 'Q' or 'K' or 'A' or 'B' or 'R' or message['CurRank']:
                    message['actionList'] = [['PASS', 'PASS', 'PASS']]
                    message['indexRange'] = 0
            elif own_side_action == 'ThreePair' or own_side_action == 'TripsPair':
                if own_side_point == 'T' or 'J' or 'Q' or 'K' or 'A':
                    message['actionList'] = [['PASS', 'PASS', 'PASS']]
                    message['indexRange'] = 0
            elif own_side_action == 'Straight':
                if own_side_point == '8' or '9' or 'T' or 'J':
                    message['actionList'] = [['PASS', 'PASS', 'PASS']]
                    message['indexRange'] = 0
            elif own_side_action == 'StraightFlush':
                message['actionList'] = [['PASS', 'PASS', 'PASS']]
                message['indexRange'] = 0
            # 对选择完的牌型做进一步缩小范围
            for action_t in message['actionList']:
                if action_t[1] == own_side_action:
                    if int(action_t[2]) - own_side_point <= 2:
                        message['actionList'] = [action_t]
                        message['indexRange'] = 0
                        break
            else:
                message['actionList'] = [['PASS', 'PASS', 'PASS']]
                message['indexRange'] = 0

        else:
            pass
            # own_ops_action=message['greaterAction'][0]
            # own_ops_point=message['greaterAction'][1]
            # if own_ops_action=='Single':
            #     if int(own_ops_point):
            #         num=0
            #         for  action_l in message['actionList']:
            #             #手牌中的对子，三张拆与不拆
            #             # if action_l[0]=='Pair' and action_l[1]==own_ops_point:
            #             #     message['actionList'][num]=['PASS','PASS','PASS']
            #             # elif action_l[0]=='Trips' and action_l[1]==own_ops_point:
            #             #     message['actionList'][num]=['PASS','PASS','PASS']
            #             if action_l[0]=='Bomb' and action_l[1]==own_ops_point:
            #                 message['actionList'][num]=['PASS','PASS','PASS']

            #             num+=1
    return message