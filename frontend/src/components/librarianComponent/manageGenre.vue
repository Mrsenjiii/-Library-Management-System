<template>
  <h1>{{ sectionToFilter }}</h1>
  <editCategoryManager v-if="showEditCategory" @close-modal="closeEditModel(false)" :showEditCategory="showEditCategory" :categoryToEdit="categoryToEdit" />
  <addCategoryManager @close-modal="addCategory(false)" v-if="showAddCategory" />


  <div class="container-fluid border-primary p-5">
    <div class="w-75">
      <table class="table table-hover">
        <thead>
          <tr>
            <th class="bg-info" scope="col">Genre Name</th>
            <th class="bg-info" scope="col">Number of Books</th>
            <th class="bg-info" scope="col">Action Edit</th>
            <th class="bg-info" scope="col">Action Delete</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="genre in filteredGenres" :key="genre.id">
            <td class="align-middle">{{ genre.name }}</td>
            <td class="align-middle">{{ genre.number_of_books }}</td>
            <td class="align-middle">
              <button class="btn btn-warning" @click="handleDelete(genre.id)">Delete Genre</button>
            </td>
            <td class="align-middle">
              <button class="btn btn-secondary" @click="editCategory(genre)">Edit Category</button>
            </td>
          </tr>
          
        </tbody>
      </table>
    </div>
  </div>



  <div @click="addCategory(true)" class="fixed-button">
    <button class="round-button bg-light text-black">+</button>
  </div>
</template>

<script>
import editCategoryManager from './editGenre.vue'
import addCategoryManager from './addGenre.vue'
import { sectionToFilter } from './storeManager';

export default {
  name: 'manageGenres',
  data() {
    return {
      genres: [],
      sectionToFilter,
      showAddCategory: false,
      showEditCategory: false,
      categoryToEdit: null,
    }
  },
  components: {
    editCategoryManager,
    addCategoryManager
  },
  computed: {
    filteredGenres() {
      const regex = new RegExp(this.sectionToFilter, 'i');
      return this.genres.filter(genre => regex.test(genre.name));
    }
  },
  methods: {
    async handleDelete(id) {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const url = `http://127.0.0.1:5000/api/section/${id}`;
        const response = await fetch(url, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });
        if (response.ok) {
          console.log('Section deleted successfully');
          this.genres = this.genres.filter(genre => genre.id !== id);
        } else {
          const errorData = await response.json();
          console.error('Failed to delete section:', errorData.error); 
        }
      } catch (error) {
        console.error('Error deleting section:', error);
      }
    },

    editCategory(data) {
      if (!this.showAddCategory && !this.showEditCategory) {
        this.showEditCategory = true;
        this.categoryToEdit = data;
      } else if (!this.showAddCategory && this.showEditCategory) {
        if (this.categoryToEdit.category_id === data.category_id) {
          this.showEditCategory = false;
          this.categoryToEdit = null;
        } else {
          this.showEditCategory = false;
          this.categoryToEdit = data;
          this.showEditCategory = true;
        }
      } else {
        this.showAddCategory = false;
        this.categoryToEdit = data;
        this.showEditCategory = true;
      }
    },
    addCategory(flag) {
      this.showAddCategory = flag;
    },
    closeEditModel(flag) {
      this.showEditCategory = flag;
    }
  },
  async mounted() {
    const token = sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    try {
      const response = await fetch('http://127.0.0.1:5000/api/section'
        , {
          headers: {
            'Authorization': `Bearer ${token}`}
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }

      const data = await response.json();
      this.genres = data;
    } catch (error) {
      console.error('Error fetching data:', error.message);
    }
  },

}
</script>

<style scoped>
.style_css {
  background-color: #D9D9D9;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.4);
}

#addManagerCategory {
  border: 1px solid maroon;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  transform: translate(-50%, -50%);
  width: auto;
  top: 300px;
}

.fixed-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 20;
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
</style>
