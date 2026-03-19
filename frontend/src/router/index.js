import {createRouter, createWebHistory} from 'vue-router'
import Home from '../views/Main/Home.vue'
import Articles from '../views/Main/Articles.vue'
import Projects from '../views/Main/Projects.vue'
import Project from '../views/Main/Project.vue'
import Tools from '../views/Main/Tools.vue'
import Resources from '../views/Main/Resources.vue'
import AboutMe from '../views/Main/AboutMe.vue'
import Diary from '../views/Main/Diary.vue'
import Todo from '../views/Main/Todo.vue'
import AdminLogin from '@/views/admin/AdminLogin.vue'
import Dashboard from '@/views/admin/Dashboard.vue'
import ProjectManagement from '@/views/admin/ProjectManagement.vue'
import ArticleManagement from '@/views/admin/ArticleManagement.vue'
import ToolManagement from '@/views/admin/ToolManagement.vue'
import ResourceManagement from '@/views/admin/ResourceManagement.vue'
import DiaryManagement from '@/views/admin/DiaryManagement.vue'
import TodoManagement from '@/views/admin/TodoManagement.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/about',
        name: 'AboutMe',
        component: AboutMe
    },
    {
        path: '/articles',
        name: 'Articles',
        component: Articles
    },
    {
        path: '/articles/:slug+',
        name: 'Article',
        component: () => import('@/views/Main/Article.vue'),
        meta: {title: '文章详情'}
    },
    {
        path: '/projects',
        name: 'Projects',
        component: Projects
    },
    {
        path: '/projects/:slug',
        name: 'Project',
        component: Project
    },
    {
        path: '/diary',
        name: 'Diary',
        component: Diary
    },
    {
        path: '/todo',
        name: 'Todo',
        component: Todo
    },
    {
        path: '/tools',
        name: 'Tools',
        component: Tools
    },
    {
        path: '/resources',
        name: 'Resources',
        component: Resources
    },
    {
        path: '/admin/login',
        name: 'AdminLogin',
        component: AdminLogin,
        meta: {title: '管理员登录'}
    },
    {
        path: '/admin',
        component: Dashboard,
        meta: {title: '管理后台'},
        children: [
            {
                path: 'dashboard',
                name: 'AdminDashboard',
                component: () => import('@/views/admin/Dashboard.vue'),
                meta: {title: '管理后台控制台'}
            },
            {
                path: 'projects',
                name: 'ProjectManagement',
                component: ProjectManagement,
                meta: {title: '项目管理'}
            },
            {
                path: 'articles',
                name: 'ArticleManagement',
                component: ArticleManagement,
                meta: {title: '文章管理'}
            },
            {
                path: 'tools',
                name: 'ToolManagement',
                component: ToolManagement,
                meta: {title: '工具管理'}
            },
            {
                path: 'resources',
                name: 'ResourceManagement',
                component: ResourceManagement,
                meta: {title: '资源管理'}
            },
            {
                path: 'diaries',
                name: 'DiaryManagement',
                component: DiaryManagement,
                meta: {title: '日记管理'}
            },
            {
                path: 'todos',
                name: 'TodoManagement',
                component: TodoManagement,
                meta: {title: '待办管理'}
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
    // 设置页面标题
    if (to.meta && to.meta.title) {
        document.title = `${to.meta.title} - 卟瓿钚的布罗格`
    } else {
        document.title = '卟瓿钚的布罗格'
    }

    // 检查是否访问管理后台路由(除了登录页面)
    if (to.path.startsWith('/admin') && to.path !== '/admin/login') {
        // 检查是否已登录
        const token = localStorage.getItem('admin_token')
        const isLoggedIn = localStorage.getItem('admin_logged_in') === 'true'

        if (!token || !isLoggedIn) {
            // 未登录，重定向到登录页
            next({
                path: '/admin/login',
                query: {redirect: to.fullPath}
            })
        } else {
            // 已登录，继续访问
            next()
        }
    } else {
        // 不是管理后台路由或者是登录页，直接访问
        next()
    }
})

export default router
