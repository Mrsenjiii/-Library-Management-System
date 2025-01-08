
<!-- 
A signle component which will be render for each book in the database.
-->

<template>


  <div class="box col-md-4 col-lg-2 col-xl-2 col-xxl-2 mx-2 rounded-1 p-0">
    <div class="fluid-container w-100" @click="pushToBook(book.id, book.name)" style="cursor:pointer">
      <!-- Dynamically bind the image source -->
      <img :src="image_link(book.book_loc_url)" style="width:100%; height: auto;" :alt="book.name">
    </div>

    <div class="container text-start">

      <p @click="pushToBook(book.id, book.name)" style="cursor:pointer" class="fw-bold m-0 p-1">Book Name: {{ book.name }}</p>
      <p class="fw-medium m-0 p-1">Author: {{ book.author }}</p>
      <p class="fw-bolder m-0 p-1">Price: {{ book.price }}</p> 
      <p class="fw-bolder m-0 p-1">Genre {{ book.genre }}</p>
      
    
      <button v-if="status === 'Not Requested'" type="button" class="btn btn-primary" @click="requestBook(userId, book.id)">Request Book</button>
      <div class="read-and-return fluid-container d-flex  flex-row-start" v-else-if="status === 'Approved'">
        <button  type="button" class="btn btn-success col-4 m-1" style="font-size: 1rem" @click="readBook(book.book_pdf_loc_url)">Read </button>
        <button type="button" class="btn btn-warning  col-4 m-1" style="font-size:1rem" @click="returnBook(cartId)">Return</button>
      </div>

      <button v-else type="button" class="btn btn-warning my-2" @click="deleteCart(userId, book.id)">Cancel Request</button>
      
    </div>

    <ul v-if="status === 'Not Requested'" class="container-fluid row justify-content-end mt-2">
      <li class="col-12 list-group-item">
        <div class="container-fluid row justify-content-start mx-1">
          Days: {{ items }}
          <button class="btn-sm btn btn-outline-danger px-2 mx-1 col-2" :disabled="items >= 14" @click="add(1)">+</button>
          <button class="btn-sm btn btn-outline-danger px-2 col-2" :disabled="items <= 1" @click="minus(1)">-</button>
        </div>
      </li>
    </ul>
  </div>


</template>


<script>

export default {
  name: 'singleBookComponent',
  props: {
    book: Object,
    noOfproductsInCart: Number
  },
  data() {
    return {
      userId: this.$route.params.id,
      items: 3, // Default number of days
      bookDetailforUser: null,
      cartId:null,
      status: '',
      showFeedBackForm:false,
    };
  },

  components: {
    
  },
  methods: {
    async getUserCarts(userId, bookId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/users/${userId}/carts/${bookId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          
          }
        });
        if (!response.ok) {
          throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
        this.bookDetailforUser = await response.json();
        if (this.bookDetailforUser.cart_id) {
          this.cartId = this.bookDetailforUser.cart_id
          this.status = this.bookDetailforUser.approved ? 'Approved' : 'Not Approved';
        } else {
          this.status = 'Not Requested';
        }
      } catch (error) {
        console.error('An error occurred while fetching user carts:', error.message);
      }
    },

    async requestBook(userId, bookId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const proceed = confirm('Are you sure you want to request this book?');
        if (!proceed) return;

        const today = new Date();
        today.setDate(today.getDate() + this.items);
        const url = `http://127.0.0.1:5000/api/users/${userId}/carts/${bookId}`;
        const data = {
          date_issued: new Date(),
          date_end: today
        };
        
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(data),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const responseData = await response.json();
        console.log('Book request successful:', responseData);
        this.status = 'Not Approved';
      } catch (error) {
        console.error('Error requesting book:', error);
      }
    },


    async deleteCart(userId, bookId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const proceed = confirm('Are you sure you want to delete this cart?');
        if (!proceed) return;

        const response = await fetch(`http://127.0.0.1:5000/api/users/${userId}/carts/${bookId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,

          }
        });
        if (!response.ok) {
          throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }

        console.log('Cart deleted successfully.');
        this.status = 'Not Requested';
      } catch (error) {
        console.error('An error occurred while deleting the cart:', error.message);
      }
    },
    
    returnBook(cartId){
      this.$router.push({ name: 'returnBook', params: { cartId: cartId } });
    },
    closeEditModel(){
      this.showFeedBackForm = false;
    },
    add(count) {
      this.items += count;
    },
    minus(count) {
      this.items -= count;
    },
    pushToBook(id, name) {
      console.log(id, name);
      this.$router.push({
        name: 'singleBookInfoUser', // Route name defined in your router
        params: { book_name: name }, // Route parameter, must match the param defined in the route
        query: { bookId: id } // Additional data passed as query parameters
      });
      console.log(this.$route.params);
    },
    readBook(src) {
      window.open(`http://localhost:5000/static/${src}`, '_blank');
    },

    image_link(src) {
      console.log(src, 'source .......');
      // Adjust this path according to your project structure
      // You might need to update the path to match your actual structure
      let url = `http://127.0.0.1:5000/static/${src}`;
      return url;
    }
  },
  mounted() {
    const token = sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    this.getUserCarts(this.userId, this.book.id);
  }
};
</script>

<style scoped>
.box {
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
}
.box:hover {
  box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
}
</style>