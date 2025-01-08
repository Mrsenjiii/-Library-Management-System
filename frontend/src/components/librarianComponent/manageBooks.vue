<template>
  <div class="outer-container my-4">
    <!-- {{ showfilters }} -->
    <!-- {{ this.showfilters }} -->
    <div v-for="genre in tempData" :key="genre.id">
      
      <div class="fluid-container bg-light rounded p-2" :ref="`productContainerWrapper_${genre.id}`" style="box-shadow: rgba(0, 0, 0, 0.04) 0px 3px 5px;">
        <div class="Genre text-start w-50 mx-2 my-2 border-bottom">
          <h3 class="category-title px-4">{{ genre.name }}</h3>
        </div>
        <div class="d-flex flex-nowrap row w-100 p-2 overflow-auto">
          <productComponentManager v-for="book in genre.Books" @deleteBook="deleteBook" :key="book.id" :book="book" />
        </div>
      </div>
    </div>
  </div>
  
  <div :class="['filter-box', { 'show': showfilters }]">
    <div class="offcanvas-body" v-if="this.showfilters">
      <form @submit.prevent="applyAllFiltersHandler">
        <div class="container mb-3 text-start">
          <label for="cars" class="form-label">Choose a Section:</label>
          <select id="cars" name="cars" class="form-select" v-model="filters.section">
            <option :value="null">Select a Book Section</option>
            <option v-for="section in Sections" :key="section.id" :value="section.id">{{ section.name }}</option>
          </select>
        </div>
        <div class="container mb-3 text-start">
          <label for="initialPrice" class="form-label">Starting Price</label>
          <input type="number" id="initialPrice" class="form-control" v-model="filters.priceStart">
        </div>
        <div class="container mb-3 text-start">
          <label for="finalPrice" class="form-label">Ending Price</label>
          <input type="number" id="finalPrice" class="form-control" v-model="filters.priceEnd">
        </div>
        <div class="container mb-3 text-start">
          <label for="author" class="form-label">Author Name</label>
          <input type="text" id="author" class="form-control" v-model="filters.Author">
        </div>
        <div class="container mb-3 text-start">
          <label for="mfgStart" class="form-label">Book Issue Date</label>
          <input type="number" id="mfgStart" class="form-control" min="1600" max="2024" v-model="filters.year">
        </div>
        <div class="container mb-3 text-start">
          <button type="submit" class="btn btn-primary">Apply Filters</button>
        </div>
      </form>
    </div>
  </div>

  <div @click="addBook" class="fixed-button">
    <button class="round-button bg-light text-black">+</button>
  </div>
</template>

<script>
import productComponentManager from './smallBookView.vue';
import eventBus from './eventBus';
import { filters, productToFilter } from './storeManager';

export default {
  name: 'ManageProducts',
  data() {
    return {
      data: null,
      showfilters: false,
      filters, // Add filters here
      tempData: null,
      Sections: [], // Add this to store sections data
      productToFilter,
    };
  },
  components: {
    productComponentManager,
  },
  methods: {
    handleDataEvent() {
      this.showfilters = !this.showfilters;
      console.log("showfilters", this.showfilters);
    },

    async fetchSections() {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const response = await fetch('http://127.0.0.1:5000/api/section', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          this.Sections = data; // Store sections data
          const bookPromises = data.map(async (section) => {
            try {
              const bookResponse = await fetch(`http://127.0.0.1:5000/api/section/${section.id}/books`, {
                method: 'GET',
                headers: {
                  'Authorization': `Bearer ${token}`,
                  'content-type': 'application/json'
                }
              });
              if (bookResponse.ok) {
                const bookData = await bookResponse.json();
                section['Books'] = bookData.books;
              } else {
                throw new Error(`Error fetching books for section with ID ${section.id}`);
              }
            } catch (error) {
              console.log(`Error fetching books for section with ID ${section.id}`, error);
            }
          });
          await Promise.all(bookPromises);
          this.data = data.filter(section => section.Books && section.Books.length > 0);
          this.tempData = JSON.parse(JSON.stringify(this.data));
        } else {
          const data = await response.json();
          console.log(data);
        }
      } catch (error) {
        console.log('Error in fetching sections', error);
      }
    },


    addBook() {
      console.log('add book');
      this.$router.push('/librarian/' + this.$route.params.id + '/addProduct');
    },
    applyAllFiltersHandler() {
      confirm('Are you sure you want to apply all filters?');
      this.tempData = JSON.parse(JSON.stringify(this.data));
      if (filters.section) {
        this.tempData = this.tempData.filter(section => section.id === filters.section);
      }
      if (filters.Author) {
        const regex = new RegExp(filters.Author, 'i');
        this.tempData = this.tempData.filter(section => {
          section.Books = section.Books.filter(book => regex.test(book.author));
          return section.Books.length > 0;
        });
      }
      if (filters.priceStart || filters.priceEnd) {
        const priceStart = parseInt(filters.priceStart) || 0;
        const priceEnd = parseInt(filters.priceEnd) || Infinity;
        this.tempData = this.tempData.filter(section => {
          section.Books = section.Books.filter(book => {
            const price = parseInt(book.price);
            return !isNaN(price) && price >= priceStart && price <= priceEnd;
          });
          return section.Books.length > 0;
        });
      }
    },
    searchForProductHandler(newValue, oldValue) {
      console.log('newValue', newValue, 'oldValue', oldValue);
      this.tempData = JSON.parse(JSON.stringify(this.data));
      const regex = new RegExp(productToFilter.value, 'i');
      this.tempData = this.tempData.filter(section => {
        section.Books = section.Books.filter(book => regex.test(book.name));
        return section.Books.length > 0;
      });
    },
    deleteBook(bookIdToDelete) {
      this.data = this.data.filter(section => {
        section.Books = section.Books.filter(book => book.id !== bookIdToDelete);
        return section.Books.length > 0;
      })
      this.data = JSON.parse(JSON.stringify(this.data));
    }
  },
  mounted() {
    const token = sessionStorage.getItem('jwt_token');
    console.log( token , 'token');
    if (!token) {
      this.$router.push('/login');
    } else {
      this.fetchSections();
      eventBus.on('applyAllFilters', this.handleDataEvent);
    }
  },
  beforeUnmount() {
    eventBus.off('applyAllFilters', this.handleDataEvent);
  },
  watch: {
    productToFilter: 'searchForProductHandler'
  }
};
</script>

<style scoped>
.outer-container {
  width: 95%;
  margin: auto;
  overflow: hidden;
}
.overflow-auto {
  overflow-x: auto;
}
.fixed-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}
.round-button {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 1px solid black;
  color: white;
  font-size: 70px;
  text-align: center;
  line-height: 50px;
  cursor: pointer;
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 1px 3px 1px;
}
.round-button:hover {
  box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
}
.filter-box {
  background-color: white;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  right: 0;
  z-index: 10000;
  border-radius: 8px 0 0 8px;
  width: 400px;
  height: 100vh;
  transform: translateX(100%);
  transition: transform 0.3s ease;
}
.filter-box.show {
  transform: translateX(0);
}
</style>
