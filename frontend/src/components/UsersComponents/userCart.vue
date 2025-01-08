


<template>
  <div class="fluid-container mt-3">
    <div class="d-flex justify-content-end">
      <div class="p-2">
        <button class="btn btn-primary" @click="redirectTo('requestedBooks')">Requested Books</button>
      </div>
      <div class="p-2">
        <button class="btn btn-danger" @click="redirectTo('readingBooks')">Reading Books</button>
      </div>
      <div class="p-2">
        <button class="btn btn-secondary" @click="redirectTo('completedBooks')">Completed Books</button>
      </div>
    </div>
  </div>
  <router-view></router-view>
</template>

<script>
export default {
  name: 'userCart',

  methods: {
    redirectTo(routeName) {
      // Redirect to the specified route
      this.$router.push({ name: routeName });
    }
  },
  data() {
    return {
      userId: null // Initialize userId to null
    };
  },
  created() {
    // Access the route params in the created hook
    this.userId = this.$route.params.id;
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