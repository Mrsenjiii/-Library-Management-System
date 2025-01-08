<template>
  <div>
    <div class="heading-box">
       <h3 class="page-heading">ALL Requested Books</h3>
    </div>
  
    <div class="container-fluid border p-4 rounded shadow-sm">
      <div class="w-100">
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th scope="col">User</th>
              <th scope="col">Book Name</th>
              <th scope="col">Requested For</th>
              <th scope="col">Requested on</th>
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
            <tr v-else v-for="cart in data" :key="cart.cart_id">
              <td class="align-middle"> {{ cart.user_name }}</td>
              <td class="align-middle">{{ cart.book_name }}</td>
              <td class="align-middle">{{ calculateDays(cart.date_issued , cart.date_end) }} days</td>
          
                <td class="align-middle">{{ cart.date_issued }}</td>
        
              <td class="align-middle">
                <button class="btn btn-warning m-1" @click="deleteCart(cart.cart_id)">Cancel Request</button>
                <button class="btn btn-success m-1" @click="approveCart(cart.cart_id , calculateDays(cart.date_issued , cart.date_end))">Approve Request</button>
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
  name: 'requestedUsersList',
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

    async deleteCart(cartId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        if (!confirm('Are you sure you want to delete this cart?')) {
          return;
        }
        const url = `http://127.0.0.1:5000/api/cart/${cartId}`;
        const response = await fetch(url, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });
        if (response.ok) {
          this.setMessage('Cart deleted successfully', 'success');
          this.data = this.data.filter(cart => cart.cart_id !== cartId); 
        } else {
          this.setMessage('Failed to delete cart', 'error');
        }
      } catch (error) {
        console.error(error);
        this.setMessage('An error occurred while deleting the cart', 'error');
      }
    },

    async approveCart(cartId, daysToApprove) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        if (!confirm('Are you sure you want to approve this book for the user?')) {
          return;
        }
        const url = `http://127.0.0.1:5000/api/cart/${cartId}`;
        const response = await fetch(url, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({
            daysToApprove: daysToApprove
          }),
        });
        if (response.ok) {
          this.setMessage('Cart approved successfully', 'success');
          this.data = this.data.filter(cart => cart.cart_id !== cartId);
        } else {
          this.setMessage('Failed to approve cart', 'error');
        }
      } catch (error) {
        console.error(error);
        this.setMessage('An error occurred while approving the cart', 'error');
      }
    },

    async getUserBookCartsWithProductInfo(approved = 0) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      this.loading = true; // Start loading
      try {
        const url = `http://127.0.0.1:5000/api/carts?approved=${approved}`;
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          if (response.status === 404) {
            console.log('No carts found for the specified user and book.');
            return null;
          } else {
            throw new Error('Network response was not ok');
          }
        }

        const responseData = await response.json();
        console.log(responseData);
        this.data = responseData.carts;
        this.data = this.data.map(cart => {
          cart.date_issued = new Date(cart.date_issued).toLocaleDateString();
          cart.date_end = new Date(cart.date_end).toLocaleDateString();
          return cart;
        })
      } catch (error) {
        console.error('Error getting user book carts with product info:', error);
        throw error;
      } finally {
        this.loading = false; // End loading
      }
    },

    isObjectEmpty(obj) {
      return Object.keys(obj).length === 0;
    },
  },
  mounted() {
    this.getUserBookCartsWithProductInfo(0);
  },
};
</script>

<style scoped>
.heading-box{
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
