import { ref } from 'vue'
import { defineStore } from 'pinia';
import { Notification } from '@/types/notification'

export const useNotificationsStore = defineStore('notifications', () => {
    const notifications = ref<Notification[]>([])
    
    let lastNotificationId = 0
    function showNotification(notification: Omit<Notification, 'id'>, secondsToShow = 5) {
        const newNotificationId = lastNotificationId + 1
        lastNotificationId = newNotificationId

        notifications.value.push({ id: newNotificationId, ...notification })

        if(notifications.value.length === 4) {
            notifications.value.shift()
        }

        setTimeout(() => {
            notifications.value = notifications.value.filter(notification =>
                notification.id !== newNotificationId)
        }, secondsToShow * 1000)
    }

    return { notifications, showNotification }
})
