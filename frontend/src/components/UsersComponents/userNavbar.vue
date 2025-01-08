<template>
  <nav class="navbar sticky-top navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <h3 class="navbar-brand mx-4">My Library</h3>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li v-if="pageRoute === 'allBooksUser'" class="nav-item mx-2">
            <form @submit.prevent="searchForProduct" class="d-flex" role="search">
              <input class="form-control me-2" type="search" placeholder="Search for products" aria-label="Search"
                v-model="productToFilter">
            </form>
          </li>

          <li v-if="pageRoute === 'allBooksUser'" class="nav-item mx-2">
            <button @click="filterProducts" class="btn btn-outline-secondary" data-bs-toggle="offcanvas" data-bs-target="#offcanvasWithBothOptions">
              Filters
            </button>
          </li>

          <li v-if="pageRoute === 'allBooksUser'" class="nav-item mx-2">
            <router-link :to="{ name: 'requestedBooks' }" class="btn btn-outline-secondary">
              Requests
            </router-link>
          </li>

          <li v-else class="nav-item mx-2">
            <router-link :to="{ name: 'allBooksUser' }" class="btn btn-outline-secondary">
              Home
            </router-link>
          </li>

          <li class="nav-item mx-2">
            <button @click="logout" class="btn btn-outline-secondary">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="offcanvas offcanvas-end" data-bs-scroll="true" tabindex="-1" id="offcanvasWithBothOptions"
    aria-labelledby="offcanvasWithBothOptionsLabel">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title text-center" id="offcanvasWithBothOptionsLabel">Filter Products by your preferences</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>

    <div class="offcanvas-body">
      <form @submit.prevent="applyAllFilters">
        <div class="container mb-3 text-start">
          <label for="sections" class="form-label">Choose a Section:</label>
          <select id="sections" name="sections" class="form-select" v-model="filters.section">
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
          <label for="year" class="form-label">Book Issue Date</label>
          <input type="number" id="year" class="form-control" min="1600" max="2024" v-model="filters.year">
        </div>

        <div class="container mb-3 text-start">
          <button type="submit" class="btn btn-primary">Apply Filters</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { filters, productToFilter } from '../UsersComponents/storeUser';
import { useRoute } from 'vue-router';
import { ref, watchEffect } from 'vue';
import mitt from 'mitt';

export const eventBus = mitt();

export default {
  name: 'userNavbar',
  data() {
    return {
      Sections: null,
      id: this.$route.params.id,
    };
  },
  methods: {
    logout() {
      sessionStorage.clear();
      this.$router.push('/login');
    },
    applyAllFilters() {
      eventBus.emit('applyAllFilters', 'payload loading');
    },
    searchForProduct() {
      eventBus.emit('searchForProduct', 'payload loading');
    },
    filterProducts() {
      eventBus.emit('applyAllFilters', 'payload loading');
    },
  },
  setup() {
    const route = useRoute();
    const pageRoute = ref(route.name);
    watchEffect(() => {
      pageRoute.value = route.name;
    });

    return {
      pageRoute,
      filters,
      productToFilter,
    };
  },
  async mounted() {
    const token = sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    try {
      const response = await fetch('http://127.0.0.1:5000/api/section', {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }

      const data = await response.json();
      this.Sections = data;
    } catch (error) {
      console.error('Error fetching data:', error.message);
    }
  },
};
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
}

.navbar-toggler {
  border-color: rgba(0, 0, 0, 0.1);
}

.navbar-toggler-icon {
  background-image: none;
}

@media (max-width: 767px) {
  .navbar-nav {
    text-align: center;
  }
  .navbar-nav .nav-item {
    margin-bottom: 10px;
  }
  .btn-outline-secondary {
    width: 100%;
  }
}
</style>
