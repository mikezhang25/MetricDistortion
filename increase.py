from metric import *

x = []
y = []
div = []

""" Finds the metric with the lowest distortion and increment their weights by 1"""
def step(weights, plu, M):
    max_dist = 0
    max_metric = []
    min_dist = 99999999999999
    min_metric = []
    for metric in range(m):
        dist = distortion(metric, weights, plu, M)
        """
        if dist >= max_dist:
            if metric not in max_metric:
                max_metric.append(metric)
                div.append(len(x))
            max_dist = dist
        """
        if dist > max_dist:
            max_metric = [metric]
            max_dist = dist
        elif dist == max_dist:
            div.append(len(x))
            max_metric.append(metric)

        if dist < min_dist:
            min_metric = [metric]
            min_dist = dist
        elif dist == min_dist:
            div.append(len(x))
            min_metric.append(metric)

    x.append((len(x) + 1) * step_size / sum(weights))
    y.append(max_dist)
    print(max_metric, end="\t")
    print(max_dist)
    if len(max_metric) == m:
        return False
    # increment weights
    for metric in max_metric:
        weights[metric] += step_size / len(max_metric)
    for metric in min_metric:
        weights[metric] -= step_size / len(min_metric)
    return True

if __name__ == "__main__":
    # plu[i] = proportion of voters who ranked candidate i first
    # M[i][j] = proportion of voters who ranked i above j
    plu, M = paper_ex()
    # initialize weights w/ plurality count
    weights = [int(x * m) for x in plu]

    print('start')
    status = True
    for _ in range(100):
        """print("weights: ")
        for w_x in weights:
            print("%d" % w_x, end = " ")
        print()"""
        status = step(weights, plu, M)
        if not status:
            print("Equilibrium achieved")
            break

    plt.plot(y)
    for val in div:
        plt.axvline(x=val, color='r', linestyle='--')
    plt.ylabel('Worst Distortion')
    plt.show()

    # print out comparisons
    for row in range(m):
        print("[", end="")
        for col in range(m):
            print("%.2f" % M[row][col], end=" ")
        print("]")