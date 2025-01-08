<template>

<div class="fluid-container text-start ">
    <div class="container d-flex justify-content-start">
      <div class="heading w-50  border-bottom border-danger border-3" >
        <h3>Reading Users List</h3>
      </div>
    </div>
  </div>
  <div class="container-fluid my-4">
    <div class="container d-flex justify-content-start">
      <table class="table table-hover">

        <thead>
          <tr>
            <th class="bg-danger " scope="col">Book Name</th>
            <th class="bg-danger" scope="col">Taken For</th>
            <th class="bg-danger" scope="col">Days left</th>
            <th class="bg-danger" scope="col">Action</th>
          </tr>
        </thead>
        
        <tbody>
          <tr v-if="isObjectEmpty(data)">
            <td  class="align-middle p-4 text-start fs-4" colspan="4">No Books in Reading List </td>
          </tr>
          <tr v-for="book in data" :key="book.cart_id">
            <td class="align-middle">{{ book.user_name }}</td>
            <td class="align-middle">{{ calculateDays(book.date_issued, book.date_end) }}</td>
            <td class="align-middle">{{ calculateDays(new Date(), book.date_end) }}</td>
            <td class="align-middle"> <button class="btn btn-warning" @click="deleteCart(book.cart_id)">Remove access</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>


</template>



<script>



export default {
  name: 'readingBookList',
  data() {
    return {
      userId: this.$route.params.id,
      book_Id: this.$route.params.bookId,
      data: {},
    };
  },


  methods: {


    calculateDays(startDate, endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      const differenceInTime =   end.getTime() - start.getTime();
      const differenceInDays = differenceInTime / (1000 * 3600 * 24);
      return Math.ceil(differenceInDays);
    },

    async getUserBookCartsWithProductInfo(bookId, approved = 1) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const url = `http://127.0.0.1:5000/api/carts/${bookId}?approved=${approved}`;
        const response = await fetch(url, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            // Add Authorization header if JWT is required
            'Authorization': `Bearer ${token}`
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
        console.log(responseData)
        this.data = responseData.carts;
        // return responseData.carts;
        console.log(this.data)

      } catch (error) {
        console.error('Error getting user book carts with product info:', error);
        throw error;
      }
    },





    async deleteCart(cartId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      alert('delete cart' + cartId)
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/cart/${cartId}`, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          method: 'DELETE'
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
    if (!sessionStorage.getItem('jwt_token')) {
      this.$router.push('/login');
      return;
    }
    this.getUserBookCartsWithProductInfo(this.book_Id);
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