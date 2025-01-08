<template>
  <managerNavbar />

  <router-view>

  </router-view>

  <div>

  </div>
</template>
  
<script>
import managerNavbar from "../components/librarianComponent/librarianNavbar.vue"

export default {
  name: 'managerHome',
  data() {
    return {

    }

  },
  components: {
    managerNavbar
  },
  methods: {

  }
};
</script>