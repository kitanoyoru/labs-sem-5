#include <iostream>
#include <unordered_set>

using namespace std;

bool is_primitive_element(int g, int p) {
    unordered_set<int> powers;
    int result = 1;

    for (int i = 1; i < p; i++) {
        result = (result * g) % p;
        powers.insert(result);
    }

    for (int i = 1; i < p - 1; i++) {
        if (powers.find(i) == powers.end()) {
            return false;
        }
    }

    return true;
}

int find_primitive_element(int p) {
    for (int g = 2; g < p; g++) {
        if (is_primitive_element(g, p)) {
            return g;
        }
    }

    return -1;
}

int main() {
    int p = 1877;
    int g = find_primitive_element(p);
    cout << "Primitive element GF(" << p << "): " << g << endl;

    int a_private_key = 1245;
    int A_public_key = 1;
    for (int i = 0; i < a_private_key; i++) {
        A_public_key = (A_public_key * g) % p;
    }

    int b_private_key = 756;
    int B_public_key = 1;
    for (int i = 0; i < b_private_key; i++) {
        B_public_key = (B_public_key * g) % p;
    }

    int shared_secret_Alice = 1;
    for (int i = 0; i < a_private_key; i++) {
        shared_secret_Alice = (shared_secret_Alice * B_public_key) % p;
    }

    int shared_secret_Bob = 1;
    for (int i = 0; i < b_private_key; i++) {
        shared_secret_Bob = (shared_secret_Bob * A_public_key) % p;
    }

    if (shared_secret_Alice == shared_secret_Bob) {
        cout << "A common secret: " << shared_secret_Alice << endl;
    } else {
        cout << "Shared secret calculation failed." << endl;
    }

    return 0;
}
