<template>
    <div class="fluid-container text-start ">
    <div class="container d-flex justify-content-start">
      <div class="heading w-50  border-bottom border-secondary border-3" >
        <h3>My Finished Books</h3>
      </div>
    </div>
  </div>
  <div class="container-fluid my-4">
    <div class="container d-flex justify-content-start">
      <table class="table table-hover bg-warning-subtle">
        <thead>
          <tr class="bg-info-subtle">
            <th class=" bg-secondary" scope="col">Book Name</th>
            <th class="bg-secondary" scope="col">Finished In</th>
            <th class="bg-secondary" scope="col">Date Issued</th>
          </tr>
        </thead>
        <tbody>
          <!-- {{ data }} -->
          <tr v-if="isObjectEmpty(data)">
            <td  class="align-middle p-4 text-start fs-4" colspan="4">NO FINISHED BOOKS </td>
          </tr>

          <tr v-for="book in this.data" :key="book.id">
            <td class="align-middle">{{ book.book_name }}</td>
            <td class="align-middle">{{ calculateDays(book.date_issued, book.return_date) }}</td>
            <td class="align-middle">{{ book.date_issued }}</td>

            <!-- <td class="align-middle">
              <button class="btn btn-warning" @click="deleteBook(book.id)">Cancel Request</button>
            </td> -->
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'finishedBooks',

  data() {
    return {
      userId: this.$route.params.id,
      data: {},
    };
  },


  methods: {
    async getUserCompletedBooks(userId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const url = `http://127.0.0.1:5000/api/completedbooks/${userId}`;
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
        this.data = responseData.completed_books;
        this.data.map(book => {
          book.date_issued = new Date(book.date_issued).toLocaleDateString();
          book.return_date = new Date(book.return_date).toLocaleDateString();
        })

      } catch (error) {
        console.error('Error getting user completed books:', error);
        throw error;
      }
    },

    async deleteBook(bookId) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/completedbooks/${this.userId}?id=${bookId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const errorMessage = await response.text();
          throw new Error(`Failed to delete book: ${errorMessage}`);
        }

        // Remove the deleted book from the list
        this.data.completed_books = this.data.completed_books.filter(book => book.id !== bookId);
      } catch (error) {
        console.error('Error deleting book:', error);
        throw error;
      }
    },

    isObjectEmpty(obj) {
      const keys = Object.keys(obj);
      return keys.length === 0;
    },

    calculateDays(startDate, endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      const differenceInTime = end.getTime() - start.getTime();
      const differenceInDays = differenceInTime / (1000 * 3600 * 24);
      return differenceInDays;
    }
  },

  mounted() {
    const token =   sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    this.getUserCompletedBooks(this.userId);
  }
};
</script>