<template>
<NavbarSignup></NavbarSignup>


  <div class="container-fluid full-height-container d-flex justify-content-center align-items-center">
    <div class="col-sm-4 border rounded p-4 box">
      <h3 class="mb-4">User Login</h3>
      <form @submit.prevent="login">
        <div class="form-group mb-4">
          <label for="name" class="form-label">User Name</label>
          <input v-model="credential.user_name" type="text" id="name" class="form-control" placeholder="Enter your username" />
        </div>

        <div class="form-group mb-4">
          <label for="password" class="form-label">Password</label>
          <input v-model="credential.user_password" type="password" id="password" class="form-control" placeholder="Enter your password" />
        </div>

        <div class="form-group mb-4">
          <button @click="login" class="btn btn-primary w-100">User Login</button>
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
  name: 'LoginComponent',

  components: {
    NavbarSignup
  },
  
  data() {
    return {
      credential: {
        user_name: null,
        user_password: null,
        role_type: 'user',
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
            'Accept': 'application/json',
            credentials: 'include',
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
        await new Promise(resolve => setTimeout(resolve, 1000));

        this.sucessMsg = 'Logging in...'
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.successMsg = 'Login successful';
        if (role.includes('user')) {
          this.$router.push(`/home/${id}/books`);
        } else {
          this.$router.push('/manager-login');
        }

      } catch (error) {
        console.error('Login failed:', error.message);
      }
    },

  },
  mounted() {
   const token = sessionStorage.getItem('jwt_token');
   if (token) {
     this.$router.push('/home/' + sessionStorage.getItem('user_id') + '/books');
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

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.5rem;
  text-align: left; /* Ensure label is left-aligned */
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

.success-msg {
  background-color: #28a745; /* Bootstrap success color */
  color: white;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
  font-weight: bold;
}

</style>
