<template>
    <div class="fluid-container text-start ">
    <div class="container d-flex justify-content-start">
      <div class="heading w-50  border-bottom border-danger border-3" >
        <h3>Reading Books List</h3>
      </div>
    </div>
  </div>
  <!-- <h3>Reading Books</h3> -->
  <div class="container-fluid my-4">
    <div class="container d-flex justify-content-start">
      <table class="table table-hover ">
        <thead class="bg-danger">
          <tr>
            <th class="bg-danger" scope="col">Book Name</th>
            <th class="bg-danger" scope="col">Bought For</th>
            <th class="bg-danger" scope="col">Days Left</th>
            <th class="bg-danger" scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isObjectEmpty(data)">
            <td  class="align-middle p-4 text-start fs-4" colspan="4">No Books in Reading List </td>
          </tr>
          <tr v-else v-for="book in data" :key="book.cart_id">
            <td class="align-middle"> {{ book.book_name }}</td>
            <td class="align-middle">{{ calculateDays(book.date_issued, book.date_end) }} days</td>
            <td class="align-middle">{{ calculateDays(new Date() , book.date_end) }} days</td>
            <td class="align-middle">
              <button class="btn btn-warning" @click="deleteCart(book.cart_id)">Return Book</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'readingBooks',
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
      const differenceInTime =   end.getTime() - start.getTime();
      const differenceInDays = differenceInTime / (1000 * 3600 * 24);
      return Math.ceil(differenceInDays);
    },


    async getUserCartsWithBookInfo(userId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const url = `http://127.0.0.1:5000/api/usercarts/${userId}?approved=1`;
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
    deleteCart(cartId){
      this.$router.push({ name: 'returnBook', params: { cartId: cartId } });
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
