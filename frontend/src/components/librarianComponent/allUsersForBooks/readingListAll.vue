<template>
  <div>
    <div class="heading-box">
      <h3 class="page-heading">Books Users Reading</h3>
    </div>

    <div class="container border p-4 rounded shadow-sm">
      <div class="w-100">
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th scope="col">User</th>
              <th scope="col">Book Name</th>
              <th scope="col">Taken For</th>
              <th scope="col">Days Left</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="5" class="text-center">Loading...</td>
            </tr>
            <tr v-else-if="isObjectEmpty(data)">
              <td colspan="5" class="text-center">No Book in the Cart</td>
            </tr>
            <tr v-else v-for="book in data" :key="book.cart_id">
              <td class="align-middle">{{ book.user_name }}</td>
              <td class="align-middle">{{ book.book_name }}</td>
              <td class="align-middle">{{ calculateDays(book.date_issued, book.date_end) }} days</td>
              <td class="align-middle text-danger">{{ calculateDays(new Date(), book.date_end) }} days</td>
              <td class="align-middle">
                <button class="btn btn-danger" @click="deleteCart(book.cart_id)">
                  <i class="bi bi-x-circle"></i> Remove access
                </button>
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
  name: 'allReadingUsersList',
  data() {
    return {
      userId: this.$route.params.id,
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

    async getUserBookCartsWithProductInfo(approved = 1) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const url = `http://127.0.0.1:5000/api/carts?approved=${approved}`;
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const responseData = await response.json();
          this.data = responseData.carts;
        } else if (response.status === 404) {
          this.setMessage('No carts found', 'warning');
        } else {
          throw new Error('Network response was not ok');
        }
      } catch (error) {
        console.error('Error getting user book carts with product info:', error);
        this.setMessage('Failed to load books', 'error');
      } finally {
        this.loading = false;
      }
    },

    async deleteCart(cartId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        if (!confirm('Are you sure you want to remove access to this book?')) {
          return;
        }
        const response = await fetch(`http://127.0.0.1:5000/api/cart/${cartId}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          method: 'DELETE'
        });
        if (response.ok) {
          this.data = this.data.filter(cart => cart.cart_id !== cartId);
          this.setMessage('Access removed successfully', 'success');
        } else {
          const errorMessage = await response.text();
          throw new Error(`Failed to remove access: ${errorMessage}`);
        }
      } catch (error) {
        console.error('Error deleting cart:', error);
        this.setMessage('An error occurred while removing access', 'error');
      }
    },
    
    isObjectEmpty(obj) {
      return Object.keys(obj).length === 0;
    },
  },
  mounted() {
    const token = sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    this.getUserBookCartsWithProductInfo();
  },
};
</script>

<style scoped>
.heading-box {
  margin-top: 2rem;
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
  border-bottom: 4px solid #ff0051;
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

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

.text-center {
  text-align: center;
}

.container {
  padding: 2rem;
}

.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,.075) !important;
}
</style>
