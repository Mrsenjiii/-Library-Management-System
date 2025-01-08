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
          <li v-if="pageRoute === 'booksPage'" class="nav-item mx-2">
            <form @submit.prevent="searchForProduct" class="d-flex" role="search">
              <input class="form-control me-2" type="search" placeholder="Search for books" aria-label="Search"
                v-model="productToFilter">
            </form>
          </li>

          <li v-if="pageRoute === 'genresPage'" class="nav-item mx-2">
            <form @submit.prevent="searchForProduct" class="d-flex" role="search">
              <input class="form-control me-2" type="search" placeholder="Search For Genres" aria-label="Search"
                v-model="sectionToFilter">
            </form>
          </li>

          <li class="nav-item mx-2">
            <button @click="filterproducts()" class="btn btn-outline-secondary">Filters</button>
          </li>

          <li class="nav-item mx-2">
            <router-link :to="'/librarian/' + id + '/allrequests/all-requests-persons'" class="btn btn-outline-secondary">
              All Requests
            </router-link>
          </li>

          <li class="nav-item mx-2">
            <router-link :to="'/librarian/' + id + '/genres'" class="btn btn-outline-secondary">
              Sections
            </router-link>
          </li>

          <li class="nav-item mx-2">
            <router-link :to="'/librarian/' + id + '/analytics'" class="btn btn-outline-secondary">
              Analytics
            </router-link>
          </li>

          <li class="nav-item mx-2">
            <router-link :to="'/librarian/' + id + '/books'" class="btn btn-outline-secondary">
              Books
            </router-link>
          </li>

          <li class="nav-item mx-2">
            <button @click="logout" class="btn btn-outline-secondary">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useRoute } from 'vue-router';
import { ref } from 'vue';
import { productToFilter, sectionToFilter } from './storeManager';
import { watchEffect } from 'vue';
import eventBus from './eventBus';
export default {
  name: 'managerNavbar',
  data() {
    return {
      id: this.$route.params.id,
      productToFilter,
      sectionToFilter,
    };
  },
  methods: {
    logout() {
      sessionStorage.clear();
      this.$router.push('/login');
    },
    filterproducts() {
      eventBus.emit('applyAllFilters', 'payload loading');
    }
  },
  setup() {
    const route = useRoute();
    const pageRoute = ref(route.name);
    watchEffect(() => {
      pageRoute.value = route.name;
    });
    return { pageRoute };
  },
}
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
