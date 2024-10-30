import numpy as np
import math

#input: current state = feedback
#output: optimal input

class MPPI():
    def __init__(
        self,
        horizon: int,
        dt: float,
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
        self.dt = dt
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

        self.total_steps = self.horizon / self.dt

    #ここにクリッピング入れる？それとも最後？
    def sampling(self, u_opt):
        mu = np.zeros(2,1)
        distributed_noise = np.random.multiveriate_normal(mu, self.sigma)
        input_series = u_opt + distributed_noise
        state_series = np.zeros(self.dim_state, self.total_steps)
        for i in range(self.total_steps):
            #you have to check the index
            state_series[i+1] = self.dynamics(input_series[i], state_series[i])

        return input_series, state_series

    def calc_cost(self, input_series, state_series):
        cost = 0
        #you have to check the num of loops
        for i in range(self.total_steps):
            cost += self.stage_cost(state_series[i])
        cost += self.terminal_cost(state_series[-1])
        return cost

    def calc_weight(self, cost, u_opt, input_series):
        sum = 0
        for i in range(self.total_steps):
            sum += u_opt[i].T * self.sigma.linalg.inv * input_series[i]
        weight = math.exp(-(cost / self.temp_lambda) - sum) / self.eta
        return weight

    def mppi(self):
        u_opt = 0
        input_series_array = np.zeros(2,self.total_steps, self.num_samples)
        weight_array = np.zeros(self.num_samples)

        for i in range(self.num_samples):
            input_series, state_series = self.sampling(u_opt)
            cost = self.calc_cost(input_series, state_series)
            weight = self.calc_weight(cost, u_opt, input_series)

            input_series_array[:, :, i] = input_series
            weight_array[i] = weight

        normalized_weight_array = weight_array / np.sum(weight_array)

        for i in range(self.num_samples):
            u_opt = normalized_weight_array[i] * input_series_array[:, :, i]
            


