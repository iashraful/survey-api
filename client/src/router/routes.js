import Home from '../views/Home.vue'
import middlewares from '../middlewares/middlewares'

export default [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/surveys',
    name: 'SurveyListView',
    component: () => import(/* webpackChunkName: "survey-list" */ '../views/survey/SurveyListView.vue'),
    meta: {
      middleware: [
        middlewares.isAuthenticated
      ]
    }
  },
  {
    path: '/surveys/create',
    name: 'SurveyCreateView',
    component: () => import(/* webpackChunkName: "survey-create" */ '../views/survey/SurveyCreateView.vue'),
    meta: {
      middleware: [
        middlewares.isAuthenticated
      ]
    }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
    meta: {
      middleware: [
        middlewares.isAuthenticated
      ]
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "login" */ '../components/auth/Login.vue'),
    meta: {
      middleware: [
        middlewares.publicOnly
      ]
    }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import(/* webpackChunkName: "signup" */ '../components/auth/Signup.vue'),
    meta: {
      middleware: [
        middlewares.publicOnly
      ]
    }
  }
]