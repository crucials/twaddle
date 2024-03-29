<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useNotificationsStore } from '@/stores/notifications'

const { notifications } = storeToRefs(useNotificationsStore())
</script>

<template>
    <TransitionGroup
        tag="ul"
        class="fixed bottom-4 right-4 flex flex-col gap-y-4 w-96"
        enter-from-class="translate-x-12 opacity-0"
        leave-to-class="translate-x-12 opacity-0"
        tabindex="0"
    >
        <li
            v-for="notification in notifications"
            :key="notification.id"
            class="transition-all duration-300 bg-white/40 backdrop-blur-sm border-2 border-neutral-300 rounded-lg w-full px-8 py-6"
        >
            {{ notification.text }}
        </li>
    </TransitionGroup>
</template>
