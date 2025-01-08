<template>
  <userNavbar />

  <router-view>

  </router-view>
</template>
<script>

import userNavbar from '../components/UsersComponents/userNavbar.vue'


export default {
  name: 'UserHome',
  components: {
    userNavbar

  },
  data() {
    return {

    }
  },

  methods: {

  },
  mounted() {
    const token = sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
  }

};
</script>
