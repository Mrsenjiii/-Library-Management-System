// It is for filtering data we are using it.It is like a global variable which will change when we change filters.


import { ref,reactive } from 'vue';
export const productToFilter = ref();

export const filters = reactive({
  // Define your filtesr properties here
  // Example: 
  year : null, // filter by issue date
  priceStart:null, // filter by start price
  endPrice:null, // max price
  section: null, // section of the book
  Author: null , // filter by author name 
  Rating:null, // rating of the book 1 to 5 max
  // Add more filters as needed 
});