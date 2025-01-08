<template>
  <div class="box col-md-4 col-lg-2 col-xl-2 col-xxl-2 mx-2 rounded-1 p-2 ">


    <div class="fluid-container w-100" style="cursor:pointer" @click="pushToBook(book.id, book.name)">
      <!-- Dynamically bind the image source -->
      <img :src="image_link(book.book_loc_url)" style="width:100%; height:  auto;" :alt="book.name">
    </div>


    <div class="container text-start">


      <p @click="pushToBook(book.id, book.name)" style="cursor:pointer" class="fw-bold m-0 p-1">Book Name: {{
        book.name }}</p>
      <p class="fw-medium m-0 p-1">Author: {{ book.author }}</p>
      <p class="fw-bolder m-0 p-1">Price: {{ book.price }}</p>
      <p class="fw-bolder m-0 p-1">Genre {{ book.genre }}</p>
      
    </div>

    
    <div class="container-fluid   d-flex justify-content-start align-items-end">

      <span class="m-0 me-1">
        <button class="p-2  custom-button" @click="deleteBook(book.id)">
          Delete
        </button>
      </span>
      <span class="m-0 me-1">
        <button class="p-2 bg-grey  custom-button" @click="editProduct(book.id)">
          Edit
        </button>
      </span>

      <span class="m-0 me-1">
        <button class="p-2 bg-grey  custom-button" @click="toBookUser(book.id)">
          Users
        </button>
      </span>

    </div>



    <!-- <h1>{{ book.book_name }}</h1> -->
  </div>
</template>



<script>


export default {

  name: 'productComponentManager',
  props: {
    book: Object
  },

  data() {

    return {



    }

  },



  components: {
    // AppNavbar
  },

  methods: {


    async deleteBook(bookIdToDelete) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/book/${bookIdToDelete}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const result = await response.json();
          this.$emit('deleteBook', bookIdToDelete.id);
          console.log(result.message);  // Log the success message from the server
        } else {
          const errorData = await response.json();
          console.error(`Error: ${errorData.message}`);
        }
      } catch (error) {
        console.error('An error occurred while processing the request:', error);
      }
    },


    editProduct(idToEdit) {

      console.log(idToEdit)
      this.$router.push('/librarian/' + this.$route.params.id + '/editProduct/' + idToEdit)
      console.log(this.$route.params.id)
      console.log(idToEdit)
    },
    addProduct() {


      console.log('add book')
      this.$router.push('/librarian/' + this.$route.params.id + '/editProduct')
    },
    toBookUser(bookId) {
      this.$router.push('/librarian/' + this.$route.params.id + '/userBook/' + bookId + '/requests-persons')
    },
    image_link(src) {
      console.log(src, 'source .......');
 
      let url = `http://127.0.0.1:5000/static/${src}`;
      return url;
    },
    pushToBook(id, name) {
      console.log(id, name , 'id name');
      this.$router.push({
        name: 'bookInfoMananger',
        params: { book_name: name }, 
        query: { bookId: id } // Additional data passed as query parameters
      });
      console.log(this.$route.params);
    },
  },



  watch: {

  },
  mounted() {
    // this.getCart()
    const token = sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
  }
}

</script>

<style scoped>
.box {
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
  ;
}

.box:hover {
  box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
}

.custom-button {
  border: none;
}

.custom-button:hover {
  border: 1px solid black;
}
</style>