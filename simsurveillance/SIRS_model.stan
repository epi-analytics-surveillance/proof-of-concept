functions {
  real[] ode(real time, real[] state, real[] theta, real[] x_r, int[] x_i) {
    real S = state[1];
    real I = state[2];
    real R = state[3];
    real transmission_rate = theta[1];
    real recovery_rate = theta[2];
    real waning_rate = theta[3];
    real dSdt = -transmission_rate * S * I + waning_rate * R;
    real dIdt = transmission_rate * S * I - recovery_rate * I;
    real dRdt = recovery_rate * I - waning_rate * R;
    real dinfectionsdt = transmission_rate * S * I;
    return {dSdt, dIdt, dRdt, dinfectionsdt};
  }
}

data {
  int num_cases;
  int case_times[num_cases];
  real cases[num_cases];
  int num_prevalences;
  int prev_times[num_prevalences];
  int prev_as[num_prevalences];
  int prev_bs[num_prevalences];
  real N;
  int final_t;
}

transformed data {
  real x_r[0];
  int x_i[0];
  int t0 = 0;
  int ts[final_t];
  for(i in 1:final_t) {
    ts[i] = i;
  }
}

parameters {
  real<lower=0> transmission_rate;
  real<lower=0> recovery_rate;
  real<lower=0> waning_rate;
  real<lower=0.01, upper=0.99> case_ascertainment;
  real<lower=0> sigma;
  real<lower=1> num_init_infect;
}

transformed parameters {
  real y0[4];
  y0[1] = 1.0 - num_init_infect / N;
  y0[2] = num_init_infect / N;
  y0[3] = 0.0;
  y0[4] = num_init_infect / N;

  real y[final_t, 4];
  real prevalence[final_t];
  real cumulative_infections[final_t];
  real infections[final_t];

  real theta[3];
  theta[1] = transmission_rate;
  theta[2] = recovery_rate;
  theta[3] = waning_rate;
  
  y = integrate_ode_rk45(ode, y0, t0, ts, theta, x_r, x_i);
  prevalence = to_array_1d(col(to_matrix(y), 2));
  cumulative_infections = to_array_1d(col(to_matrix(y), 4));

  infections[1] = 0;
  for(i in 2:final_t) {
    infections[i] = N * (cumulative_infections[i] - cumulative_infections[i-1]);
  }
}

model {
  transmission_rate ~ gamma(0.25 * 1, 1);
  recovery_rate ~ gamma(0.125 * 1000, 1000);
  waning_rate ~ gamma(0.01 * 1000, 1000);
  sigma ~ inv_gamma(1, 1);
  case_ascertainment ~ uniform(0.05, 0.95);
  num_init_infect ~ uniform(1, 100);
  int j = 1;
  for(i in 1:final_t) {
    if(i == case_times[j]) {
      target += normal_lpdf(cases[j] | infections[i] * case_ascertainment, sigma);
      j += 1;
      if (j > num_cases) break;
    }
  }
  j = 1;
  for(i in 1:final_t) {
    if(i == prev_times[j]) {
      target += beta_lpdf(prevalence[i] | prev_as[j], prev_bs[j]);
      j += 1;
      if (j > num_prevalences) break;
    }
  }
}

generated quantities {
  real y_projection[final_t, 4];
  y_projection = y;
}

