<template>
  <div class="outer-box">
    <div class="container book-info p-2">
      <div v-if="bookDetailforUser" class="container">
        <div class="row">
          <div class="book-image col-3 p-0">
            <div class="image-cover p-0 d-inline-block my-1">
              <img :src="image_link(this.bookDetailforUser.book_loc_url)" class="w-100" alt="Image not found">
              <div class="price text-start w-100 m-1">
              </div>
            </div>


            <div class="container m-0 p-0">
              <div class="row align-items-center" v-if="status === 'Not Requested'">
                <div class="col-auto">
                  <button type="button" class="btn btn-primary" @click="requestBook(userId, bookId)">Request
                    Book</button>
                </div>
                
                <div class="col-auto d-flex align-items-center bg-light rounded p-2">
                  <span style="font-size: 0.9rem; margin-right: 8px;">Days: {{ items }}</span>
                  <button class="btn btn-outline-danger btn-sm mx-1" :disabled="items >= 14" @click="add(1)">+</button>
                  <button class="btn btn-outline-danger btn-sm mx-1" :disabled="items <= 1" @click="minus(1)">-</button>
                </div>
              </div>

              <div class="read-and-return container d-flex flex-row-start" v-else-if="status === 'Approved'">
                <button type="button" class="btn btn-success col-4 m-1" style="font-size: 1rem"
                  @click="readBook(this.bookDetailforUser.book_pdf_loc_url)">Read</button>
                <button type="button" class="btn btn-warning col-4 m-1" style="font-size:1rem"
                  @click="returnBook(this.data.cart_id)">Return</button>
              </div>
              <div class="other-button col-auto d-flex align-items-start m-1" v-else>
                <button type="button" class="btn btn-warning" @click="deleteCart(userId, bookId)">Cancel
                  Request</button>
              </div>
            </div>
          </div>
          <div class="book-body col-6">
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
          <div class="book-others col-3 border">
            <div class="history-box fluid-container text-start m-2">
              <div class="heading text" v-if="bought_book">
                <h4>History</h4>
              </div>
              <div class="heading text" v-else>
                <h4>No History</h4>
              </div>
              <div class="history">
                <div class="history-inner-box text-start review" v-for="book_history in completed_book"
                  :key="book_history.id">
                  <p><strong>Issued: </strong>{{ book_history.date_issued }}</p>
                  <p><strong>Returned: </strong> {{ book_history.return_date }}</p>
                </div>
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
  name: 'SingleBookInfo',
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



    async getCompletedBook(userId, bookName) {
      console.log('in the get completed book');
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/completedbook/${userId}/${bookName}`
          , {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
          }
        );
        if (response.ok) {
          const data = await response.json();
          this.completed_book = data.completed_book;
          console.log(this.completed_book, 'completed book');
          this.completed_book.map((book) => {
            book.date_issued = new Date(book.date_issued).toDateString();
            book.return_date = new Date(book.return_date).toDateString();

          });
          if (this.completed_book.length > 0) {
            this.bought_book = true;
          }
        } else {
          console.error('Failed to fetch completed book data');
        }
      } catch (error) {
        console.error('An error occurred while fetching completed book data:', error.message);
      }
    },


    fetchBookData() {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      return new Promise((resolve, reject) => {
        fetch(`http://127.0.0.1:5000/api/book/${this.bookId}`
          , {
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

    async getUserCarts(userId, bookId) {
      try {
        const token = sessionStorage.getItem('jwt_token');
        if (!token) {
          this.$router.push('/login');
          return;
        }
        const response = await fetch(`http://127.0.0.1:5000/api/users/${userId}/carts/${bookId}`
          , {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
          }
        );
        if (response.ok) {
          const data = await response.json();
          this.data = data;
          this.status = data.cart_id ? (data.approved ? 'Approved' : 'Not Approved') : 'Not Requested';
          console.log(this.data, 'cart info ');
        } else {
          console.error('Failed to fetch user carts');
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

  const proceed = confirm('Are you sure you want to request this book?');
  if (!proceed) return;

  try {
    const dateIssued = new Date();
    const dateEnd = new Date();
    dateEnd.setDate(dateIssued.getDate() + this.items);

    const response = await fetch(`http://127.0.0.1:5000/api/users/${userId}/carts/${bookId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ date_issued: dateIssued, date_end: dateEnd }),
    });

    if (response.ok) {
      console.log('Book request successful:', await response.json());
      this.status = 'Not Approved';
    } else {
      console.error('Network response was not ok');
    }
  } catch (error) {
    console.error('Error requesting book:', error);
  }
},

    async getBookFeedback(bookId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) { 
        this.$router.push('/login');
        return;
      }
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/feedback/${bookId}`
          , {
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
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
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


    returnBook(cartId) {
      this.$router.push({ name: 'returnBook', params: { cartId: cartId } });
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
    readBook(src) {
      window.open(`http://localhost:5000/static/${src}`, '_blank');}
  },
  mounted() {
    const token = sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
    }


    this.bookId = this.$route.query.bookId;
    this.fetchBookData().then(bookData => {
      this.getCompletedBook(this.userId, bookData.name);
    }).catch(error => {
      console.error('Failed to fetch book data:', error);
    });
    this.getUserCarts(this.userId, this.bookId);
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
