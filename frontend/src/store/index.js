import { createStore } from 'vuex';

export default createStore({
    state: {
        isLoggedIn: false
    },
    mutations: {
        login(state) {
        state.isLoggedIn = true;
        },
        logout(state) {
        state.isLoggedIn = false;
        },
        setLogin(state, user) {
            state.isLoggedIn = true;
            state.user = user; // 假设你想存储用户信息
            // 如果你使用 token，你可能还需要存储 token
            // state.token = user.token;
        },
    },
    actions: {
        login({ commit }) {
        commit('login');
        },
        logout({ commit }) {
        commit('logout');
        }
    },
    getters: {
        isLoggedIn: state => state.isLoggedIn
    }
});