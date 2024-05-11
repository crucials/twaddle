import RecordPage from '@/pages/record-page.vue'
import HomePage from '@/pages/home-page.vue'
import TranscribeFromFilePage from '@/pages/transcribe-from-file-page.vue'
import { createRouter, createWebHashHistory } from 'vue-router'

export const routes = [
    { path: '/', component: HomePage, name: 'spoken-words-counter' },
    { path: '/record', component: RecordPage, name: 'record and transcribe' },
    {
        path: '/transcribe-from-file',
        component: TranscribeFromFilePage,
        name: 'transcribe from file',
    },
]

export const router = createRouter({
    history: createWebHashHistory(),
    routes
})
