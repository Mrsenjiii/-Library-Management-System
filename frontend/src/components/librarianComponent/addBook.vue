<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-12">
        <div class="card shadow-sm border">
          <div class="card-body">
            <h2 class="card-title mb-4 text-center">Add Book</h2>
            <form @submit.prevent="addBook" class="needs-validation" novalidate>
              <div class="row text-start p-2">
                <!-- First Column: Book Name, Author, Section -->
                <div class="col-md-6 mb-3">
                  <label for="bookName" class="form-label">Book Name</label>
                  <input v-model="book_data.name" type="text" class="form-control" id="bookName" required>
                  <div class="invalid-feedback" v-if="errors.name">{{ errors.name }}</div>
                </div>

                <div class="col-md-6 mb-3">
                  <label for="bookAuthor" class="form-label">Book Author</label>
                  <input v-model="book_data.author" type="text" class="form-control" id="bookAuthor" required>
                  <div class="invalid-feedback" v-if="errors.author">{{ errors.author }}</div>
                </div>

                <div class="col-md-6 mb-3">
                  <label for="sectionSelect" class="form-label">Select Section</label>
                  <select v-model="book_data.section_id" class="form-select" id="sectionSelect" required>
                    <option value="" disabled>Select a Section</option>
                    <option v-for="section in sections" :key="section.id" :value="section.id">
                      {{ section.name }}
                    </option>
                  </select>
                  <div class="invalid-feedback" v-if="errors.section_id">{{ errors.section_id }}</div>
                </div>

                <!-- Second Column: Price, Content -->
                <div class="col-md-6 mb-3">
                  <label for="bookPrice" class="form-label">Book Price</label>
                  <input v-model.number="book_data.price" type="number" class="form-control" id="bookPrice" min="0" step="0.01" required>
                  <div class="invalid-feedback" v-if="errors.price">{{ errors.price }}</div>
                </div>

                <div class="col-md-12 mb-3">
                  <label for="bookContent" class="form-label">Book Content</label>
                  <textarea v-model="book_data.content" class="form-control" id="bookContent" rows="3" required></textarea>
                  <div class="invalid-feedback" v-if="errors.content">{{ errors.content }}</div>
                </div>

                <!-- Image and PDF Upload -->
                <div class="col-md-6 mb-3">
                  <label for="bookImage" class="form-label">Upload Book Image</label>
                  <input type="file" class="form-control" id="bookImage" ref="imageFile" accept="image/*" required>
                  <div class="invalid-feedback" v-if="errors.imageFile">{{ errors.imageFile }}</div>
                </div>

                <div class="col-md-6 mb-3">
                  <label for="bookPDF" class="form-label">Upload Book PDF</label>
                  <input type="file" class="form-control" id="bookPDF" ref="pdfFile" accept=".pdf" required>
                  <div class="invalid-feedback" v-if="errors.pdfFile">{{ errors.pdfFile }}</div>
                </div>

                <!-- Publish Date -->
                <div class="col-md-6 mb-3">
                  <label for="publishDate" class="form-label">Publish Date</label>
                  <input v-model="book_data.publish_date" type="date" class="form-control" id="publishDate" required>
                  <div class="invalid-feedback" v-if="errors.publish_date">{{ errors.publish_date }}</div>
                </div>
              </div>
              <div class="row text-start p-2">
                <div class="col-md-12 text-center">
                  <button type="submit" class="btn btn-primary">Add Book</button>
                </div>
                <div class="col-md-12 text-center mt-3">
                  <div v-if="serverMessage" class="alert alert-info">{{ serverMessage }}</div>
                  <div v-if="serverErrorMessage" class="alert alert-danger">{{ serverErrorMessage }}</div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AddBookForm",
  data() {
    return {
      book_data: {
        name: "",
        author: "",
        section_id: "",
        price: null,
        content: "",
        publish_date: ""
      },
      sections: [],
      errors: {
        name: "",
        author: "",
        section_id: "",
        price: "",
        content: "",
        imageFile: "",
        pdfFile: "",
        publish_date: ""
      },
      serverMessage: "",
      serverErrorMessage: ""
    };
  },

  methods: {
    validateForm() {
      const today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format

      this.errors = {
        name: this.book_data.name ? "" : "Please enter a book name.",
        author: this.book_data.author ? "" : "Please enter the author's name.",
        section_id: this.book_data.section_id ? "" : "Please select a section.",
        price: this.book_data.price != null && this.book_data.price >= 0 ? "" : "Please enter a valid book price.",
        content: this.book_data.content ? "" : "Please enter book content.",
        imageFile: this.$refs.imageFile.files.length > 0 ? "" : "Please upload an image file.",
        pdfFile: this.$refs.pdfFile.files.length > 0 ? "" : "Please upload a PDF file.",
        publish_date: this.book_data.publish_date
          ? (this.book_data.publish_date > today ? "Publish date cannot be in the future." : "")
          : "Please select a publish date."
      };

      return !Object.values(this.errors).some(error => error);
    },

    async addBook() {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      if (!this.validateForm()) {
        console.log("Form validation errors:", this.errors);
        return;
      }

      console.log('Form data is valid:', this.book_data);
      const formData = new FormData();
      formData.append('name', this.book_data.name);
      formData.append('author', this.book_data.author);
      formData.append('section_id', this.book_data.section_id);
      formData.append('price', this.book_data.price);
      formData.append('content', this.book_data.content);
      formData.append('publish_date', this.book_data.publish_date);
      formData.append('book_pdf', this.$refs.pdfFile.files[0]);
      formData.append('book_image', this.$refs.imageFile.files[0]);
      try {
        const response = await fetch('http://127.0.0.1:5000/api/book', {
          headers: {
            'Authorization': `Bearer ${token}`
            
          },
  
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          this.serverMessage = "Book added successfully";
          this.errors = {}; // Clear errors
          this.book_data = {
            name: "",
            author: "",
            section_id: "",
            price: null,
            content: "",
            publish_date: ""
          };
          this.$refs.pdfFile.value = null;
          this.$refs.imageFile.value = null;
        } else {
          const error = await response.json();
          this.serverErrorMessage = error.message || "Failed to add book";
          console.error("Server error:", error);
        }
      } catch (error) {
        this.serverErrorMessage = "An unexpected error occurred: " + error.message;
        console.error("Unexpected error:", error);
      }
    }
  },

  async mounted() {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/section' ,
        {
          headers: {
            'Authorization': `Bearer ${sessionStorage.getItem('jwt_token')}`
          }
        }
      );
      if (!response.ok) {
        throw new Error('Failed to fetch sections');
      }
      this.sections = await response.json();
    } catch (error) {
      console.error('Error fetching sections:', error.message);
    }
  }
};
</script>

<style scoped>
.card {
  border-radius: 10px;
  border: none;
  padding: 1rem;
}

.btn {
  width: 100%;
  font-size: 1rem;
  padding: 0.75rem 0;
}

.form-label {
  font-weight: 500;
}

.form-control {
  border-radius: 5px;
}

.container {
  max-width: 1000px; /* Increased the container width */
}

.invalid-feedback {
  display: block;
  color: #dc3545; /* Bootstrap danger color */
}

@media (min-width: 768px) {
  .row > .col-md-6 {
    flex: 0 0 50%;
    max-width: 50%;
  }
}
</style>
