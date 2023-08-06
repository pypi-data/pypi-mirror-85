def repay_plan_factory(repay_type):
    if repay_type == "等额本息":
        return gen_repay_plan_fixed_prin_int
    elif repay_type == "等额本金":
        return gen_repay_plan_fixed_prin
    elif repay_type == "等本等息":
        return gen_repay_plan_fixed_prin_fixed_int
    else:
        return None


def gen_repay_plan_fixed_prin_int(principal, monthly_rate, n_periods):
    prin_remain = principal
    plan = []
    repay_per_month = principal * monthly_rate * (1 + monthly_rate) ** n_periods / ((1 + monthly_rate) ** n_periods - 1)
    for i in range(0, n_periods):
        cur_int = round(prin_remain * monthly_rate, 2)
        cur_prin = round(repay_per_month - cur_int, 2)
        prin_remain -= cur_prin
        plan.append([cur_prin, cur_int])
    plan[-1][0] = round(principal - sum([_[0] for _ in plan])+plan[-1][0],2)
    plan[-1][1] = round(repay_per_month - plan[-1][0], 2)
    return plan


def gen_repay_plan_fixed_prin(principal, monthly_rate, n_periods):
    prin_remain = principal
    plan = []
    prin_per_month = round(principal / n_periods, 2)
    for i in range(0, n_periods):
        _ = prin_remain * monthly_rate
        prin_remain -= prin_per_month
        plan.append([prin_per_month, round(_, 2)])
    plan[-1][0] = round(principal - sum([_[0] for _ in plan]) + plan[-1][0], 2)
    return plan


def gen_repay_plan_fixed_prin_fixed_int(principal, monthly_rate, n_periods):
    plan = []
    for i in range(0, n_periods):
        plan.append([round(principal / n_periods, 2), round(principal * monthly_rate, 2)])
    plan[-1][0] = round(principal - sum([_[0] for _ in plan]) + plan[-1][0], 2)
    return plan
