<template>
    <div class="h1">
      {{ title }}
    </div>
    
    <div>

    <!-- Incoming Requests Table -->
    <div>
      <h2>Incoming Friend Requests</h2>
      <table >
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(friend_request) in incoming_requests" >
            <td>{{  friend_request.id }}</td>
            <td>{{ friend_request.sender.name }}</td>
            <td>
              <button @click=acceptFriendRequest(friend_request) id="accept">Accept</button>
              <button @click=deleteFriendRequest(friend_request,true) id="decline">Decline</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Outgoing Requests Table -->
    <div>
      <h2>Outgoing Friend Requests</h2>
      <table >
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(friend_request) in outgoing_requests" >
            <td>{{  friend_request.id }}</td>
            <td>{{ friend_request.receiver.name }}</td>
            <td>
              <button @click=deleteFriendRequest(friend_request,false)>Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Friends Table -->
    <div>
      <h2>Friends</h2>
      <table >
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(friend) in friends" key="friend.id" :value="friend.id">
            <td>{{  friend.id }}</td>
            <td>{{ friend.user2.name }}</td>
            <td>
              <button @click=removeFriend(friend)>Remove</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    </div>
  </template>
  
  <script lang="ts">
    const baseUrl = 'http://127.0.0.1:8000'
      import { defineComponent } from "vue";
      import { Friend, FriendRequest } from "../types";

      export default defineComponent({
          data() {
              return {
                  title: "Friends Page",
                  incoming_requests: [] as FriendRequest[], // Explicitly typed as an array of FriendRequest
                  outgoing_requests: [] as FriendRequest[],
                  friends: [] as Friend[],
              }
          },
          computed: {
            csrfToken(): string {
            const cookies = document.cookie.split('; ');
            const csrfCookie = cookies.find((cookie) => cookie.startsWith('csrftoken='));
            return csrfCookie ? csrfCookie.split('=')[1] : '';
            },
        },
          async mounted() {
            const response = await fetch(`${baseUrl}/api/incoming-fr-api/`)
            const data = await response.json()
            this.incoming_requests = data.incoming_requests;
            const response2 = await fetch(`${baseUrl}/api/outgoing-fr-api/`)
            const data2 = await response2.json()
            this.outgoing_requests = data2.outgoing_requests;  
            const response3 = await fetch(`${baseUrl}/api/get-friends/`)
            const data3 = await response3.json()
            this.friends = data3.friends;
          },
        methods: {
            async removeFriend(friend: Friend){
                if (confirm(`Are you sure you want to remove '${friend.user2.name}'?`)) {
                    const response = await fetch(`${baseUrl}/api/remove-friend/`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': this.csrfToken,
                        },
                        body: JSON.stringify({ id: friend.id }),
                    })
                    if (response.ok)
                        this.friends = this.friends.filter(m => m.id !== friend.id)
                }
            },
            async deleteFriendRequest(friend_request: FriendRequest,isIncoming: boolean){
                const confirmMessage = isIncoming? `Are you sure you want to reject friend request from '${friend_request.sender.name}'?`: `Are you sure you want to cancel the outgoing friend request to '${friend_request.receiver.name}'?`;
                if (confirm(confirmMessage)) {
                    const response = await fetch(`${baseUrl}/api/delete-friend-request/`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': this.csrfToken,
                        },
                        body: JSON.stringify({ id: friend_request.id }),
                    })
                    if (response.ok){
                        if(isIncoming){
                            this.incoming_requests = this.incoming_requests.filter(m => m.id !== friend_request.id)
                        }else{
                            this.outgoing_requests = this.outgoing_requests.filter(m => m.id !== friend_request.id)
                        }
                    }
                }
            },
            async acceptFriendRequest(friend_request: FriendRequest){
                const response = await fetch(`${baseUrl}/api/accept-friend-request/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': this.csrfToken,
                        },
                        body: JSON.stringify({ id: friend_request.id }),
                    })
                    this.incoming_requests = this.incoming_requests.filter(req => req.id !== friend_request.id);
                    if (response.ok) {
                        const newFriend = await response.json();
                        console.log(newFriend.friendship) // Assuming the response contains the new friend's data
                        this.friends.push(newFriend.friendship); // Add the new friend to the list of friends
                    }
            }
        }
      })
  </script>
  
  <style scoped>
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  table th, table td {
    padding: 8px;
    text-align: left;
    color: white; /* Make text white */
  }
  
  table th {
    background-color: #f2f2f2;
  }
  
  h2 {
    margin-top: 20px;
    color: white; /* Make text white */
  }
  
  .h1 {
    color: white; /* Make text white */
  }
  
  body {
    background-color: #333; /* Dark background for contrast */
    color: white; /* Default text color white */
  }
  </style>