<template>
  <div>
    <div class="heading-box">
      <h3 class="page-heading">Finished Users Lists</h3>
    </div>
    <div class="container-fluid border p-4 rounded shadow-sm">
      <div class="w-100">
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th scope="col">User Name</th>
              <th scope="col" >Book Name</th>
              <th scope="col">Bought For</th>
              <th scope="col">Finished In</th>
              <th scope="col">Issued On</th>
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
              <td class="align-middle">{{ book.book_name }}</td>
              <td class="align-middle">{{ calculateDays(book.date_issued, book.return_date) }} days</td>
              <td class="align-middle">{{ calculateDays(book.date_issued, book.return_date) }} days</td>
              <td class="align-middle">
                {{ book.date_issued }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-if="message" :class="['alert-container', 'alert', 'alert-' + messageType, 'p-2', 'rounded-3']" role="alert">
      {{ message }}
    </div>
  </div>
</template>




<script>
export default {
  name: 'allFinishedBookUsers',
  data() {
    return {
      data: {},
      message: '',
      messageType: '',
      loading: true
    };
  },
  methods: {
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
          this.setMessage(`Failed to delete book: ${errorData.message || 'Unknown error'}`, 'error');
        }
      } catch (error) {
        console.error(error);
        this.setMessage('An unexpected error occurred while deleting the book.', 'error');
      }
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
            console.log('No users found for the specified book.');
            this.data = {};
          } else {
            throw new Error('Network response was not ok');
          }
        } else {
          const responseData = await response.json();
          this.data = responseData.completed_books;
          this.data.map(book => {
            book.date_issued = new Date(book.date_issued).toLocaleDateString();
          })
          console.log(this.data)
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        this.setMessage('Error fetching data', 'error');
      } finally {
        this.loading = false;
      }
    },

    isObjectEmpty(obj) {
      return Object.keys(obj).length === 0;
    },
  },
  mounted() {
    const token =   sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    this.getCompletedBooksUsers(this.$route.params.bookName);
  }
}
</script>

<style scoped>
.heading-box {
  margin-top: 0rem;
  margin-bottom: 2rem;
  text-align: left;
}

.page-heading {
  text-align: left;
  margin-left: 1.5rem;
  font-size: 1.75rem;
  font-weight: 600;
  color: #343a40;
  display: inline-block;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 4px solid #001eff;
}

.alert-container {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  width: 90%;
  max-width: 500px;
  text-align: center;
  box-sizing: border-box;
}

.alert-success {
  background-color: #28a745;
  color: white;
}

.alert-error {
  background-color: #dc3545;
  color: white;
}

.alert-warning {
  background-color: #ffc107;
  color: black;
}

.table {
  background-color: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: #f2f2f2;
}

.table-bordered th, .table-bordered td {
  border: 1px solid #dee2e6;
}

.btn-warning {
  background-color: #ffc107;
  border-color: #ffc107;
}

.btn-warning:hover {
  background-color: #e0a800;
  border-color: #d39e00;
}

.btn-success {
  background-color: #28a745;
  border-color: #28a745;
}

.btn-success:hover {
  background-color: #218838;
  border-color: #1e7e34;
}

.text-center {
  text-align: center;
}

.mb-4 {
  margin-bottom: 1.5rem;
}

.container-fluid {
  padding: 2rem;
}

.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,.075) !important;
}
</style>
