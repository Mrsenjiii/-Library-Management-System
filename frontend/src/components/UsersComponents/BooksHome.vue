<template>

  <div class="outer-container my-4 ">
    <div v-for="genre in tempData" :key="genre.id" class="category-section border border-secondary border-opacity-50 p-2 border-1  rounded overflow-x-scroll">

      <div class="Genre text-start w-50 mx-2 my-2 border-bottom">
        <h3 class="category-title px-4">{{ genre.name }}</h3>
      </div>
      <div class="books-container fluid-container d-flex flex-nowrap row w-100 p-2 mx-2 ">
        <singleBookComponent v-for="book in genre.Books" :key="book.id" :book="book" @returnBook="returnBook" />
      </div>
    </div>
  </div>
  
</template>

<script>
import { filters, productToFilter } from './storeUser';
import singleBookComponent from './components/singleBookComponent.vue';
import { eventBus } from '../UsersComponents/userNavbar.vue';



export default {
  name: 'userProduct',
  data() {
    return {
      data: null,
      tempData: null,
      userId:this.$route.params.id,
      bookName:null,
      bookId:null,
      showFeedBackForm:false,
      propData:null,
    };
  },

  
  components: {
    singleBookComponent,
    // UserFeedbackForm
  },


  created() {
    eventBus.on('applyAllFilters', this.applyAllFiltersHandler);
    eventBus.on('searchForProduct', this.searchForProductHandler);
  },


  methods: {
    async fetchSections() {
      try {
        const token = sessionStorage.getItem('jwt_token');
        const headers = {
          
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        };
        const response = await fetch('http://127.0.0.1:5000/api/section', { headers , method: 'GET' });

        if (response.ok) {
          let data = await response.json();

          await Promise.all(data.map(async (section) => {
            try {
              const bookResponse = await fetch(`http://127.0.0.1:5000/api/section/${section.id}/books`, 
            
              {
                headers: headers
                ,method: 'GET'
              });
              if (bookResponse.ok) {
                const bookData = await bookResponse.json();
                section.Books = bookData.books;
              } else {
                throw new Error(`Error fetching books for section with ID ${section.id}`);
              }
            } catch (error) {
              console.error(`Error fetching books for section with ID ${section.id}`, error);
            }
          }));

          this.data = data.filter(section => section.Books && section.Books.length > 0);
          this.tempData = JSON.parse(JSON.stringify(this.data));
        } else {
          throw new Error('Failed to fetch sections');
        }
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    applyAllFiltersHandler() {
      this.tempData = JSON.parse(JSON.stringify(this.data));
      if (filters.section) {
        // console.log(filters.section ,'hello world')
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
    searchForProductHandler() {
      this.tempData = JSON.parse(JSON.stringify(this.data));
      const regex = new RegExp(productToFilter.value, 'i');
      this.tempData = this.tempData.filter(section => {
        section.Books = section.Books.filter(book => regex.test(book.name));
        return section.Books.length > 0;
      });
    },
    returnBook(cartDetails) {
    console.log(cartDetails, 'cartDetails'); // data is available in cartDetails
    this.propData = {...cartDetails};
    console.log(this.propData, 'propData');
    this.showFeedBackForm = true;
  },
  closeModel() {
    this.showFeedBackForm = false;
  },
  },
  mounted() {
    this.fetchSections();
  },
};
</script>
<style scoped>
.outer-container {
  width: 95%;
  margin: auto;
}


.category-section {
  margin-bottom: 2rem;
  box-shadow: rgba(0, 0, 0, 0.04) 0px 3px 5px;
  background-color: whitesmokes;  
}


.category-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}


.books-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
</style>