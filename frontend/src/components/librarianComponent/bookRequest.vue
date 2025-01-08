<template>
  <div class="container outer-box">
    <div class="row bg-light m-0 mb-1 p-3">


      <div class="col">
        User Name
      </div>
      <div class="col">
        Book Name
      </div>
      <div class="col">
        Date Issued
      </div>
      <div class="col">
        Date End
      </div>
      <div class="col">
        Give Acess
      </div>


    </div>


    <div v-if='users.length != 0'>
      <div v-for="user in users" :key="user.user_id" class="row bg-secondary  bg-light m-0 mb-1 p-3">
        <div class="col">
          {{ user.user_name }}
        </div>
        <div class="col">
          {{ user.book_name }}
        </div>
        <div class="col">
          {{ formatDate(user.date_issued) }}
        </div>
        <div class="col">
          {{ formatDate(user.date_end) }}
        </div>
        <div class="col">
          <button>Approve access</button>
        </div>
      </div>
    </div>


    <!-- Else block for v-if directive -->
    <div v-else class="row bg-secondary  bg-light m-0 mb-1 p-3">
      <div class="col-12">
        <h4>No </h4>
      </div>
    </div>
  </div>


</template>
<script>
export default {
  name: 'bookRequest',
  data() {
    return {
      users: []
    };
  },
  mounted() {
    this.fetchUsers();
    console.log(this.$route.params.bookId)
  },
  methods: {
    async fetchUsers() {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        // const bookId = this.$route.params.bookId;
        const response = await fetch(`http://127.0.0.1:5000/requests/book`
          , {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          }
        );
        if (!response.ok) {
          throw new Error('Failed to fetch users');
        }
        const userData = await response.json();
        this.users = userData.map(user => ({
          ...user,
          date_issued: this.formatDate(user.date_issued),
          date_end: this.formatDate(user.date_end)
        }));
        console.log(this.users);
      } catch (error) {
        console.error('Error fetching users:', error.message);
        // Handle error, e.g., display an error message to the user
      }
    },

    formatDate(dateString) {
      const originalDate = new Date(dateString);
      return originalDate.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: '2-digit'
      });
    }
  }
};

</script>

<style scoped>
.outer-box {
  border: 1px solid black;
  padding: 0px;
  width: 80%;
  margin: auto;
  margin-top: 100px;
  max-height: 450px;
  overflow-y: scroll;
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
}
</style>