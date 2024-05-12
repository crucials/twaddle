<script setup lang="ts">
import { RouterView, useRoute, useRouter } from 'vue-router'
import Notifications from '@/components/notifications.vue'

const route = useRoute()
const router = useRouter()
</script>

<template>
    <div>
        <header
            class="px-6 py-5 sm:px-5 sm:py-4 flex items-center gap-x-9 mb-10
                border-b-2 border-b-neutral-100"
        >
            <svg class="w-14" viewBox="0 0 78 78" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M74.9684 62.5466L64.6872 72.8199L54.406 62.5466L44.1248 72.8199L33.8436 62.5466L23.5624 72.8199L3 52.2733L13.2812 42L23.5624 52.2733L33.8436 42L44.1248 52.2733L54.406 42L74.9684 62.5466Z"
                    fill="#1B1B1B" />
                <path
                    d="M74.9684 25.5466L64.6872 35.8199L54.406 25.5466L44.1248 35.8199L33.8436 25.5466L23.5624 35.8199L3 15.2733L13.2812 5L23.5624 15.2733L33.8436 5L44.1248 15.2733L54.406 5L74.9684 25.5466Z"
                    fill="#8B8B8B" />
            </svg>

            <nav class="flex items-center gap-x-4">
                <button v-if="route.path !== '/'" @click="router.back()">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="40px" height="40px"
                        viewBox="0 0 512 512"
                        xml:space="preserve"
                    >
                        <g id="Layer_1"/>
                        <g id="Layer_2"><g>
                        <path class="st0" fill="black" d="M217,129.88c-6.25-6.25-16.38-6.25-22.63,0L79.61,244.64c-0.39,0.39-0.76,0.8-1.11,1.23    c-0.11,0.13-0.2,0.27-0.31,0.41c-0.21,0.28-0.42,0.55-0.62,0.84c-0.14,0.21-0.26,0.43-0.39,0.64c-0.14,0.23-0.28,0.46-0.41,0.7    c-0.13,0.24-0.24,0.48-0.35,0.73c-0.11,0.23-0.22,0.45-0.32,0.68c-0.11,0.26-0.19,0.52-0.28,0.78c-0.08,0.23-0.17,0.46-0.24,0.69    c-0.09,0.29-0.15,0.58-0.22,0.86c-0.05,0.22-0.11,0.43-0.16,0.65c-0.08,0.38-0.13,0.76-0.17,1.14c-0.02,0.14-0.04,0.27-0.06,0.41    c-0.11,1.07-0.11,2.15,0,3.22c0.01,0.06,0.02,0.12,0.03,0.18c0.05,0.46,0.12,0.92,0.21,1.37c0.03,0.13,0.07,0.26,0.1,0.39    c0.09,0.38,0.18,0.76,0.29,1.13c0.04,0.13,0.09,0.26,0.14,0.4c0.12,0.36,0.25,0.73,0.4,1.09c0.05,0.11,0.1,0.21,0.15,0.32    c0.17,0.37,0.34,0.74,0.53,1.1c0.04,0.07,0.09,0.14,0.13,0.21c0.21,0.38,0.44,0.76,0.68,1.13c0.02,0.03,0.04,0.06,0.06,0.09    c0.55,0.81,1.18,1.58,1.89,2.29l114.81,114.81c3.12,3.12,7.22,4.69,11.31,4.69s8.19-1.56,11.31-4.69c6.25-6.25,6.25-16.38,0-22.63    l-87.5-87.5h291.62c8.84,0,16-7.16,16-16s-7.16-16-16-16H129.51L217,152.5C223.25,146.26,223.25,136.13,217,129.88z"/>
                        </g></g>
                    </svg>
                </button>

                <h1
                    class="text-3xl font-bold"
                >
                    {{ route.name }}
                </h1>
            </nav>
        </header>

        <main class="flex-grow p-6 pt-0">
            <p class="text-lg font-normal max-w-[900px] mb-10">
                this tool transcribes your speech and provides a list of
                words that you said with the statistics like usage count.
                needed words can be specified
            </p>
            
            <RouterView />
        </main>
    </div>

    <Notifications />
</template>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

@font-face {
    font-family: 'Graphik';
    src: url('@/assets/fonts/graphik-light-web.woff2');
    font-weight: 300;
}

@font-face {
    font-family: 'Graphik';
    src: url('@/assets/fonts/graphik-regular-web.woff2');
    font-weight: normal;
}

@font-face {
    font-family: 'Graphik';
    src: url('@/assets/fonts/graphik-medium-web.woff2');
    font-weight: 500;
}

@font-face {
    font-family: 'Graphik';
    src: url('@/assets/fonts/graphik-semibold-web.woff2');
    font-weight: 600;
}

@layer base {
    body {
        @apply h-screen;
    }
    
    * {
        @apply font-graphik text-neutral-900;
    }

    *::-webkit-scrollbar {
        width: 17px;
    }

    *::-webkit-scrollbar-track {
        background-color: transparent;
    }

    *::-webkit-scrollbar-thumb {
        background-color: #00000032;
        border: 5px solid transparent;
        background-clip: padding-box;
        border-radius: 100px;
    }
    *::-webkit-scrollbar-thumb:hover {
        background-color: #00000050;
    }
}
</style>
