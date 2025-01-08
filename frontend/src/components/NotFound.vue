<template>
    <div class="d-flex justify-content-center align-items-center vh-100">
        <div class="text-center bg-light rounded p-5 shadow">
            <h1>404 - Page Not Found</h1>
            <p>The page you are looking for does not exist.</p>
            <button @click="goBack" class="btn btn-primary mt-3">Go Back</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'NotFound',
    methods: {
        goBack() {
            this.$router.go(-1); // Navigates to the previous page
        }
    }
}
</script>

<style scoped>
.vh-100 {
    height: 100vh;
}
</style>
