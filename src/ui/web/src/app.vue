<script setup lang="ts">
import StartCounterPanel from '@/components/start-counter-panel.vue'
import Notifications from '@/components/notifications.vue'
</script>

<template>
    <div class="px-9 py-7 sm:px-6 sm:py-6">
        <header class="flex items-center gap-x-6 mb-10">
            <svg class="w-14" viewBox="0 0 78 78" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M74.9684 62.5466L64.6872 72.8199L54.406 62.5466L44.1248 72.8199L33.8436 62.5466L23.5624 72.8199L3 52.2733L13.2812 42L23.5624 52.2733L33.8436 42L44.1248 52.2733L54.406 42L74.9684 62.5466Z"
                    fill="#1B1B1B" />
                <path
                    d="M74.9684 25.5466L64.6872 35.8199L54.406 25.5466L44.1248 35.8199L33.8436 25.5466L23.5624 35.8199L3 15.2733L13.2812 5L23.5624 15.2733L33.8436 5L44.1248 15.2733L54.406 5L74.9684 25.5466Z"
                    fill="#8B8B8B" />
            </svg>

            <h1
                class="text-3xl font-bold tracking-wide hover:cursor-default"
            >
                spoken-words-counter
            </h1>
        </header>

        <main class="flex-grow">
            <p class="text-lg font-normal max-w-[900px] mb-10">
                this app records your speech, transcribes it and provides a list of words that you said with the usage
                count. needed words can be specified
            </p>

            <StartCounterPanel />
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
    src: url('@/assets/fonts/graphik-regular.woff2');
    font-weight: normal;
}

@font-face {
    font-family: 'Graphik';
    src: url('@/assets/fonts/graphik-medium.woff2');
    font-weight: 500;
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
