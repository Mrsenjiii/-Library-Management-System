import { createRouter, createWebHistory } from 'vue-router';
import UserHome from '../views/Home.vue';
import managerHome from '../views/LibrarianHome.vue';
import SignupComponent from '../components/SignupComponent.vue';
import LoginComponent from '../components/loginComponent.vue';
import managerLogin from '../components/librarianLogin.vue';
import manageGenres from '../components/librarianComponent/manageGenre.vue';
import finishedList from '../components/librarianComponent/usersForAbook/finishedList.vue';
import readingBookList from '../components/librarianComponent/usersForAbook/readingBookList.vue';
import requestList from '../components/librarianComponent/usersForAbook/requestList.vue';
import allRequests from '../components/librarianComponent/allUsersForBooks/allRequests.vue';
import allFinishedBookUsers from '../components/librarianComponent/allUsersForBooks/finishedListAll.vue';
import allReadingUsersList from '../components/librarianComponent/allUsersForBooks/readingListAll.vue';
import requestedUsersList from '../components/librarianComponent/allUsersForBooks/requestListAll.vue';
import returnBook from '../components/UsersComponents/returnBook.vue';
import manageProducts from '../components/librarianComponent/manageBooks.vue';
import addProduct from '../components/librarianComponent/addBook.vue';
import editProduct from '../components/librarianComponent/editBook.vue';
import bookUser from '../components/librarianComponent/usersForAbook/bookUser.vue';
import bookRequest from '../components/librarianComponent/bookRequest.vue';
import userCart from '../components/UsersComponents/userCart.vue';
import userProduct from '../components/UsersComponents/BooksHome.vue';
import readingBooks from '../components/UsersComponents/readingBooks.vue';
import singleBookInfo from '../components/UsersComponents/singleBookInfo.vue';
import requestedBooks from '../components/UsersComponents/requestedbooks.vue';
import finishedBooks from '../components/UsersComponents/finishedBooks.vue';
import singleBookInfoManager from '@/components/librarianComponent/singleBookInfoManager.vue';
import AnalyticsDashboard from '../components/librarianComponent/analysisComponent.vue';

// Define child routes for user
const userChildrens = [
    {
        path: 'books',
        name: 'allBooksUser',
        component: userProduct,
        meta: { requiresAuth: true },
    },
    {
        path: 'book/:book_name',
        name: 'singleBookInfoUser',
        component: singleBookInfo,
        meta: { requiresAuth: true },
    },
    {
        path: 'return_book/:cartId',
        name: 'returnBook',
        component: returnBook,
        meta: { requiresAuth: true },
    },
    {
        path: 'carts',
        name: 'HomeCarts',
        component: userCart,
        meta: { requiresAuth: true },

        children: [
            {
                path: 'requestedBooks',
                name: 'requestedBooks',
                component: requestedBooks,
                meta: { requiresAuth: true },
            },
            {
                path: 'readbooks',
                name: 'readingBooks',
                component: readingBooks,
                meta: { requiresAuth: true },

            },
            {
                path: 'completedbooks',
                name: 'completedBooks',
                component: finishedBooks,
                meta: { requiresAuth: true },

            }
        ]
    }
];

// Define child routes for manager
const librarianComponent = [
    {
        path: 'genres',
        name: 'genresPage',
        component: manageGenres,
        meta: { requiresAuth: true },

        
    },
    {
        path: 'books',
        name: 'booksPage',
        component: manageProducts,
        meta: { requiresAuth: true },

    },
    {
        path: 'editProduct/:productId',
        name: 'productsPageEdit',
        component: editProduct,
        meta: { requiresAuth: true },

    },
    {
        path: 'bookinfo/:book_name',
        name: 'bookInfoMananger',
        component: singleBookInfoManager,
        meta: { requiresAuth: true },

    },
    {
        path: 'addProduct',
        name: 'addProduct',
        component: addProduct,
        meta: { requiresAuth: true },

    },
    {
        path:'analytics',
        name: 'analytics',
        component: AnalyticsDashboard,
        meta: { requiresAuth: true },
    },
    {
        path: 'allrequests',
        name: 'allrequests',
        component: allRequests,
        meta: { requiresAuth: true },
        children: [
            {
                path: 'all-requests-persons',
                name: 'all-requests-persons',
                component: requestedUsersList,
                meta: { requiresAuth: true },
            },
            {
                path: 'all-reading-persons',
                name: 'all-reading-persons',
                component: allReadingUsersList,
                meta: { requiresAuth: true },
            },
            {
                path: 'all-completed-books',
                name: 'all-completed-books',
                component: allFinishedBookUsers,
                meta: { requiresAuth: true },
            }
        ]
    },
    {
        path: 'userBook/:bookId',
        name: 'userBook',
        component: bookUser,
        meta: { requiresAuth: true }, 
        children: [
            {
                path: 'requests-persons',
                name: 'requests-persons',
                component: requestList,
                meta: { requiresAuth: true },
            },
            {
                path: 'reading-persons',
                name: 'reading-persons',
                component: readingBookList,
                meta: { requiresAuth: true },
            },
            {
                path: 'completed-books',
                name: 'completed-books',
                component: finishedList,
                meta: { requiresAuth: true },
            }
        ]
    },
    {
        path: 'bookRequest',
        name: 'bookRequest',
        component: bookRequest,
        meta: { requiresAuth: true },
    },
];




// Define routes
const routes = [
    {
        path: '/signup',
        name: 'signup',
        component: SignupComponent,
        // meta: { requiresAuth: true },
    },
    {
        path: '/librarian-login',
        name: 'librarian-login',
        component: managerLogin,
        // meta: { requiresAuth: true },
    },
    {
        path: '/login',
        name: 'login',
        component: LoginComponent,
        // meta: { requiresAuth: true },
    },
    {
        path: '/home/:id',
        name: 'Home',
        component: UserHome,
        children: userChildrens,
        meta: { requiresAuth: true },
    },
    {
        path: '/librarian/:id',
        component: managerHome,
        children: librarianComponent,
        meta: { requiresAuth: true },
    },

    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('../components/NotFound.vue'),
    }
];

// Create and configure the router
const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

// Navigation guard to check authentication
router.beforeEach((to, from, next) => {
    const token = sessionStorage.getItem('jwt_token');
    
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!token) {
            next('/login');
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;
