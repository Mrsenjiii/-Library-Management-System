<template>
  <div>
    <div class="fluid-container text-start">
      <div class="container d-flex justify-content-start">
        <div class="heading w-50 border-bottom border-secondary border-3">
          <h3>Finished Users List</h3>
        </div>
      </div>
    </div>
    <div class="container-fluid my-4">
      <div class="container d-flex justify-content-start">
        <table class="table table-hover">
          <thead>
            <tr>
              <th class="bg-secondary" scope="col">User Name</th>
              <th class="bg-secondary" scope="col">Bought For</th>
              <th class="bg-secondary" scope="col">Finished In</th>
              <th class="bg-secondary" scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="4" class="text-center">Loading...</td>
            </tr>
            <tr v-else-if="isObjectEmpty(data)">
              <td colspan="4" class="text-center">No Book in the Cart</td>
            </tr>
            <tr v-else v-for="book in data" :key="book.id">
              <td class="align-middle">{{ book.user_name }}</td>
              <td class="align-middle">{{ calculateDays(book.date_issued, book.return_date) }} days</td>
              <td class="align-middle">{{ calculateDays(book.date_issued, book.return_date) }} days</td>
              <td class="align-middle">
                <button class="btn btn-warning" @click="deleteCart(book.id)">Cancel Request</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-if="message" :class="['alert', 'alert-' + messageType]" role="alert">
      {{ message }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'finishedBooks',
  data() {
    return {
      userId: this.$route.params.id,
      bookId: this.$route.params.bookId,
      data: {},
      message: '',
      messageType: '',
      loading: true,
    };
  },
  methods: {
    isObjectEmpty(obj) {
      return Object.keys(obj).length === 0;
    },

    calculateDays(startDate, endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      const differenceInTime = end.getTime() - start.getTime();
      const differenceInDays = differenceInTime / (1000 * 3600 * 24);
      return Math.ceil(differenceInDays);
    },

    setMessage(text, type) {
      this.message = text;
      this.messageType = type;
      setTimeout(() => {
        this.message = '';
      }, 3000);
    },

    async getCompletedBooksUsers(bookName) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const response = await fetch(`http://localhost:5000/api/completed_books?book_name=${bookName}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          if (response.status === 404) {
            this.setMessage('No users found for the specified book.', 'warning');
            this.data = {};
          } else {
            throw new Error('Network response was not ok');
          }
        } else {
          const responseData = await response.json();
          this.data = responseData.completed_books;
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        this.setMessage('Error fetching data', 'danger');
      } finally {
        this.loading = false;
      }
    },

    async deleteCart(id) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      } 
      try {
        const confirmation = confirm('Are you sure you want to delete this book from your cart?');
        if (!confirmation) {
          return;
        }

        const url = `http://127.0.0.1:5000/api/delete_completed_books_users?book_id=${id}`;
        const response = await fetch(url, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          this.setMessage('Book deleted successfully from finished books list', 'success');
          this.data = this.data.filter(book => book.id !== id);
        } else {
          const errorData = await response.json();
          this.setMessage(`Failed to delete book: ${errorData.message || 'Unknown error'}`, 'danger');
        }
      } catch (error) {
        console.error(error);
        this.setMessage('An unexpected error occurred while deleting the book.', 'danger');
      }
    },
  },

  mounted() {
    const token = sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    this.getCompletedBooksUsers(this.bookId);
  },
};
</script>

<style scoped>
.heading {
  margin-bottom: 1rem;
}

.table {
  background-color: #fff;
}

.text-center {
  text-align: center;
}

.alert {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  width: 90%;
  max-width: 500px;
  text-align: center;
}
</style>
