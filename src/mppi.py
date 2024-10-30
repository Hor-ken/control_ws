import numpy as np
import math

#input: current state = feedback
#output: optimal input

class MPPI():
    def __init__(
        self,
        horizon: int,
        num_samples: int,
        dim_state: int,
        dim_control: int,
        dynamics,
        stage_cost,
        terminal_cost,
        u_min,
        u_max,
        sigma, #matrix
        temp_lambda: float,
        eta: float
    ):
        self.horizon = horizon
        self.num_samples = num_samples
        self.dim_state = dim_state
        self.dim_control = dim_control
        self.dynamics = dynamics
        self.stage_cost = stage_cost
        self.terminal_cost = terminal_cost
        self.u_min = u_min
        self.u_max = u_max
        self.sigma = sigma
        self.temp_lambda = temp_lambda
        self.eta = eta

    #ここにクリッピング入れる？それとも最後？
    def sampling(self, u_opt):
        mu = np.zeros(2,1)
        distributed_noise = np.random.multiveriate_normal(mu, self.sigma)
        input_series = u_opt + distributed_noise
        state_series = np.zeros(self.dim_state, self.num_samples)
        for i in range(self.num_samples):
            #you have to check the index
            state_series[i+1] = self.dynamics(input_series[i], state_series[i])

        return input_series, state_series

    def calc_cost(self, input_series, state_series):
        cost = 0
        #you have to check the num of loops
        for i in range(self.num_samples):
            cost += self.stage_cost(state_series[i])
        cost += self.terminal_cost(state_series[-1])
        return cost

    def calc_weight(self, cost, u_opt, input_series):
        sum = 0
        for i in range(self.num_samples):
            sum += u_opt[i].T * self.sigma.linalg.inv * input_series[i]
        weight = math.exp(-(cost / self.temp_lambda) - sum) / self.eta
        return weight

