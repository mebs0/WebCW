<template>
  <div></div>
  <!-- This code lays out the profile section for the user, showing their profile and all hobbys
   They are then able to alter their profile, add and remove hobbies -->
  <div class="bg-dark text-white">

    <div class="row">
      <!-- Profile section, Used to view and update the profile -->
      <div class="col">
        <h1>My Personal Details</h1>
        <form @submit.prevent="PUTuser">
          <div class="mb-1">
            <label>Full Name</label><input type="text" v-model="pform.profile_name" class="form-control" id="enter_name" /></div>
          <div class="mb-1">
            <label>UserName</label><input type="text" v-model="pform.profile_username" class="form-control" id="enter_username" />
          </div>
          <div class="mb-1">
            <label>Email Adress</label><input type="email" v-model="pform.profile_email" class="form-control" id="enter_email"/></div>
          <div class="mb-4">
            <label>D.O.B</label><input type="date" v-model="pform.profile_dob" class="form-control" id="enter_dob" /></div>
          <h5>Change Password</h5>
          <div class="mb-1">
            <label>Current Password</label><input type="password" placeholder="Blank = No Password Change" v-model="pform.profile_old_pass" class="form-control" id="enter_old_pass" /></div>
          <div class="mb-2">
            <label>New Password</label><input type="password" placeholder="Blank = No Password Change" v-model="pform.profile_new_pass" class="form-control"  id="enter_new_pass"/></div>
          <button type="submit" class="btn btn-primary" id="update_button">Update</button>
        </form>
      </div>

      <!-- This Section shows the users added hobbies, they are able to remove hobbies here to via inline delete button -->
      <div class="col">
        <h1>My Hobbies</h1>
        <ul class="list-group" v-if="user">
          <li class="list-group-item d-flex justify-content-between align-items-center"v-for="hobby in user.hobbies" :key="hobby[0]">
            {{ hobby[1] }}
            <button @click="DELhobby(hobby[0])" class="btn btn-danger">Delete Hobby</button>
          </li>
        </ul>

        <!--This Section Is For the user to be able to add a hobby via a dropdown, filtered so only hobbies not added can be selected-->
        <h3>Select A Hobby You Like</h3>
        <form @submit.prevent="POSTuserhobby">
          <select v-model="selectedNewHobby" class="form-select mb-1" required>
            <option disabled value=""></option>
            <option v-for="hobby in hobbynotadded" :key="hobby.id" :value="hobby.id">{{ hobby.name }}</option>
          </select>
          <button type="submit" class="btn btn-primary" id="select_hobby">Select Hobby</button>
        </form>
      </div>

      <!-- This section shows all the hobbies that are in the system -->
      <div class="col">
        <h1>All Hobbies</h1>
        <ul class="list-group"><li class="list-group-item" v-for="hobby in hobbybank" :key="hobby.id">{{ hobby.name }}</li></ul>

        <!--This section allows the user to enter a new hobby,(reflected to all the users)-->
        <div class="mt-4">
          <h3>Add a New Hobby</h3>
          <form @submit.prevent="POSThobby">
            <div class="mb-1"><input type="text" v-model="hobbytoadd" class="form-control" required /></div>
            <button type="submit" class="btn btn-primary" id="new_hobby">Add Hobby</button>
          </form>
        </div>
      </div>


    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent } from 'vue';
import { User, Hobby } from '../types'; // gets our interfaces
import { useUserStore } from '../stores/user'; // imports our user store

export default defineComponent({
  data() {
    return {
      // user taken from inteface in types
      user: null as User | null,
      // profile form + helper variables
      pform: { profile_name: '', profile_username: '', profile_email: '', profile_dob: '', profile_old_pass: '',profile_new_pass: '' },
      selectedHobbies: [] as number[], hobbybank: [] as Hobby[],
      hobbytoadd: '', selectedNewHobby: '',
    };
  },
  computed: {
    // used to return any hobbies that we do not have added
    hobbynotadded(): Hobby[] { 
      return this.hobbybank.filter((hobby) => !this.selectedHobbies.includes(hobby.id));},

      // method for csfr extraction
    extractcsrfToken(): string {
      const cookies = document.cookie.split('; ');
      const csrfCookie = cookies.find((cookie) => cookie.startsWith('csrftoken='));
      return csrfCookie ? csrfCookie.split('=')[1] : '';
    },
  },

  async mounted() { // initial data fetch
    this.GETuser();
    this.GEThobby();
  },

  methods: {

    async GETuser() { // used to get the user information
      const store = useUserStore();
      await store.fetchUsers(); // get the initial user information from the store
      if (store.user) {
        this.pform.profile_name = store.user.name;
        this.pform.profile_username = store.user.username;
        this.pform.profile_email = store.user.email;
        this.pform.profile_dob = store.user.date_of_birth;
        this.selectedHobbies = store.user.hobbies.map((hobby) => hobby[0]);

        this.user = store.user;
      }
    },

    // This method updates the user profile when you add a change
    async PUTuser() {
      const newfields: any = {
        name: this.pform.profile_name,
        username: this.pform.profile_username,
        email: this.pform.profile_email,
        date_of_birth: this.pform.profile_dob,
      };

      // only passes passwords if both aree filled, (my backend api checks this)
      if (this.pform.profile_old_pass && this.pform.profile_new_pass) {
        newfields.old_password = this.pform.profile_old_pass;
        newfields.new_password = this.pform.profile_new_pass;
      }
      const api_response = await fetch('/api/user/', {method: 'PUT',headers: {'Content-Type': 'application/json','X-CSRFToken': this.extractcsrfToken,},
        body: JSON.stringify(newfields),
      });

      const data = await api_response.json();
      if (api_response.ok) {
        this.GETuser();
        const store = useUserStore();
        store.setUser(data); // update the store
        } 
      else {alert(JSON.stringify(data));}

    },

    // this method gets all the hobbies
    async GEThobby() {
      const api_response = await fetch('/api/hobbies/', {method: 'GET',});
      const data = await api_response.json();
      this.hobbybank = data.hobbies;
    },

    //this method will be used to add a new hobby to the hobby bank
    async POSThobby() {
      const api_response = await fetch('/api/hobbies/', {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': this.extractcsrfToken, },
        body: JSON.stringify({ name: this.hobbytoadd.trim() }),
      });
      const hobby = await api_response.json();
      this.hobbybank.push(hobby);
      this.GEThobby();
      this.hobbytoadd = '';
    },

    // this method will be used to add a new user hobby to their instance
    async POSTuserhobby() {
      await fetch('/api/user/', {method: 'POST', headers: {'Content-Type': 'application/json','X-CSRFToken': this.extractcsrfToken,},
        body: JSON.stringify({ hobby_id: this.selectedNewHobby }),
      });

      const addedHobby = this.hobbybank.find(hobby => hobby.id === Number(this.selectedNewHobby));
      if (addedHobby) {
        this.user?.hobbies.push([addedHobby.id, addedHobby.name]);
      }
      this.selectedNewHobby = '';
    },

    // This method will be used to delete a hobby the user selects
    async DELhobby(hobbyId: number) {
      await fetch('/api/user/', { method: 'DELETE', headers: {'Content-Type': 'application/json','X-CSRFToken': this.extractcsrfToken,},
       body: JSON.stringify({ hobby_id: hobbyId }),});
      const h_idx = this.user?.hobbies.findIndex(hobby => hobby[0] === hobbyId);
      if (h_idx !== undefined && h_idx >= 0) {
        this.user?.hobbies.splice(h_idx, 1);
      }
    },
  },

});
</script>
