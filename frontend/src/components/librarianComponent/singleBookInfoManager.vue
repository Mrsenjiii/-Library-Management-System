<template>
    <div class="outer-box">
      <div class="container book-info p-2">
        <div v-if="bookDetailforUser" class="container">
          <div class="row">


            <div class="book-image col-3 p-0">
              <div class="image-cover p-0 d-inline-block my-1">
                <img :src="image_link(this.bookDetailforUser.book_loc_url)" class="w-100" alt="Image not found">
                <!-- <img :src="image_link(product.book_loc_url)" style="width:100%; height: auto;" :alt="product.name"> -->
  
                <div class="price text-start w-100 m-1">
                  <h5>Price: {{ bookDetailforUser.price }}</h5>
                </div>
              </div>
            </div>


            <div class="book-body col-9">
              <div class="body-cover text-start pl-4 mt-4">
                <div class="book-title">
                  <h4 class="fw-bolds p-1 border-bottom">{{ bookDetailforUser.name }}</h4>
                  <h5>Author: {{ bookDetailforUser.author }}</h5>
                  <h5>Genre: {{ bookDetailforUser.genre }}</h5>
                  <div class="price text-start w-100 m-1">
                    <h5>Published: {{ bookDetailforUser.publish_date }}</h5>
                    <h5> Price : {{ bookDetailforUser.price }} </h5>
                  </div>
                  <hr class="border-black border-4">
                </div>
                <div class="book-content">
                  <p>{{ bookDetailforUser.content }}</p>
                </div>
              </div>
            </div>
            
          </div>
        </div>
        <div v-else>
          <p>Loading book details...</p>
        </div>
      </div>
    </div>
    <div class="second-outer-box container my-2">
      <div class="row">
        <div class="col-12">
          <div class="reviews">
            <div class="heading text-start review" v-if="!isEmpty">
              <h3>Reviews</h3>
            </div>
            <div class="heading text-start review" v-else>
              <h3>No reviews yet</h3>
            </div>
            <div class="review text-start" v-for="review in this.reviews" :key="review.id">
              <div class="user text-start font-weight-bold">
                <h6>{{ review.username }}</h6>
                <div class="">
                  <div class="star-rating">
                    <span class="star" v-for="n in 5" :key="n" :class="{ active: n <= review.rating }">★</span>
                  </div>
                </div>
              </div>
              <p class="">{{ review.feedback }}</p>
            </div>
          </div>
        </div>
        <div class="col-2"></div>
      </div>
    </div>
  </template>


  <script>
  import 'core-js/features/array';
  
  export default {
    name: 'SingleBookInfoManager',
    data() {
      return {
        message: '',
        messageType: '',
        isEmpty: true,
        bought_book: false,
        bookId: null,
        bookDetailforUser: null,
        status: '',
        userId: this.$route.params.id,
        items: 3, // Default number of days
        data: {},
        completed_book: [],
        reviews: []
      };
    },

    methods: {
      setMessage(text, type) {
        this.message = text;
        this.messageType = type;
        setTimeout(() => {
          this.message = '';
        }, 3000);
      },
  
      fetchBookData(bookId) {
        const token = sessionStorage.getItem('jwt_token');
        return new Promise((resolve, reject) => {
          fetch(`http://127.0.0.1:5000/api/book/${bookId}` ,
            {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              },
            }
          )
            .then(response => {
              if (response.ok) {
                return response.json();
              } else {
                throw new Error('Failed to fetch book data');
              }
            })
            .then(bookData => {
              this.bookDetailforUser = bookData;
              console.log(this.bookDetailforUser, 'book info');
              resolve(bookData);
            })
            .catch(error => {
              console.error('An error occurred while fetching book data:', error);
              reject(error);
            });
        });
      },


      async getBookFeedback(bookId) {
        const token = sessionStorage.getItem('jwt_token');
        if (!token) {
          this.$router.push('/login');
          return;
        }
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/feedback/${bookId}` ,
            {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              },
            }
           );
          if (response.ok) {
            const data = await response.json();
            this.reviews = data.feedbacks;
            this.isEmpty = false;
            console.log(this.reviews);
          } else {
            console.error('Failed to fetch book feedback');
            this.isEmpty = true;
          }
        } catch (error) {
          console.error('An error occurred while fetching book feedback:', error.message);
        }
      },
  
      
      image_link(src) {
        console.log(src, 'source .......');
        // Adjust this path according to your project structure
        // You might need to update the path to match your actual structure
        let url = `http://127.0.0.1:5000/static/${src}`;
        return url;
      },
  
      add(count) {
        this.items = Math.min(this.items + count, 14);  // Max of 14 days
      },
      minus(count) {
        this.items = Math.max(this.items - count, 1);  // Minimum of 1 day
      },
      readBook() {
        window.open(`http://localhost:5000/static/doctandc.pdf`, '_blank');
      }
      
    },
    mounted() {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      this.bookId = this.$route.query.bookId;
      this.fetchBookData(this.bookId)
      this.getBookFeedback(this.bookId);
    }
  };
  </script>
  
  <style scoped>
  .outer-box {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 90vh;
  }
  
  .container {
    width: auto;
    margin: auto;
  }
  
  .book-info {
    box-shadow: rgba(9, 30, 66, 0.25) 0px 1px 1px, rgba(9, 30, 66, 0.13) 0px 0px 1px 1px;
    background-color: whitesmokes;
    border-radius: 5px;
  }
  
  .image-cover {
    margin: 2rem 0;
  }
  
  .second-outer-box {
    box-shadow: rgba(9, 30, 66, 0.25) 0px 1px 1px, rgba(9, 30, 66, 0.13) 0px 0px 1px 1px;
    background-color: whitesmokes;
    border-radius: 5px;
  }
  
  .reviews {
    background-color: whitesmokes;
    border-radius: 5px;
    padding: 1rem;
  }
  
  .reviews h3 {
    font-weight: bold;
    color: #333;
    margin-bottom: 1rem;
  }
  
  .review {
    background-color: #f9f9f9;
    border-radius: 5px;
    margin-bottom: 1rem;
    padding: 1rem;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 2px 4px;
  }
  
  .review p {
    margin: 0;
    color: #555;
  }
  
  .star-rating {
    display: flex;
  }
  
  .star {
    font-size: 2rem;
    cursor: pointer;
    color: #ccc;
  }
  
  .star.active {
    color: #f39c12;
  }
  </style>
  