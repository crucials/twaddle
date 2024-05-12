<script setup lang="ts">
import SelectInput from '@/components/ui/select-input.vue'
import { useNotificationsStore } from '@/stores/notifications'
import { ref } from 'vue'
import { SelectItem } from '@/types/select-item'
import { API_BASE_URL } from '@/api-url'
import { ApiResponse } from '@/types/api-response'

interface AudioDevice {
    name: string
    index: number
}

defineProps<{
    deviceIndex: string | null
}>()
const emit = defineEmits<{
    (event: 'update:deviceIndex', newValue: string | null): void
}>()

const { showNotification } = useNotificationsStore()

const items = ref<SelectItem[]>([])
await updateDevices()

async function updateDevices() {
    const devicesResponse = await fetch(API_BASE_URL + '/recording-devices')
    const devicesResponseData: ApiResponse<AudioDevice[]> = await devicesResponse.json()

    if('error' in devicesResponseData) {
        showNotification({
            type: 'error',
            text: 'failed to load recording devices: ' + devicesResponseData.explanation
        })
        return
    }

    items.value = devicesResponseData.map(device => {
        return { label: device.name, name: `${device.index}` }
    })
}
</script>

<template>
    <label class="flex-grow max-w-64 min-w-52">
        <div class="mb-1">
            recording device
        </div>
        <SelectInput
            placeholder="default"
            :items="items"
            :selected-item-name="deviceIndex"
            @update:selectedItemName="newIndex => emit('update:deviceIndex', newIndex)"
        />
    </label>
</template>
