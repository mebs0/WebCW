<template>
    <main class="container pt-4 ">
        <div>
            <router-link :to="{name: 'Main Page'}" id="bar" class="profilePage">Profile Page</router-link> |
            <router-link :to="{name: 'Other Page'}" id="bar" class="otherUsers">Other Users</router-link> |
            <router-link :to="{name: 'Friends Page'}" id="bar" class="friendsPage">Friends Page</router-link>
            <span v-if="isStaff"> | <a href="/admin/" class="text-decoration-underline" id="bar">Admin Panel</a></span>|
            <span><a href="/logout/" class="text-decoration-underline" id="bar">Logout</a></span>
        </div>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
    import { defineComponent, ref, onMounted } from "vue"; 
    import { RouterView} from "vue-router";


    export default defineComponent({
    components: { RouterView },
    setup() {
        const isStaff = ref(false);

        async function checkstaff() {
            const response = await fetch('/api/user/', { method: 'GET' });
            if (response.ok) {
                const data = await response.json();
                isStaff.value = data.isstaff;
            } 
        }
        onMounted(() => {
            checkstaff();
        });

        return {isStaff};
    }
});
</script>


<style scoped>
    #bar {
        color: white;
        text-decoration: none;
        padding: 0.2rem 1rem;
        border: solid white 0.5px;
        border-radius: 5px;
    }

    #bar:hover {
        color: #ccc;
        text-decoration: underline;
    }

</style>
