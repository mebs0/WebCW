export interface Hobby {
   id: number;
   name: string;
 }
 
 export interface User {
   id: number;
   name: string;
   username: string;
   email: string;
   date_of_birth: string;
   hobbies: [number, string][];
   shared_hobbies: number;
   age: number;
   isstaff: boolean;
 }

export interface FriendRequest {
  id: number;
  sender: User2;
  receiver: User2;
  }

export interface Friend {
  id: number;
  user2: User2
}


interface User2 {
  name: string;
  username: string;
  email: string;
  date_of_birth: string;
  hobbies: [number, string][];
  }