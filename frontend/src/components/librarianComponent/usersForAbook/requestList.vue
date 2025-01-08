<template>
  <div class="fluid-container text-start ">
<div class="container d-flex justify-content-start">
  <div class="heading w-50  border-bottom border-primary border-3" >
    <h3>Reading Users List</h3>
  </div>
</div>
</div>
<div class="container-fluid my-4">
<div class="container d-flex justify-content-start">
  <table class="table table-hover">
        <thead>
          <tr>
            <th class="bg-info " scope="col">Book Name</th>
            <th class="bg-info" scope="col">No of days</th>
            <th class="bg-info" scope="col">Action</th>
            <th class="bg-info" scope="col">Action</th>
          </tr>
        </thead>


        <tbody>
      
          <tr v-if="isObjectEmpty(data)">
            <td  class="align-middle p-4 text-start fs-4" colspan="4">No Book is Requested </td>
          </tr>

          
          <tr v-for="cart in data" :key="cart.cart_id">
            <td class="align-middle">{{ cart.user_name }}</td>
            <td class="align-middle">{{ calculateDays(cart.date_issued , cart.date_end) }} days</td>
            <td class="align-middle"> <button class="btn btn-warning" @click="deleteCart(cart.cart_id)">Cancel Request</button></td>
            <td class="align-middle">
                <button class="btn btn-warning" @click="approveCart(cart.cart_id , calculateDays(cart.date_issued , cart.date_end) ) ">Approve Request</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>


</template>

<script>


export default {
  name: 'requestList',
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
      const differenceInTime = end.getTime() - start.getTime();
      const differenceInDays = differenceInTime / (1000 * 3600 * 24);
      // this.daysToRead = differenceInDays
      return differenceInDays;
    },

    async deleteCart(cartId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        if (!confirm('Are you sure you want to delete this cart?')) {
          return ;
        }
        const url = `http://127.0.0.1:5000/api/cart/${cartId}`;
        const response = await fetch(url, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          alert('Cart deleted successfully');
          this.getUserBookCartsWithProductInfo(this.book_Id);
          // this.data = this.data.filter(cart => cart.cart_id !== cartId);
        } else {
          alert('Failed to delete cart');
        }
      } catch (error) {
        console.error(error);
      }
    },

    async approveCart(cartId , daysToApprove) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        if (!confirm('Are you sure you want to Approve this Book for the user?')) {
          return ;
        }
        const url = `http://127.0.0.1:5000/api/cart/${cartId}`;
        const response = await fetch(url, {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
          daysToApprove: daysToApprove
      }),
        });
        if (response.ok) {
          alert('Cart Approved Succesfully');
          this.getUserBookCartsWithProductInfo(this.book_Id);
        } else {
          alert('Failed to Approve cart');
        }
      } catch (error) {
        console.error(error);
      }
    },


    async getUserBookCartsWithProductInfo(bookId, approved = 0) {
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
            'Authorization': `Bearer ${token}`,
            // Add Authorization header if JWT is required
            // 'Authorization': `Bearer ${token}`
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
    this.getUserBookCartsWithProductInfo(this.$route.params.bookId, 0);
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