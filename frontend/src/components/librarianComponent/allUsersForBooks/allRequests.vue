<template>



    <div class="fluid-container mt-3">
      <div class="d-flex justify-content-end">
        <div class="p-2">
          <button class="btn btn-primary" @click="redirectTo('all-requests-persons')">Requested</button>
        </div>
        <div class="p-2">
          <button class="btn btn-danger" @click="redirectTo('all-reading-persons')">Reading</button>
        </div>
        <div class="p-2">
          <button class="btn btn-secondary" @click="redirectTo('all-completed-books')">Finished</button>
        </div>
      </div>
    </div>
  
  
  
    <router-view></router-view>
  
  
  
  </template>
  <script>
  export default {
    name: 'allRequests',
    data() {
      return {
        
      };
    },
    mounted() {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
 
    },
    methods: {
      redirectTo( routeName ) {
        // Redirect to the specified route
        this.$router.push({ name: routeName });
      }
    }
  };
  
  </script>
  
  <style scoped>
  .outer-box {
    border: 1px solid black;
    padding: 0px;
    width: 60%;
    margin: auto;
    margin-top: 100px;
    max-height: 450px;
    overflow-y: scroll;
    box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
  }
  </style>