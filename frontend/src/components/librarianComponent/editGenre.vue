<template>
  <div class="box d-flex justify-content-center align-items-center bg-primary vh-100">
    <div class="form-box bg-white rounded">
    <div class="d-flex justify-content-end p-2">
        <button type="button" class="btn-close" @click="closeModel" aria-label="Close"></button>
    </div>
    <h5 class="mx-3">Edit Category</h5>
    <div class="fluid-container m-3">
      <label for="name" id="name">Category Name</label>
      <input v-model="section.name" type="text" id="name" class="form-control" />
    </div>
    <div class="fluid-container m-3">
      <label for="sectionDescription" id="sectionDescription">Category Description</label>
      <input v-model="section.description" type="text" id="sectionDescription" class="form-control" placeholder="Enter Category Description">
    </div>
    <div class="fluid-container m-3">
      <button @click="editCategory" class="btn btn-primary w-100">Edit Category</button>
    </div>
    <div class="m-3 text-center">
      <p v-if="error" class="text-danger">*{{ errorMsg }}</p>
      <p v-if="successMsg" class="text-success">{{ successMsg }}</p>
    </div>
  </div>
  </div>
 
</template>

<script>
export default {
  name: 'editCategoryManager',
  props: {
    categoryToEdit: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      section: { ...this.categoryToEdit },
      error: false,
      errorMsg: null,
      successMsg: null
    };
  },
  methods: {
    async editCategory() {
      const token = sessionStorage.getItem('jwt_token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      this.error = false;
      this.successMsg = null;
      try {
        const requestData = {
          name: this.section.name,
          description: this.section.description,
        };
        const url = `http://127.0.0.1:5000/api/section/${this.section.id}`;
        const response = await fetch(url, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          credentials: 'include',
          body: JSON.stringify(requestData)
        });

        if (response.ok) {
          const responseData = await response.json();
          this.successMsg = responseData.message || 'Category edited successfully!';
        } else {
          const errorData = await response.json();
          this.errorMsg = errorData.error || 'Failed to edit category';
          this.error = true;
        }
      } catch (error) {
        this.errorMsg = 'Network error. Please try again later.';
        this.error = true;
      }
    },

    closeModel() {
      this.$emit('close-modal');
    },



  },
  mounted() {
    const token = sessionStorage.getItem('jwt_token');
    if (!token) {
      this.$router.push('/login');
      return;
    }
  }
};
</script>

<style scoped>
.box {
  position: absolute;
  width: 100%;
  height: 90%;
  background-color: rgba(0, 123, 255, 0.1);
  z-index: 21;
}
.form-box {
  max-width: 400px;
  width: 100%;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}
.btn-close {
  background-color: transparent;
  border: none;
  cursor: pointer;
  background-color: rgba(255, 0, 0, 0.552);
  font-size: larger;
}
.form-label {
  text-align: left;
}
</style>