<template>


<NavbarSignup></NavbarSignup>
  <div class="container-fluid full-height-container d-flex justify-content-center align-items-center ">
    <div class="col-sm-4 mx-auto box p-4">
      <h3 class="mb-4">Librarian Login</h3>

      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="name" class="form-label">Librarian Name</label>
          <input v-model="credential.user_name" type="text" id="name" class="form-control" placeholder="Enter your name" />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="credential.user_password" type="password" id="password" class="form-control" placeholder="Enter your password" />
        </div>

        <div class="mb-3">
          <button @click="login" class="btn btn-primary w-100">Login</button>
        </div>

        <div v-if="errorMessage" class="form-group mb-4">
          <div class="btn bg-danger-subtle  w-100">  {{ errorMessage }}</div>
        </div>

        <div v-if="sucessMsg" class="form-group mb-4">
  <div class="success-msg w-100">{{ sucessMsg }}</div>
</div>

      </form>
    </div>
  </div>


</template>

<script>
import NavbarSignup  from './Navbar.vue';
export default {
  name: 'ManagerLogin',
  components: {
    NavbarSignup
  },
  data() {
    return {
      credential: {
        user_name: null,
        user_password: null,
        role_type: 'librarian',
      },
      errorMessage: '',
      sucessMsg:''
    };
  },

  methods: {
    async login() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.credential),
        });

        if (!response.ok) {
          const result = await response.json();
          this.errorMessage = result.error;
          await new Promise(resolve => setTimeout(resolve, 1000));
          this.errorMessage = '';
          throw new Error('Login failed');

        }

        const result = await response.json();
        const { user_role: role, user_id: id, access_token } = result;

        sessionStorage.setItem('jwt_token', access_token);
        sessionStorage.setItem('user_id', id);
        sessionStorage.setItem('user_role', role);
        this.sucessMsg = 'Login Sucessfully';
        await new Promise(resolve => setTimeout(resolve, 1000));

    
        if (role.includes('librarian')) {
          this.$router.push(`/librarian/${id}/genres`);
        } else {
          // this.$router.push(`/home/${id}/books`);
        }

      } catch (error) {
        console.error('Login failed:', error.message);
      }
    },



    
  },

  mounted() {
    if (sessionStorage.getItem('user_id')) {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.full-height-container {
  height: 100vh;
}

.box {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  background-color: #fff;
  padding: 2rem;
  border-radius: 0.5rem;
}

.navbar {
  border-bottom: 2px solid #f8f9fa;
}

.logo-container {
  flex: 1;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.ml-auto {
  margin-left: auto;
}

.btn-outline-light {
  border-color: #fff;
  color: #fff;
}

.btn-outline-light:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #5a6268;
}

.form-label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.5rem;
  text-align: left;
}

.form-control {
  border-radius: 0.25rem;
  border: 1px solid #ced4da;
  box-shadow: none;
}

.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(38, 143, 255, 0.25);
}

.w-100 {
  width: 100%;
}

.text-danger {
  color: #dc3545;
}

.mb-3 {
  margin-bottom: 1rem;
}

.success-msg {
  background-color: #28a745; /* Bootstrap success color */
  color: white;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
  font-weight: bold;
}

</style>
