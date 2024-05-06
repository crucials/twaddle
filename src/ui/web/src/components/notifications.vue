<script setup lang="ts">
import CrossIcon from '@/components/ui/icons/cross-icon.vue'
import { storeToRefs } from 'pinia'
import { useNotificationsStore } from '@/stores/notifications'

const { notifications } = storeToRefs(useNotificationsStore())
</script>

<template>
    <TransitionGroup
        tag="ul"
        class="fixed bottom-4 right-4 flex flex-col gap-y-4 w-[410px]
            sm:w-96 sm:right-auto sm:left-1/2 sm:-translate-x-1/2 xs:w-11/12"
        enter-from-class="translate-x-12 opacity-0"
        leave-to-class="translate-x-12 opacity-0"
        tabindex="0"
    >
        <li
            v-for="notification in notifications"
            :key="notification.id"
            class="relative transition-all duration-300 bg-white shadow-lg border-2 
                border-neutral-300 rounded-lg px-8 py-6 xs:px-6 xs:py-5"
            :class="{
                'shadow-emerald-300/50': notification.type === 'success',
                'shadow-red-300/50': notification.type === 'error'
            }"
        >
            {{ notification.text }}

            <button
                class="transition-colors duration-300 absolute top-2 rounded-full right-2 p-1
                    hover:bg-neutral-100"
                @click="notifications = notifications.filter(someNotification =>
                    someNotification.id !== notification.id)"
            >
                <CrossIcon/>
            </button>
        </li>
    </TransitionGroup>
</template>
