<template>

  <NavbarSignup></NavbarSignup>


  <div class="container-fluid full-height-container d-flex justify-content-center align-items-center">
    <div class="row align-items-center w-100">
      <div class="col-sm-4 mx-auto box p-4">
        <h3 class="mb-4">Signup</h3>

        <form @submit.prevent="signup">
          <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input class="form-control" v-model="credential.user_name" type="text" id="name" placeholder="Enter your name" />
          </div>

          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input class="form-control" v-model="credential.email" type="email" id="email" placeholder="Enter your email" />
            <div v-if="emailError" class="password-criteria">
              <ul class="list-unstyled p-0">
                <li class="text-danger bg-danger-subtle p-2">{{ emailError }}</li>
              </ul>
            </div>
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input class="form-control" v-model="credential.user_password" type="password" id="password" placeholder="Enter your password" @input="updatePasswordCriteria" />
            <div v-if="showPasswordCriteria" class="password-criteria">
              <ul class="list-unstyled p-0">
                <li v-if="!criteria.length" class="text-danger bg-danger-subtle p-2">At least 8 characters</li>
                <li v-else-if="!criteria.uppercase" class="text-danger bg-danger-subtle p-2">At least one uppercase letter</li>
                <li v-else-if="!criteria.lowercase" class="text-danger bg-danger-subtle p-2">At least one lowercase letter</li>
                <li v-else-if="!criteria.digit" class="text-danger bg-danger-subtle p-2">At least one digit</li>
                <li v-else-if="!criteria.specialChar" class="text-danger bg-danger-subtle p-2">At least one special character</li>
              </ul>
            </div>
          </div>

          <button type="submit" class="btn btn-primary w-100">Signup</button>

          <div v-if="errorMessage" class="password-criteria">
            <ul class="list-unstyled p-0">
              <li class="text-danger bg-danger-subtle p-2">{{ errorMessage }}</li>
            </ul>
          </div>
          <div v-if="success" class="password-criteria">
            <ul class="list-unstyled p-0">
              <li class="text-success bg-success-subtle p-2">{{ successMsg }}</li>
            </ul>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import NavbarSignup  from './Navbar.vue';
export default {
  name: 'SignupComponent',
  components: {
    NavbarSignup
  },
  data() {
    return {
      credential: {
        user_name: '',
        user_password: '',
        email: '',
        active: true,
        user_role: 'user'
      },
      errorMessage: '',
      successMsg: '',
      success: false,
      emailError: '',
      showPasswordCriteria: false,
      criteria: {
        length: false,
        uppercase: false,
        lowercase: false,
        digit: false,
        specialChar: false
      }
    };
  },

  methods: {
    isValidEmail(email) {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailPattern.test(email);
    },

    updatePasswordCriteria() {
      const password = this.credential.user_password;
      this.criteria.length = password.length >= 8;
      this.criteria.uppercase = /[A-Z]/.test(password);
      this.criteria.lowercase = /[a-z]/.test(password);
      this.criteria.digit = /\d/.test(password);
      this.criteria.specialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    },

    async signup() {
      this.showPasswordCriteria = true;
      this.success = false;
  
      if (!this.isValidEmail(this.credential.email)) {
        this.emailError = 'Invalid email format';
        return;
      } else {
        this.emailError = '';
      }

      this.updatePasswordCriteria();

      if (!Object.values(this.criteria).every(Boolean)) {
        this.errorMessage = 'Password does not meet criteria';
        return;
      } else {
        this.errorMessage = '';
      }

      try {
        const response = await fetch('http://127.0.0.1:5000/api/signup', {
          method: 'POST',
          headers: {
            credentials: 'include',
            'Content-Type': 'application/json',

          },
          body: JSON.stringify(this.credential),
        });

        if (!response.ok) {
          const errorData = await response.json();
          this.errorMessage = errorData.error;
          throw new Error('Signup failed');
        }
      
        this.successMsg = 'Signing Up...';
        this.success = true;
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        this.successMsg = 'Signup successful';
        await new Promise(resolve => setTimeout(resolve, 1000));

        this.$router.push('/login');
      } catch (error) {
        console.error('Signup failed:', error.message);
      }
    },

    // managerLogin() {
    //   this.$router.push('/manager-login');
    // },

    // userLogin() {
    //   this.$router.push('/login');
    // }
  },

  mounted() {
    let user = sessionStorage.getItem('user_id');
    if (user) {
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

.form-group {
  margin-bottom: 1.5rem;
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

.text-success {
  color: #28a745;
}

.password-criteria {
  margin-top: 0.5rem;
}

.password-criteria ul {
  padding: 0;
  margin: 0;
  list-style-type: none;
}

.password-criteria li {
  width: 100%;
  padding: 0.5rem;
  text-align: center;
}

.bg-danger-subtle {
  background-color: #f8d7da;
}

.bg-success-subtle {
  background-color: #d4edda;
}

.mb-3 {
  margin-bottom: 1rem;
}
</style>
