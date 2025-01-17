<template>
    <div>
        <h3 class="white-text" id="title">Users with Similar Hobbies</h3>

        <div class="filters">
            <label class="white-text">
                Min Age:
                <input type="number" v-model.number="minAge" id="minAge"/>
            </label>

            <label class="white-text">
                Max Age:
                <input type="number" :value="maxAge" v-model.number="maxAge" id="maxAge"/>
            </label>

            <button @click="applyFilters" id="filterButton">Filter</button>
        </div>

        <ul>
            <li v-for="user in users" :key="user.id" class="white-text" id="username">
                {{ user.username }} - Shared Hobbies: {{ user.shared_hobbies }}
                <button @click="sendFriendRequest(user.id)">Send Friend Request</button>
            </li>
        </ul>

        <!-- Feedback message -->
        <p v-if="message" class="feedback">{{ message }}</p>

        <div class="pagination">
            <button @click="prevPage" :disabled="page === 1">Previous</button>
            <span>Page {{ page }}</span>
            <button @click="nextPage" :disabled="!hasMore">Next</button>
        </div>
  </div>
</template>
  
<script lang="ts">
    import {ref, onMounted} from 'vue';
    import { User } from '../types';

export default {
    setup() {
        const users = ref<User[]>([]);
        const page = ref(1);
        const perPage = 10;
        const hasMore = ref(true);
        const minAge = ref<number | null>(null);
        const maxAge = ref<number | null>(null);
        const message = ref(''); // To store feedback from the backend

        const fetchSimilarUsers = async () => {
            try {
                const params = new URLSearchParams();
                params.append('page', page.value.toString());
                if (minAge.value !== null) params.append('min_age', minAge.value.toString());
                if (maxAge.value !== null) params.append('max_age', maxAge.value.toString());

                const response = await fetch(`/api/similar-users/?${params.toString()}`, {
                    credentials: 'include',
                });

                const data = await response.json();
                console.log(data)
                users.value = data.users;
                hasMore.value = data.total > page.value * perPage;
            } catch (error) {
                console.error('Error fetching similar users:', error);
            }
        };

        const sendFriendRequest = async (userId: number) => {
            try {
                const response = await fetch('/api/send-friend-request/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken(),
                    },
                    body: JSON.stringify({ id: userId }),
                    credentials: 'include',
                });

                const data = await response.json();

                if (response.ok) {
                    message.value = 'Friend request sent successfully!';
                } else {
                    message.value = data.error || 'An error occurred while sending the friend request.';
                }
            } catch (error) {
                console.error('Error sending friend request:', error);
                message.value = 'Something went wrong. Please try again later.';
            }
        };

        const getCsrfToken = () => {
            const cookieValue = document.cookie
                .split('; ')
                .find(row => row.startsWith('csrftoken='))
                ?.split('=')[1];
            return cookieValue || '';
        };

        const applyFilters = () => {
            page.value = 1; // Reset page to 1
            fetchSimilarUsers(); // Fetch data with the new filters
        };

        const nextPage = () => {
        if (hasMore.value) {
            page.value += 1;
            fetchSimilarUsers();
        }
        };

        const prevPage = () => {
        if (page.value > 1) {
            page.value -= 1;
            fetchSimilarUsers();
        }
        };

        onMounted(() => {
            fetchSimilarUsers();
        });

        return {
            users,
            page,
            hasMore,
            nextPage,
            prevPage,
            minAge,
            maxAge,
            fetchSimilarUsers,
            applyFilters,
            sendFriendRequest,
            message,
        };
    },
    };
</script>

<style scoped>
    .pagination {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
    }
    
    .white-text, .feedback {
        color: white;
        padding: 5px;
    }

    .filters{
        margin: 10px;
    }

    #title{
        margin: 10px;
    }

    #username{
        padding: 5px;
    }
</style>
  