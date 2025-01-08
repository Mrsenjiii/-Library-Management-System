<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary fixed-top shadow-sm">
    <div class="container-fluid">
      <div class="logo-container d-flex align-items-center">
        <h3 class="navbar-brand mx-4 text-dark">My Library</h3>
      </div>
      <div class="ml-auto d-flex">
        <!-- Check current route and conditionally render buttons -->
        <button v-if="pageRoute !== 'signup'" @click="toSignUp" class="btn btn-outline-light border text-dark me-2" type="button">Sign Up</button>
        <button v-if="pageRoute !== 'librarian-login'" @click="managerLogin" class="btn btn-outline-light border text-dark me-2" type="button">Librarian Login</button>
        <button v-if="pageRoute !== 'login'" @click="userLogin" class="btn btn-outline-light border text-dark me-2" type="button">User Login</button>
      </div>
    </div>
  </nav>
</template>

<script>
import { useRoute } from 'vue-router';
import { computed } from 'vue';

export default {
  name: 'NavbarSignup',

  methods: {
    toSignUp() {
      this.$router.push('/signup');
    },

    userLogin() {
      this.$router.push('/login');
    },

    managerLogin() {
      this.$router.push('/librarian-login');
    }
  },

  setup() {
    const route = useRoute();

    // Compute the current route name
    const pageRoute = computed(() => route.name);

    return { pageRoute };
  },
}
</script>
