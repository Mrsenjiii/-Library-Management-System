<template>
    <div class="fluid-container text-start ">
    <div class="container d-flex justify-content-start">
      <div class="heading w-50  border-bottom border-info border-3" >
        <h3>My Requested Books</h3>
      </div>
    </div>
  </div>
  <div class="container-fluid my-5">
    <div class="container d-flex justify-content-start">
      <table class="table table-hover">

        <thead> <!-- Changed background color to navy blue -->
          <tr>
            <th class="bg-info " scope="col">Book Name</th>
            <th class="bg-info" scope="col">Requested For</th>
            <th class="bg-info" scope="col">Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-if="isObjectEmpty(data)">
            <td  class="align-middle p-4 text-start fs-4" colspan="3">No Book Requested</td>
          </tr>

          
          <tr v-for="cart in data" :key="cart.cart_id">
            <td class="align-middle">{{ cart.book_name }}</td>
            <td class="align-middle">{{ calculateDays(cart.date_issued, cart.date_end) }} days </td>
            <td class="align-middle">
              <button class="btn btn-warning" @click="deleteCart(cart.cart_id)">Cancel Request</button>
            </td>
          </tr>
        </tbody>

      </table>
    </div>
  </div>
</template>


<script>
export default {
  name: 'requestedBooks',
  data() {
    return {
      userId: this.$route.params.id,
      data: {},
    };
  },


  methods: {


    calculateDays(startDate, endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      const differenceInTime = end.getTime() - start.getTime();
      const differenceInDays = differenceInTime / (1000 * 3600 * 24);
      return differenceInDays;
    },

    async getUserCartsWithBookInfo(userId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const url = `http://127.0.0.1:5000/api/usercarts/${userId}?approved=0`;
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });
        if (!response.ok && response.status != 404) {
          throw new Error('Network response was not ok');
        }
        const responseData = await response.json();
        this.data = responseData.carts;
        return '';
      } catch (error) {
        console.error('Error getting user carts with product info:', error);
        throw error;
      }
    },

    async deleteCart(cartId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/cart/${cartId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },

        });
        if (!response.ok) {
          const errorMessage = await response.text();
          throw new Error(`Failed to delete cart: ${errorMessage}`);
        }
        this.data = this.data.filter(cart => cart.cart_id !== cartId);
        return await response.json();
      } catch (error) {
        console.error('Error deleting cart:', error);
        throw error;
      }
    },
    isObjectEmpty(obj) {
      const keys = Object.keys(obj);
      return keys.length === 0;
    },
  },

  mounted() {
    const token = sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    this.getUserCartsWithBookInfo(this.userId);
  },

};
</script>

<style scoped>
.bg-navy-blue {
  background-color: navy;
  color: white;
  /* Optionally change text color to white */
}
</style>