
import { defineStore } from 'pinia';
import { User } from '../types/';

export const useUserStore = defineStore('user', {
    state: () => ({user: null as User | null}),
    actions: {
        setUser(user: User) {
            this.user = user;
            console.log("User set:", user);
        },
        async fetchUsers(){
            const response = await fetch('/api/user/', {
                method: 'GET',
            });
            this.user = await response.json();
            console.log(this.user); // remove, for tests
        },        
    }
});
