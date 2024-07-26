import os, sys
import json, math

from pathlib import Path

import numpy as np
import cvxpy as cp


class ConfigNotFoundError(FileNotFoundError):
    pass


def generateConfig(configDir: str, config) -> bool:
    with open(configDir, "w", encoding="utf-8") as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)


def rewriteConfig(r: np.array, configDir: str, config) -> bool:
    for num, type in zip(r, config["资源"]):
        config["资源"][type][1] += int(num)
    with open(configDir, "w", encoding="utf-8") as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    try:
        with open("config.json", "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        config = {
            "角色": {
                "安卡希亚": {
                    "辉夜": {"资源": [0, 0, 0, 1, 0, 2, 0], "解锁": True},
                    "[不予显示]": {"资源": [0, 0, 1, 0, 0, 1, 0], "解锁": True},
                },
                "里芙": {
                    "无限之视": {"资源": [0, 1, 0, 0, 2, 0, 0], "解锁": True},
                    "狂猎": {"资源": [0, 1, 1, 0, 1, 0, 0], "解锁": True},
                    "星期三": {"资源": [1, 1, 0, 0, 0, 0, 0], "解锁": True},
                },
                "芙提雅": {
                    "缄默": {"资源": [0, 0, 1, 1, 0, 1, 0], "解锁": True},
                    "小太阳": {"资源": [0, 0, 0, 1, 0, 1, 0], "解锁": True},
                },
                "茉莉安": {
                    "雨燕": {"资源": [0, 2, 0, 0, 0, 1, 0], "解锁": True},
                    "绷带小姐": {"资源": [0, 1, 0, 0, 1, 0, 0], "解锁": True},
                },
                "晴": {
                    "藏锋": {"资源": [1, 0, 2, 0, 0, 0, 0], "解锁": True},
                    "旧日王牌": {"资源": [1, 0, 0, 0, 1, 0, 0], "解锁": True},
                },
                "琴诺": {
                    "悖谬": {"资源": [0, 1, 0, 0, 0, 0, 2], "解锁": True},
                    "双面": {"资源": [0, 0, 0, 0, 0, 0, 2], "解锁": True},
                },
                "芬妮": {
                    "辉耀": {"资源": [2, 0, 1, 0, 0, 0, 0], "解锁": True},
                    "咎冠": {"资源": [1, 0, 1, 0, 0, 0, 1], "解锁": True},
                    "黄金狮子": {"资源": [0, 0, 0, 0, 1, 0, 1], "解锁": True},
                },
                "肴": {
                    "冬至": {"资源": [0, 0, 0, 0, 1, 1, 1], "解锁": True},
                    "养生专家": {"资源": [0, 0, 0, 0, 1, 1, 0], "解锁": True},
                },
                "恩雅": {
                    "羽蜕": {"资源": [0, 2, 0, 1, 0, 0, 0], "解锁": True},
                    "姐姐大人": {"资源": [0, 1, 0, 1, 0, 0, 0], "解锁": True},
                },
                "猫汐尔": {
                    "溯影": {"资源": [0, 0, 0, 1, 0, 2, 0], "解锁": True},
                    "猫猫": {"资源": [0, 0, 0, 1, 0, 1, 0], "解锁": True},
                },
                "瑟瑞斯": {
                    "瞬刻": {"资源": [0, 0, 0, 2, 0, 0, 1], "解锁": True},
                    "小金鱼": {"资源": [0, 1, 0, 0, 0, 0, 1], "解锁": True},
                },
                "晨星": {
                    "云篆": {"资源": [2, 0, 0, 1, 0, 0, 0], "解锁": True},
                    "观测者": {"资源": [1, 0, 1, 0, 0, 0, 0], "解锁": True},
                },
                "凯茜娅": {"蓝闪": {"资源": [0, 0, 0, 0, 2, 0, 1], "解锁": True}},
                "伊切尔": {"豹豹": {"资源": [0, 0, 0, 2, 1, 0, 0], "解锁": True}},
                "苔丝": {"魔术师": {"资源": [0, 2, 0, 0, 0, 0, 1], "解锁": True}},
                "妮塔": {"四手": {"资源": [0, 0, 2, 0, 0, 0, 0], "解锁": True}},
            },
            "资源": {
                "皇冠": [20, 0],
                "花朵": [20, 0],
                "天平": [21, 0],
                "雪花": [20, 0],
                "子弹": [21, 0],
                "无限": [22, 0],
                "火焰": [20, 0],
            },
        }
        generateConfig(os.path.join(Path(sys.argv[0]).parent, "config.json"), config)
        raise ConfigNotFoundError("未找到config.json 已重新生成")

    characters = config["角色"]
    characterList = []
    resourceList = []
    unlockList = []
    totalList = np.zeros(
        7,
    )

    for character in characters:
        for armor in characters[character]:
            characterList.append([character, armor])
            resourceList.append(characters[character][armor]["资源"])
            unlockList.append(characters[character][armor]["解锁"])
            totalList += np.array(resourceList[-1])

    resource = config["资源"]
    requireList = []
    for type in resource:
        requireList.append(resource[type][0] - resource[type][1])

    n = len(characterList)

    c = np.ones(
        n,
    )
    a = np.transpose(np.array(resourceList))
    b = np.array(requireList, dtype=np.int64)
    eq = ~np.array(unlockList)
    a1 = np.full((n, n), 3)
    row, col = np.diag_indices_from(a1)
    a1[row, col] = -2
    b1 = np.zeros(
        n,
    )
    x = cp.Variable(n, integer=True)

    while True:
        objective = cp.Minimize(cp.sum(c * x * 1 / 3))
        constriants = [0 <= x, x <= 16, a * x >= b, eq * x == 0, a1 * x >= b1]
        prob = cp.Problem(objective, constriants)
        results = prob.solve(solver=cp.CPLEX)

        print("总计出战次数：", math.ceil(prob.value))
        ans = x.value

        for armor, times in zip(characterList, ans):
            if times != 0:
                print(armor, int(times))

        while True:
            confirm = input("进行下一次计算?确认/取消 y/n 默认为n:") or "n"
            if confirm == "n" or confirm == "N":
                exit()
            elif confirm == "y" or "Y":
                break
            else:
                continue

        r = np.zeros((7,), dtype=np.int64)
        while True:
            r[0] = input(f"本次皇冠掉落数，默认为{r[0]}:") or r[0]
            r[1] = input(f"本次花朵掉落数，默认为{r[1]}:") or r[1]
            r[2] = input(f"本次天平掉落数，默认为{r[2]}:") or r[2]
            r[3] = input(f"本次雪花掉落数，默认为{r[3]}:") or r[3]
            r[4] = input(f"本次子弹掉落数，默认为{r[4]}:") or r[4]
            r[5] = input(f"本次无限掉落数，默认为{r[5]}:") or r[5]
            r[6] = input(f"本次火焰掉落数，默认为{r[6]}:") or r[6]

            print(
                f"本次掉落为：\n皇冠:{r[0]}\n花朵:{r[1]}\n天平:{r[2]}\n雪花:{r[2]}\n子弹:{r[4]}\n无限:{r[5]}\n火焰:{r[6]}"
            )
            while True:
                confirm = input("确认/取消 y/n 默认为y:") or "y"
                if confirm == "y" or confirm == "Y":
                    b -= r
                    rewriteConfig(r, "config copy.json", config)
                    break
                elif confirm == "n" or confirm == "N":
                    break
                else:
                    continue
            if confirm == confirm == "y" or confirm == "Y":
                break
            else:
                continue
