#include<bits/stdc++.h>

using namespace std;

int soep(long long n, long long k)
{
    long long MOD = (long long)1e9 + 7;
    const int K = 100;
    vector<vector<long long>> combination(K + 10, vector<long long>(K + 10, -1));
    vector<long long> factorial(K + 10);
    vector<long long> bernoulli(K + 10);
    auto calc_combination = [&](auto calc_combination, long long n, long long k) -> long long {
        if (combination[n][k] != -1) {
            return combination[n][k];
        }

        if (k == 0 || n == k) {
            combination[n][k] = 1;
        } else if (k == 1) {
            combination[n][k] = n % MOD;
        } else {
            combination[n][k] = (calc_combination(calc_combination, n - 1, k - 1) + calc_combination(calc_combination, n - 1, k)) % MOD;
        }

        return combination[n][k];
    };

    for (int n = 0; n < K + 10; n++) {
        for (int k = 0; k <= n; k++) {
            combination[n][k] = calc_combination(calc_combination, n, k);
        }
    }

    factorial[0] = 1;
    for (int i = 1; i < K + 10; i++) {
        factorial[i] = (1ll * i * factorial[i - 1]) % MOD;
    }

    auto binary_mul = [&](long long a, long long b) -> long long {
        long long res = 1;
        a %= MOD;
        while (b) {
            if (b & 1) {
                res = (res * a) % MOD;
            }
            a = (a * a) % MOD;
            b >>= 1;
        }
        return res;
    };

    // (a / b) % MOD
    auto modular_div = [&](long long a, long long b) -> long long {
        if (a < 0) a = (a + MOD) % MOD;
        if (a >= MOD) a = a % MOD;
        return (a * (binary_mul(b, MOD - 2))) % MOD;
    };

    auto calc_bernoulli = [&](int m) -> long long {
        long long res = 0;
        for(int k = 0; k < m; k++) {
            long long res1 = (combination[m + 1][k] * bernoulli[k]) % MOD;
            res = (res + res1) % MOD;
        }
        res = (-1 * res + MOD) % MOD;
        res = modular_div(res, (m + 1));
        return res;
    };

    bernoulli[0] = 1;
    for (int i = 1; i < K + 9; i++) {
        bernoulli[i] = calc_bernoulli(i);
    }

    bernoulli[1] = modular_div(1, 2);

    auto calc_faulhaber_polynomial = [&](long long n, int p) -> long long {
        long long res = 0;
        for (int r = 0; r <= p; r++) {
            long long res1 = ((combination[p + 1][r] * bernoulli[r]) % MOD * binary_mul(n, p + 1 - r)) % MOD;
            res = (res + res1) % MOD;
        }
        res = modular_div(res, p + 1);
        return res;
    };

    return calc_faulhaber_polynomial(n, k);
}

int32_t main() {
    long long n, k;
    cin >> n >> k;
    cout << soep(n, k);

    return 0;
}