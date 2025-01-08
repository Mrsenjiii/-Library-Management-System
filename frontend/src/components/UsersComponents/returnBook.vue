<template>
    <div class="box d-flex justify-content-center align-items-center vh-100">
        <div class="form-box rounded p-4">
            <div class="d-flex justify-content-end">
                <button type="button" class="btn-close" @click="closeModel" aria-label="Close"></button>
            </div>

            <h5 class="text-start mb-4">User Feedback Form</h5>

            <div class="mb-3">
                <label for="rating" class="form-label">Rating</label>
                <div class="star-rating" @mouseover="hoverStar" @mouseout="leaveStar" @click="rateStar">
                    <span class="star" v-for="n in 5" :key="n" :data-value="n"
                        :class="{ active: n <= rating || n <= hoverRating }">★</span>
                </div>
                <p v-if="error && rating === 0" class="text-danger">* Rating is required</p>
            </div>

            <div class="mb-3">
                <label for="feedback" class="form-label">Your Feedback:</label>
                <textarea id="feedback" v-model="feedback" name="feedback" rows="4" class="form-control"
                    placeholder="Enter your feedback here..."></textarea>
                <p v-if="error && !feedback.trim()" class="text-danger">* Feedback is required</p>
            </div>

            <div class="mb-3">
                <button @click="submitFeedback" class="btn btn-primary w-100">Submit Feedback</button>
            </div>

            <div class="text-center">
                <p v-if="error" class="text-danger">{{ errorMsg }}</p>
                <p v-if="success" class="text-success">{{ successMsg }}</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'returnBook',
    data() {
        return {
            feedback: '',
            rating: 0,
            hoverRating: 0,
            error: false,
            errorMsg: null,
            successMsg: null,
            success: false,
            cartId: this.$route.params.cartId
        };
    },
    methods: {
        closeModel() {
            this.$router.go(-1);
        },
        hoverStar(event) {
            this.hoverRating = parseInt(event.target.getAttribute('data-value'), 10);
        },
        leaveStar() {
            this.hoverRating = 0;
        },
        rateStar(event) {
            this.rating = parseInt(event.target.getAttribute('data-value'), 10);
        },
        resetForm() {
            this.feedback = '';
            this.rating = 0;
            this.hoverRating = 0;
            this.error = false;
            this.errorMsg = null;
            this.successMsg = null;
            this.success = false;
        },
        async submitFeedback() {    
            const token = sessionStorage.getItem('jwt_token');
            if (!token) {
                this.$router.push('/login');
                return;
            }

            // Reset previous messages
            this.error = false;
            this.success = false;
            this.errorMsg = null;
            this.successMsg = null;

            // Validate input
            if (!this.feedback.trim()) {
                this.error = true;
                this.errorMsg = "Feedback is required.";
                return;
            }
            if (this.rating === 0) {
                this.error = true;
                this.errorMsg = "Rating is required.";
                return;
            }

            try {
                const feedback = {
                    rating: this.rating,
                    feedback: this.feedback
                };

                const url = `http://127.0.0.1:5000/api/return_book/${this.cartId}`;
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(feedback),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    this.errorMsg = errorData.message || 'Network error. Please try again later.';
                    this.error = true;
                    throw new Error(`HTTP error! status: ${response.status}, message: ${this.errorMsg}`);
                } else {
                    this.resetForm(); // Clear form after successful submission
                    this.successMsg = 'Feedback submitted successfully!';
                    this.success = true;
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    this.$emit('close-modal'); // Emit event to close the modal if necessary
                    this.$router.go(-1);
                }
            } catch (error) {
                console.error('Error submitting feedback:', error);
                this.error = true;
                this.errorMsg = 'An error occurred while submitting feedback. Please try again.';
            }
        }
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
    height: 100%;
    background-color: rgb(53, 120, 227);
    z-index: 21;
}

.form-box {
    max-width: 400px;
    background-color: white;
    width: 100%;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.btn-close {
    background-color: transparent;
    border: none;
    cursor: pointer;
    color: rgba(255, 0, 0, 0.8);
    font-size: larger;
}

.form-label {
    text-align: left;
    margin-bottom: 0.5rem;
    font-weight: bold;
}

.star-rating {
    font-size: 1.5rem;
    display: flex;
}

.star {
    cursor: pointer;
    transition: color 0.2s;
    color: #ccc;
    font-size: 2.5rem;
}

.star.active {
    color: gold;
}

.star:hover {
    color: gold;
}

textarea {
    resize: vertical;
}

.text-danger {
    color: red;
}

.text-success {
    color: green;
}
</style>
